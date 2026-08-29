#!/usr/bin/env python3
"""
extract_from_sheets.py
======================
Trích xuất dữ liệu từ Google Sheets và lưu vào 10_Data/raw/
Tuân thủ SOP-SAL-001 Section 4 (Data Schema)
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_google_client(creds_json_path: str):
    """Khởi tạo Google Sheets Client"""
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(creds_json_path, scopes=scopes)
    return gspread.authorize(creds)

def sheet_to_dict_list(worksheet) -> list:
    """Chuyển đổi Google Sheet worksheet thành list of dictionaries"""
    records = worksheet.get_all_records(value_render_option='UNFORMATTED_VALUE')
    
    # Xử lý ngày tháng từ Google Sheets (thường là float serial number)
    for record in records:
        for key, value in record.items():
            if isinstance(value, float) and key.lower().endswith('date'):
                # Chuyển đổi Excel/Sheets serial date sang YYYY-MM-DD
                try:
                    dt = datetime(1899, 12, 30) + timedelta(days=value)
                    record[key] = dt.strftime('%Y-%m-%d')
                except:
                    pass
    return records

def main():
    parser = argparse.ArgumentParser(description='Extract data from Google Sheets')
    parser.add_argument('--creds', required=True, help='Path to Google Service Account JSON')
    parser.add_argument('--sheet-id', required=True, help='Google Sheet ID (from URL)')
    parser.add_argument('--output-dir', required=True, help='Output directory (10_Data/raw/)')
    
    args = parser.parse_args()
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    logger.info("Connecting to Google Sheets...")
    client = get_google_client(args.creds)
    
    try:
        sheet = client.open_by_key(args.sheet_id)
        
        # 1. Extract Opportunities
        logger.info("Extracting Opportunities...")
        opp_ws = sheet.worksheet('Opportunities') # Tên tab trong Google Sheet
        opp_data = sheet_to_dict_list(opp_ws)
        
        opp_file = output_path / 'opportunities' / f'opportunities_{datetime.now().strftime("%Y_%m")}.json'
        opp_file.parent.mkdir(exist_ok=True)
        with open(opp_file, 'w', encoding='utf-8') as f:
            json.dump({'extracted_at': datetime.now().isoformat(), 'data': opp_data}, f, indent=2, ensure_ascii=False)
        
        # 2. Extract Leads (Optional, nếu có tab riêng)
        # ... (Tương tự như trên)

        logger.info("✅ Extraction completed successfully!")
        
    except gspread.WorksheetNotFound:
        logger.error("❌ Không tìm thấy tab 'Opportunities' trong Google Sheet. Vui lòng kiểm tra tên tab.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Lỗi kết nối Google Sheets: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
