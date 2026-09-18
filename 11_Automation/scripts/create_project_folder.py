#!/usr/bin/env python3
"""
create_project_folder.py
========================
Tự động tạo cấu trúc thư mục dự án trong 03_Projects khi có hợp đồng mới (WON).
Cập nhật trạng thái trên Google Sheets để tránh tạo trùng lặp.
"""

import os
import re
import logging
import sys
from datetime import datetime
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

# Cấu hình Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('create_project.log')]
)
logger = logging.getLogger(__name__)

# ==============================================================================
# CẤU HÌNH HỆ THỐNG
# ==============================================================================
CONFIG = {
    'GOOGLE_CREDS': os.getenv('GOOGLE_CREDS_PATH', 'creds/google-creds.json'),
    'SHEET_ID': os.getenv('SHEET_ID'),
    # Đường dẫn đến thư mục chứa các dự án đang thi công
    'BASE_PROJECT_DIR': Path('../03_Projects/01_Dang_Thi_Cong'),
    'TEMPLATE_DIR': Path('../03_Projects/03_Template/Template_Ho_So_Du_An')
}

# Cấu trúc thư mục chuẩn cho mọi dự án
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
        creds = Credentials.from_service_account_file(CONFIG['GOOGLE_CREDS'])
        return gspread.authorize(creds)

    def get_new_won_projects(self):
        """Lấy danh sách các deal WON chưa được tạo thư mục"""
        logger.info("🔍 Đang quét Google Sheets tìm dự án mới cần tạo thư mục...")
        sheet = self.gs_client.open_by_key(CONFIG['SHEET_ID']).worksheet('Opportunities')
        records = sheet.get_all_records()
        
        new_projects = []
        # Giả sử cột 'project_folder_created' là cột đánh dấu (bạn cần thêm cột này vào Sheet)
        for idx, record in enumerate(records, start=2):
            stage = str(record.get('stage', '')).upper()
            is_created = str(record.get('project_folder_created', '')).lower()
            
            if stage == 'WON' and is_created != 'yes':
                record['_row_index'] = idx
                new_projects.append(record)
                
        logger.info(f"✅ Tìm thấy {len(new_projects)} dự án cần tạo thư mục.")
        return new_projects

    def sanitize_folder_name(self, name: str) -> str:
        """Làm sạch tên để tạo tên thư mục hợp lệ (không dấu, không ký tự đặc biệt)"""
        # Xóa dấu tiếng Việt
        name = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', name)
        name = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', name)
        name = re.sub(r'[ìíịỉĩ]', 'i', name)
        name = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', name)
        name = re.sub(r'[ùúụủũưừứựửữ]', 'u', name)
        name = re.sub(r'[ỳýỵỷỹ]', 'y', name)
        name = re.sub(r'[đ]', 'd', name)
        
        # Viết hoa chữ cái đầu, thay khoảng trắng bằng dấu gạch dưới
        name = name.upper()
        name = re.sub(r'[^A-Z0-9\s]', '', name)
        name = name.replace(' ', '_')
        return name[:50] # Giới hạn độ dài

    def create_project_structure(self, project: dict):
        """Tạo cấu trúc thư mục và file README cho dự án"""
        project_id = project.get('opportunity_id', 'UNKNOWN')
        customer = project.get('customer', 'Khong_Ten')
        project_name = project.get('project_name', 'Du_An_Moi')
        
        # Tạo tên thư mục: DU_AN_[ID]_[TEN_DU_AN]
        clean_name = self.sanitize_folder_name(project_name)
        folder_name = f"DA_{project_id}_{clean_name}"
        project_path = CONFIG['BASE_PROJECT_DIR'] / folder_name
        
        if project_path.exists():
            logger.warning(f"️ Thư mục {folder_name} đã tồn tại, bỏ qua.")
            return project_path

        logger.info(f"📂 Đang tạo thư mục cho dự án: {folder_name}")
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Tạo các thư mục con
        for sub_folder in STANDARD_FOLDERS:
            sub_path = project_path / sub_folder
            sub_path.mkdir(exist_ok=True)
            # Tạo file .gitkeep để Git nhận diện thư mục trống
            (sub_path / '.gitkeep').touch()
            
        # Tạo file README.md tổng quan cho dự án
        readme_content = f"""# 📁 HỒ SƠ DỰ ÁN: {project_name}

**Mã dự án:** {project_id}
**Khách hàng:** {customer}
**Ngày khởi tạo hệ thống:** {datetime.now().strftime('%Y-%m-%d')}
**PM Phụ trách:** [Điền tên PM]

---

##  Thông tin hợp đồng
- **Giá trị hợp đồng:** {project.get('quoted_value', '...')} VND
- **Ngày ký hợp đồng:** {project.get('created_date', '...')}
- **Link Google Sheets:** [Chèn link]

## 📑 Mục lục thư mục
1. `01_Hop_Dong`: Hợp đồng nguyên tắc, phụ lục, biên bản thanh lý.
2. `02_Ho_So_Thiet_Ke`: Bản vẽ 2D, 3D, hồ sơ kỹ thuật thi công.
3. `03_Tien_Do_Thi_Cong`: Nhật ký thi công, báo cáo tuần/tháng.
4. `04_Bien_Ban_Nghiem_Thu`: BB nghiệm thu giai đoạn, nghiệm thu hoàn thành.
5. `05_Phat_Sinh`: Các yêu cầu phát sinh khối lượng/chi phí đã được phê duyệt.
6. `06_Ban_Giao`: Biên bản bàn giao, hướng dẫn sử dụng, hồ sơ bảo hành.
7. `07_Hinh_Anh_Thuc_Te`: Ảnh chụp hiện trạng trước, trong và sau thi công.

---
*Được tạo tự động bởi KVA-Enterprise AI Automation System*
"""
        with open(project_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        return project_path

    def update_sheet_status(self, project: dict):
        """Đánh dấu trên Google Sheets là đã tạo thư mục"""
        sheet = self.gs_client.open_by_key(CONFIG['SHEET_ID']).worksheet('Opportunities')
        row_idx = project['_row_index']
        
        # Giả sử cột 'project_folder_created' là cột thứ 28 (AA). 
        # ⚠️ BẠN CẦN ĐIỀU CHỈNH SỐ CỘT NÀY CHO ĐÚNG VỚI SHEET THỰC TẾ CỦA BẠN
        col_idx = 28 
        
        sheet.update_cell(row_idx, col_idx, 'Yes')
        sheet.update_cell(row_idx, col_idx + 1, datetime.now().strftime('%Y-%m-%d %H:%M'))
        logger.info(f"🔄 Đã cập nhật trạng thái trên Google Sheets cho {project.get('opportunity_id')}")

    def run(self):
        logger.info("="*60)
        logger.info("🚀 BẮT ĐẦU QUY TRÌNH TẠO THƯ MỤC DỰ ÁN")
        logger.info("="*60)
        
        projects = self.get_new_won_projects()
        if not projects:
            logger.info("✅ Không có dự án mới nào cần xử lý. Kết thúc.")
            return

        for project in projects:
            try:
                self.create_project_structure(project)
                self.update_sheet_status(project)
                logger.info(f"✅ Hoàn tất xử lý dự án {project.get('opportunity_id')}\n")
            except Exception as e:
                logger.error(f"❌ Lỗi khi xử lý dự án {project.get('opportunity_id')}: {e}", exc_info=True)

if __name__ == '__main__':
    generator = ProjectFolderGenerator()
    generator.run()
