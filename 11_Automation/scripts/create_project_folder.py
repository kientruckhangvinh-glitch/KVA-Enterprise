#!/usr/bin/env python3
"""
create_project_folder.py
========================
Tự động tạo folder dự án khi có hợp đồng WON từ Google Sheets.
Tích hợp với GitHub Actions để chạy tự động.
"""

import os
import re
import logging
import shutil
from datetime import datetime
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('create_project.log')
    ]
)
logger = logging.getLogger(__name__)

# ==============================================================================
# CẤU HÌNH
# ==============================================================================
CONFIG = {
    'GOOGLE_CREDS': os.getenv('GOOGLE_CREDS_PATH', 'creds/google-creds.json'),
    'SHEET_ID': os.getenv('SHEET_ID'),
    'BASE_PROJECT_DIR': Path('../03_Projects/01_Dang_Thi_Cong'),
    'TEMPLATE_DIR': Path('../03_Projects/03_Template/DA_Template_Du_An_Mau')
}

# Cấu trúc folder chuẩn cho dự án
STANDARD_FOLDERS = [
    "01_Hop_Dong",
    "02_Ho_So_Thiet_Ke",
    "03_Tien_Do_Thi_Cong",
    "04_Bien_Ban_Nghiem_Thu",
    "05_Phat_Sinh",
    "06_Ban_Giao",
    "07_Hinh_Anh_Thuc_Te"
]

class ProjectFolderGenerator:
    def __init__(self):
        self.gs_client = self._init_google_sheets()
        CONFIG['BASE_PROJECT_DIR'].mkdir(parents=True, exist_ok=True)

    def _init_google_sheets(self):
        """Khởi tạo Google Sheets Client"""
        try:
            creds = Credentials.from_service_account_file(CONFIG['GOOGLE_CREDS'])
            return gspread.authorize(creds)
        except Exception as e:
            logger.error(f"❌ Lỗi kết nối Google Sheets: {e}")
            raise

    def get_new_won_projects(self):
        """Lấy danh sách deal WON chưa được tạo folder"""
        logger.info("🔍 Đang quét Google Sheets tìm deal WON mới...")
        
        try:
            sheet = self.gs_client.open_by_key(CONFIG['SHEET_ID']).worksheet('Opportunities')
            records = sheet.get_all_records()
            
            new_projects = []
            for idx, record in enumerate(records, start=2):
                stage = str(record.get('stage', '')).upper().strip()
                is_created = str(record.get('project_folder_created', '')).lower().strip()
                
                # Kiểm tra: Stage = WON và chưa tạo folder
                if stage == 'WON' and is_created != 'yes':
                    record['_row_index'] = idx
                    new_projects.append(record)
                    
            logger.info(f"✅ Tìm thấy {len(new_projects)} deal WON cần tạo folder")
            return new_projects
            
        except Exception as e:
            logger.error(f"❌ Lỗi đọc Google Sheets: {e}")
            return []

    def sanitize_folder_name(self, name: str) -> str:
        """Chuẩn hóa tên folder (không dấu, không ký tự đặc biệt)"""
        # Xóa dấu tiếng Việt
        name = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', name)
        name = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', name)
        name = re.sub(r'[ìíịỉĩ]', 'i', name)
        name = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', name)
        name = re.sub(r'[ùúụủũưừứựửữ]', 'u', name)
        name = re.sub(r'[ỳýỵỷỹ]', 'y', name)
        name = re.sub(r'[đ]', 'd', name)
        
        # Viết hoa, thay khoảng trắng bằng dấu gạch dưới
        name = name.upper()
        name = re.sub(r'[^A-Z0-9\s]', '', name)
        name = name.replace(' ', '_')
        
        return name[:50]  # Giới hạn độ dài

    def create_project_structure(self, project: dict) -> Path:
        """Tạo cấu trúc folder cho dự án"""
        project_id = project.get('opportunity_id', 'UNKNOWN')
        customer = project.get('customer', 'Khong_Ten')
        project_name = project.get('project_name', 'Du_An_Moi')
        
        # Tạo tên folder: DA_[ID]_[TEN_DU_AN]
        clean_name = self.sanitize_folder_name(project_name)
        folder_name = f"DA_{project_id}_{clean_name}"
        project_path = CONFIG['BASE_PROJECT_DIR'] / folder_name
        
        if project_path.exists():
            logger.warning(f"⚠️ Folder {folder_name} đã tồn tại, bỏ qua")
            return project_path

        logger.info(f"📂 Đang tạo folder: {folder_name}")
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Tạo các folder con
        for sub_folder in STANDARD_FOLDERS:
            sub_path = project_path / sub_folder
            sub_path.mkdir(exist_ok=True)
            # Tạo .gitkeep để Git nhận diện folder trống
            (sub_path / '.gitkeep').touch()
            
        # Copy template README
        self._copy_template_readme(project_path, project)
        
        # Copy Excel template nếu có
        self._copy_excel_template(project_path, project_id)
        
        return project_path

    def _copy_template_readme(self, project_path: Path, project: dict):
        """Tạo README.md cho dự án"""
        readme_content = f"""#  HỒ SƠ DỰ ÁN: {project.get('project_name', 'Unknown')}

**Mã dự án:** {project.get('opportunity_id', 'Unknown')}
**Khách hàng:** {project.get('customer', 'Unknown')}
**Ngày tạo hệ thống:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**PM Phụ trách:** [Điền tên PM]
**Chỉ huy trưởng:** [Điền tên CHH]

---

## 📊 Thông tin hợp đồng

| Hạng mục | Chi tiết |
|----------|----------|
| **Giá trị hợp đồng** | {project.get('quoted_value', project.get('estimated_value', '...'))} VND |
| **Ngày ký hợp đồng** | {project.get('created_date', '...')} |
| **Ngày khởi công** | [Điền ngày] |
| **Ngày dự kiến hoàn thành** | {project.get('expected_close_date', '...')} |
| **Tiến độ thực tế** | 0% |
| **Trạng thái** | 🟡 Mới khởi động |

---

## 📑 Cấu trúc hồ sơ

1. **01_Hop_Dong/**: Hợp đồng, phụ lục, biên bản thanh toán
2. **02_Ho_So_Thiet_Ke/**: Bản vẽ 2D, 3D, hồ sơ kỹ thuật
3. **03_Tien_Do_Thi_Cong/**: Nhật ký thi công, báo cáo tuần/tháng
4. **04_Bien_Ban_Nghiem_Thu/**: BB nghiệm thu các giai đoạn
5. **05_Phat_Sinh/**: Yêu cầu phát sinh đã phê duyệt
6. **06_Ban_Giao/**: BB bàn giao, hướng dẫn sử dụng, bảo hành
7. **07_Hinh_Anh_Thuc_Te/**: Ảnh hiện trạng trước/trong/sau thi công

---

## 📈 Tiến độ các hạng mục

| STT | Hạng mục | % Hoàn thành | Ghi chú |
|-----|----------|--------------|---------|
| 1 | Chuẩn bị mặt bằng | 0% | ⏳ Chưa bắt đầu |
| 2 | [Hạng mục 2] | 0% |  Chưa bắt đầu |

---

##  Liên hệ

- **PM:** [Tên] - [SĐT]
- **Chỉ huy trưởng:** [Tên] - [SĐT]
- **Khách hàng:** {project.get('contact', '...')}

---

*Được tạo tự động bởi KVA-Enterprise AI Automation System*
*Ngày tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(project_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        logger.info(f"✅ Đã tạo README.md")

    def _copy_excel_template(self, project_path: Path, project_id: str):
        """Copy file Excel template vào folder dự án"""
        template_dir = Path('../03_Projects/03_Template/Template_Ho_So_Du_An')
        template_file = template_dir / 'Tien_Do_Thi_Cong_TEMPLATE.xlsx'
        
        if template_file.exists():
            target_dir = project_path / '03_Tien_Do_Thi_Cong'
            target_file = target_dir / f'Tien_Do_Thi_Cong_{project_id}.xlsx'
            shutil.copy2(template_file, target_file)
            logger.info(f"✅ Đã copy Excel template")
        else:
            logger.warning(f"⚠️ Không tìm thấy template Excel tại {template_file}")

    def update_sheet_status(self, project: dict):
        """Cập nhật trạng thái trên Google Sheets"""
        try:
            sheet = self.gs_client.open_by_key(CONFIG['SHEET_ID']).worksheet('Opportunities')
            row_idx = project['_row_index']
            
            # Tìm cột project_folder_created (thường là cột cuối)
            headers = sheet.row_values(1)
            col_idx = None
            
            for i, header in enumerate(headers, start=1):
                if str(header).strip() == 'project_folder_created':
                    col_idx = i
                    break
            
            if col_idx:
                sheet.update_cell(row_idx, col_idx, 'Yes')
                sheet.update_cell(row_idx, col_idx + 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                logger.info(f"✅ Đã cập nhật Google Sheets cho {project.get('opportunity_id')}")
            else:
                logger.warning(f"⚠️ Không tìm thấy cột project_folder_created trên Google Sheets")
                
        except Exception as e:
            logger.error(f"❌ Lỗi cập nhật Google Sheets: {e}")

    def run(self):
        """Chạy toàn bộ quy trình"""
        logger.info("="*60)
        logger.info("🚀 BẮT ĐẦU QUY TRÌNH TẠO FOLDER DỰ ÁN")
        logger.info("="*60)
        
        projects = self.get_new_won_projects()
        
        if not projects:
            logger.info("✅ Không có deal WON mới nào. Kết thúc.")
            return False

        created_count = 0
        for project in projects:
            try:
                project_path = self.create_project_structure(project)
                self.update_sheet_status(project)
                created_count += 1
                logger.info(f"✅ Hoàn tất: {project.get('opportunity_id')}\n")
            except Exception as e:
                logger.error(f"❌ Lỗi xử lý {project.get('opportunity_id')}: {e}", exc_info=True)
        
        logger.info("="*60)
        logger.info(f"🎉 HOÀN TẤT! Đã tạo {created_count}/{len(projects)} folder dự án")
        logger.info("="*60)
        
        return created_count > 0

if __name__ == '__main__':
    generator = ProjectFolderGenerator()
    generator.run()
