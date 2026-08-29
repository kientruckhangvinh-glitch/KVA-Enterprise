#!/usr/bin/env python3
"""
generate_ceo_report.py
======================
Sử dụng Anthropic Claude để tạo báo cáo CEO tuần (SOP-SAL-001 Section 11)
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
import anthropic

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--metrics', required=True, help='Path to pipeline_metrics.json')
    parser.add_argument('--alerts', required=True, help='Path to pipeline_alerts.json')
    parser.add_argument('--api-key', required=True, help='Anthropic API Key')
    parser.add_argument('--output', required=True, help='Output directory for report')
    parser.add_argument('--model', default='claude-3-5-sonnet-20241022', help='Claude model')
    
    args = parser.parse_args()
    
    # 1. Load Data
    with open(args.metrics, 'r', encoding='utf-8') as f:
        metrics = json.load(f)
    with open(args.alerts, 'r', encoding='utf-8') as f:
        alerts = json.load(f)

    # 2. Build Prompt (System + User)
    system_prompt = """Bạn là CEO AI - Trợ lý Giám đốc điều hành cấp cao. 
Nhiệm vụ: Phân tích dữ liệu Sales Pipeline và tạo báo cáo tuần cho CEO theo đúng SOP-SAL-001 Section 11.
Quy tắc:
1. Chỉ sử dụng dữ liệu được cung cấp, KHÔNG bịa đặt (No hallucination).
2. Output phải là định dạng Markdown thuần túy, chuyên nghiệp, dễ đọc.
3. Sử dụng emoji (🔴, 🟡, 🟢) để đánh dấu mức độ rủi ro.
4. Tập trung vào hành động (Actionable insights) và các quyết định cần CEO phê duyệt."""

    user_prompt = f"""
## DỮ LIỆU ĐẦU VÀO
- Ngày báo cáo: {datetime.now().strftime('%Y-%m-%d')}
- Tổng cơ hội: {metrics.get('total_opportunities', 0)}
- Tổng giá trị: {metrics.get('total_value', 0):,.0f} VND
- Weighted Pipeline: {metrics.get('total_weighted_value', 0):,.0f} VND
- Số lượng cảnh báo: {alerts.get('total_alerts', 0)}

### Chi tiết cảnh báo quan trọng:
{json.dumps(alerts.get('alerts', [])[:15], indent=2, ensure_ascii=False)}

## YÊU CẦU OUTPUT
Hãy tạo báo cáo với cấu trúc chính xác sau:
# 📊 BÁO CÁO PIPELINE TUẦN (CEO AI)

## A. Executive Summary
(Tóm tắt 3-4 câu về sức khỏe pipeline, so với mục tiêu)

## B. Top Opportunities
(Liệt kê Top 3-5 cơ hội có `weighted_value` cao nhất dưới dạng bảng Markdown)

## C. Critical Opportunities (Cần CEO can thiệp)
(Phân tích các cơ hội dính RULE-SAL-004, 005, hoặc quá hạn)

## D. Pipeline Risk
(Phân tích các cảnh báo RULE-SAL-001, 002, 003. Chỉ ra điểm nghẽn)

## E. CEO Decisions Required
(Danh sách gạch đầu dòng các việc cần CEO phê duyệt ngay trong tuần)
"""

    # 3. Call Claude API
    logger.info(f"Calling Claude ({args.model})...")
    client = anthropic.Anthropic(api_key=args.api_key)
    
    try:
        response = client.messages.create(
            model=args.model,
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        report_content = response.content[0].text
        
        # 4. Save Report
        Path(args.output).mkdir(parents=True, exist_ok=True)
        week_num = datetime.now().strftime('%Y_W%V')
        filepath = Path(args.output) / f'ceo_weekly_report_{week_num}.md'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        logger.info(f"✅ Báo cáo đã được lưu tại: {filepath}")
        
    except Exception as e:
        logger.error(f"❌ Lỗi khi gọi Claude API: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
