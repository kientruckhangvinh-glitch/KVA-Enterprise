#!/usr/bin/env python3
"""
generate_contract.py
====================
Tự động tạo hợp đồng từ Google Sheets (Stage = WON), điền dữ liệu, 
tối ưu bằng AI (Claude) và gửi cho Sales.
Tích hợp đầy đủ 5 bước của quy trình AI Agent.
"""

import os
import re
import logging
import smtplib
from datetime import datetime
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import gspread
from google.oauth2.service_account import Credentials
from docxtpl import DocxTemplate
import anthropic
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Cấu hình Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('contract_gen.log')]
)
logger = logging.getLogger(__name__)

# ==============================================================================
# CẤU HÌNH HỆ THỐNG
# ==============================================================================
CONFIG = {
    'GOOGLE_CREDS': os.getenv('GOOGLE_CREDS_PATH', 'creds/google-creds.json'),
    'SHEET_ID': os.getenv('SHEET_ID'),
    'TEMPLATE_DIR': Path('../08_Documents/01_Hop_Dong_Mau'),
    'OUTPUT_DIR': Path('../08_Documents/04_Bao_Cao_Tu_Dong/Hop_Dong'),
    'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
    'SMTP_SERVER': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'SMTP_PORT': int(os.getenv('SMTP_PORT', 587)),
    'SMTP_USER': os.getenv('SMTP_USER'),
    'SMTP_PASS': os.getenv('SMTP_PASS'),
    'SENDER_EMAIL': os.getenv('SENDER_EMAIL', 'ai-agent@kva-enterprise.com')
}

# Mapping loại dự án -> File Template
TEMPLATE_MAPPING = {
    'Thiết kế nội thất': 'HD_Thiet_Ke_No_That_Template.docx',
    'Thi công nội thất': 'HD_Thi_Cong_No_That_Template.docx',
    'Thiết kế & Thi công (Trọn gói)': 'HD_Thi_Cong_No_That_Template.docx',
    'Bảo trì': 'HD_Bao_Tri_Bao_Hanh_Template.docx'
}

# ==============================================================================
# CLASS CHÍNH: CONTRACT GENERATOR
# ==============================================================================
class ContractGenerator:
    def __init__(self):
        self.gs_client = self._init_google_sheets()
        self.ai_client = anthropic.Anthropic(api_key=CONFIG['ANTHROPIC_API_KEY'])
        CONFIG['OUTPUT_DIR'].mkdir(parents=True, exist_ok=True)

    def _init_google_sheets(self):
        """Bước 0: Khởi tạo Google Sheets Client"""
        creds = Credentials.from_service_account_file(CONFIG['GOOGLE_CREDS'])
        return gspread.authorize(creds)

    # --- BƯỚC 1: EVENT LISTENER (Lấy deal WON chưa xử lý) ---
    def get_won_deals(self):
        """Lấy danh sách deals có stage = WON và chưa tạo hợp đồng"""
        logger.info("🔍 Đang quét Google Sheets tìm deals mới WON...")
        sheet = self.gs_client.open_by_key(CONFIG['SHEET_ID']).worksheet('Opportunities')
        records = sheet.get_all_records()
        
        won_deals = []
        for idx, record in enumerate(records, start=2): # start=2 vì dòng 1 là header
            if str(record.get('stage', '')).upper() == 'WON' and str(record.get('contract_generated', '')).lower() != 'yes':
                record['_row_index'] = idx # Lưu index để update lại sheet sau này
                won_deals.append(record)
                
        logger.info(f"✅ Tìm thấy {len(won_deals)} deals cần tạo hợp đồng.")
        return won_deals

    # --- BƯỚC 2: TEMPLATE SELECTOR ---
    def select_template(self, project_type: str) -> Path:
        """Chọn template Word dựa trên loại dự án"""
        template_name = TEMPLATE_MAPPING.get(project_type)
        if not template_name:
            logger.warning(f"⚠️ Không có template cho loại '{project_type}'. Dùng template mặc định.")
            template_name = 'HD_Thi_Cong_No_That_Template.docx'
            
        template_path = CONFIG['TEMPLATE_DIR'] / template_name
        if not template_path.exists():
            raise FileNotFoundError(f" Không tìm thấy file template: {template_path}")
        return template_path

    # --- BƯỚC 3: DATA FILLER (Sử dụng docxtpl) ---
    def prepare_context(self, deal: dict) -> dict:
        """Chuẩn bị dictionary dữ liệu để merge vào Word"""
        # Xử lý ngày tháng
        today = datetime.now()
        
        # Xử lý số tiền (thêm dấu phẩy)
        quoted_value = float(deal.get('quoted_value', 0) or deal.get('estimated_value', 0))
        
        return {
            'HOP_DONG_SO': f"KVA-{deal.get('opportunity_id', 'NEW')}",
            'NGAY': today.strftime('%d'),
            'THANG': today.strftime('%m'),
            'NAM': today.strftime('%Y'),
            'TEN_CONG_TY': 'CÔNG TY TNHH KIẾN TRÚC KHANG VINH',
            'DU_AN': deal.get('project_name', ''),
            'TEN_KHACH_HANG': deal.get('customer', ''),
            'NGUOI_LIEN_HE': deal.get('contact', ''),
            'GIA_TRI_HOP_DONG': f"{quoted_value:,.0f}",
            'GIA_TRI_BANG_CHU': self._number_to_words(quoted_value), # Hàm tự viết nếu cần
            'THOI_GIAN_THI_CONG': deal.get('duration_days', '90'),
            'NGAY_KY_HOP_DONG': today.strftime('%d/%m/%Y')
        }

    def _number_to_words(self, number):
        """Placeholder: Chuyển số thành chữ. (Có thể dùng thư viện num2words)"""
        return f"{number:,.0f} đồng" 

    # --- BƯỚC 4: AI ENHANCER (Claude phân tích & thêm điều khoản) ---
    def get_ai_clauses(self, deal: dict) -> str:
        """Gọi Claude để sinh điều khoản thông minh dựa trên đặc thù deal"""
        prompt = f"""
Bạn là luật sư chuyên về hợp đồng xây dựng/nội thất tại Việt Nam.
Phân tích deal sau và viết 3 điều khoản bổ sung cụ thể để bảo vệ công ty thi công (Bên A):
- Khách hàng: {deal.get('customer')}
- Giá trị: {deal.get('quoted_value')} VND
- Loại dự án: {deal.get('project_type')}
- Tên dự án: {deal.get('project_name')}

Yêu cầu: Viết ngắn gọn, súc tích, ngôn ngữ pháp lý chuẩn. Output chỉ gồm 3 gạch đầu dòng.
"""
        try:
            response = self.ai_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Lỗi khi gọi AI: {e}")
            return "Không có đề xuất từ AI."

    def append_ai_clauses_to_doc(self, doc: DocxTemplate, ai_text: str):
        """Thêm text từ AI vào cuối document (Lưu ý: docxtpl render xong mới thao tác được)"""
        # Vì docxtpl hoạt động bằng cách render template, ta sẽ thêm 1 biến {{AI_CLAUSES}} vào template
        # Ở đây ta trả về text để gán vào context
        return ai_text.replace('\n', '\n\n') # Format lại xuống dòng cho Word

    # --- BƯỚC 5: SAVE, NOTIFY & UPDATE ---
    def save_contract(self, doc: DocxTemplate, context: dict, deal: dict) -> Path:
        """Render và lưu file Word"""
        doc.render(context)
        filename = f"HopDong_{deal.get('opportunity_id')}_{deal.get('customer', '').replace(' ', '_')}.docx"
        output_path = CONFIG['OUTPUT_DIR'] / filename
        doc.save(output_path)
        logger.info(f"💾 Đã lưu hợp đồng tại: {output_path}")
        return output_path

    def update_google_sheet(self, deal: dict):
        """Đánh dấu deal đã được tạo hợp đồng trên Google Sheets"""
        sheet = self.gs_client.open_by_key(CONFIG['SHEET_ID']).worksheet('Opportunities')
        # Cập nhật cột 'contract_generated' (Giả sử cột này là cột Z, index 26)
        # Cần điều chỉnh index cột cho khớp với Sheet thực tế của bạn
        sheet.update_cell(deal['_row_index'], 26, 'Yes') 
        sheet.update_cell(deal['_row_index'], 27, datetime.now().strftime('%Y-%m-%d %H:%M'))
        logger.info(f" Đã cập nhật trạng thái trên Google Sheets cho {deal.get('opportunity_id')}")

    def send_email_notification(self, contract_path: Path, deal: dict):
        """Gửi email thông báo cho Sales (Placeholder)"""
        sales_email = deal.get('sales_owner_email', 'sales@kva-enterprise.com') # Cần có cột email trên Sheet
        
        msg = MIMEMultipart()
        msg['From'] = CONFIG['SENDER_EMAIL']
        msg['To'] = sales_email
        msg['Subject'] = f"🎉 [AI AUTO] Hợp đồng đã tạo: {deal.get('project_name')}"
        
        body = f"""Chào bạn,\n\nAI Agent đã tự động tạo hợp đồng cho dự án {deal.get('project_name')}.\nFile đính kèm.\n\nLưu ý: AI đã tự động thêm các điều khoản bảo vệ công ty ở Mục 8."""
        msg.attach(MIMEText(body, 'plain'))
        
        with open(contract_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {contract_path.name}")
            msg.attach(part)
            
        # Bỏ comment đoạn dưới khi đã có SMTP thật
        # with smtplib.SMTP(CONFIG['SMTP_SERVER'], CONFIG['SMTP_PORT']) as server:
        #     server.starttls()
        #     server.login(CONFIG['SMTP_USER'], CONFIG['SMTP_PASS'])
        #     server.send_message(msg)
        
        logger.info(f"📧 Đã gửi email (giả lập) đến {sales_email}")

    # --- HÀM CHẠY CHÍNH (ORCHESTRATOR) ---
    def run(self):
        logger.info("="*60)
        logger.info("🚀 BẮT ĐẦU QUY TRÌNH TẠO HỢP ĐỒNG TỰ ĐỘNG")
        logger.info("="*60)
        
        deals = self.get_won_deals()
        if not deals:
            logger.info("✅ Không có deal mới nào cần xử lý. Kết thúc.")
            return

        for deal in deals:
            try:
                logger.info(f"\n🔄 Xử lý deal: {deal.get('project_name')} ({deal.get('opportunity_id')})")
                
                # 1. Chọn template
                template_path = self.select_template(deal.get('project_type'))
                doc = DocxTemplate(template_path)
                
                # 2. Chuẩn bị dữ liệu
                context = self.prepare_context(deal)
                
                # 3. Gọi AI lấy điều khoản thông minh
                ai_clauses = self.get_ai_clauses(deal)
                context['AI_CLAUSES'] = ai_clauses # Gán vào biến {{AI_CLAUSES}} trong Word
                
                # 4. Lưu file
                output_path = self.save_contract(doc, context, deal)
                
                # 5. Gửi email & Cập nhật Sheet
                self.send_email_notification(output_path, deal)
                self.update_google_sheet(deal)
                
                logger.info(f"✅ Hoàn tất deal {deal.get('opportunity_id')}")
                
            except Exception as e:
                logger.error(f"❌ Lỗi khi xử lý deal {deal.get('opportunity_id')}: {e}", exc_info=True)

if __name__ == '__main__':
    generator = ContractGenerator()
    generator.run()
