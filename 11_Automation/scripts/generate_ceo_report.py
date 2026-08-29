#!/usr/bin/env python3
"""
generate_ai_report.py
=====================
Generate CEO AI Weekly Report using LLM (Section 11 SOP-SAL-001)

Usage:
    python generate_ai_report.py --processed-data <dir> --alerts-data <dir> --prompt-file <file> --output-report <dir>

Author: KVA-Enterprise
Version: 1.0
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from openai import OpenAI
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('generate_ai_report.log')
    ]
)
logger = logging.getLogger(__name__)


class CEOAIReportGenerator:
    """Generate CEO reports using AI/LLM"""
    
    def __init__(self, api_key: str, prompt_file: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.prompt_file = Path(prompt_file)
        self.model = model
        
        # Initialize OpenAI client (or use compatible API)
        self.client = OpenAI(api_key=api_key)
        
        logger.info(f"Initialized AI client with model: {model}")
    
    def load_system_prompt(self) -> str:
        """Load system prompt from file"""
        with open(self.prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_pipeline_data(self, processed_dir: str) -> Dict:
        """Load processed pipeline metrics"""
        metrics_file = Path(processed_dir) / 'pipeline_metrics.json'
        
        with open(metrics_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_alerts(self, alerts_dir: str) -> Dict:
        """Load alerts data"""
        alerts_file = Path(alerts_dir) / 'pipeline_alerts.json'
        
        if not alerts_file.exists():
            return {'alerts': [], 'total_alerts': 0}
        
        with open(alerts_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def build_user_prompt(self, metrics: Dict, alerts: Dict) -> str:
        """Build user prompt with current data"""
        current_week = datetime.now().strftime('%Y-W%V')
        
        prompt = f"""
## BỐI CẢNH
Bạn là CEO AI - Trợ lý Giám đốc điều hành. Hãy phân tích dữ liệu Sales Pipeline hiện tại và tạo báo cáo tuần theo SOP-SAL-001 Section 11.

Tuần báo cáo: {current_week}
Ngày tạo báo cáo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## DỮ LIỆU PIPELINE

### Tổng quan:
- Tổng số cơ hội: {metrics.get('total_opportunities', 0)}
- Tổng giá trị: {metrics.get('total_value', 0):,.0f} VND
- Weighted Pipeline: {metrics.get('total_weighted_value', 0):,.0f} VND
- Win Rate: {metrics.get('conversion_rates', {}).get('win_rate_percent', 0)}%
- Deal trung bình: {metrics.get('average_deal_size', 0):,.0f} VND

### Phân bổ theo Stage:
{json.dumps(metrics.get('stage_distribution', {}), indent=2, ensure_ascii=False)}

### Hiệu suất Sales Team:
{json.dumps(metrics.get('sales_owner_performance', {}), indent=2, ensure_ascii=False)}

## CẢNH BÁO (ALERTS)

Tổng số cảnh báo: {alerts.get('total_alerts', 0)}
Phân bổ theo mức độ: {json.dumps(alerts.get('alerts_by_severity', {}), indent=2)}

### Chi tiết cảnh báo quan trọng:
{json.dumps(alerts.get('alerts', [])[:10], indent=2, ensure_ascii=False)}

## YÊU CẦU

Hãy tạo báo cáo CEO tuần theo đúng cấu trúc Section 11 SOP-SAL-001:

A. Executive Summary
B. Top Opportunities (Top 10)
C. Critical Opportunities (cần CEO can thiệp)
D. Pipeline Risk
E. Sales Performance
F. CEO Decisions Required

Sử dụng Markdown format. Dùng emoji (🔴🟡🟢) để đánh dấu mức độ rủi ro.
"""
        return prompt
    
    def generate_report(self, metrics: Dict, alerts: Dict) -> str:
        """Generate report using LLM"""
        system_prompt = self.load_system_prompt()
        user_prompt = self.build_user_prompt(metrics, alerts)
        
        logger.info("Calling LLM API to generate report...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Low temperature for consistent output
                max_tokens=4000
            )
            
            report_content = response.choices[0].message.content
            logger.info("Report generated successfully")
            
            return report_content
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            raise
    
    def save_report(self, report_content: str, output_dir: str) -> str:
        """Save report to file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with week number
        week_num = datetime.now().strftime('%Y_W%V')
        filename = f"ceo_weekly_report_{week_num}.md"
        filepath = output_path / filename
        
        # Add header
        header = f"""# CEO AI WEEKLY SALES PIPELINE REPORT

**Tuần:** {week_num}
**Ngày tạo:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Nguồn:** SOP-SAL-001 Section 11
**AI Model:** {self.model}

---

"""
        
        full_content = header + report_content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        logger.info(f"Report saved to {filepath}")
        return str(filepath)
    
    def run(self, processed_data_dir: str, alerts_dir: str, output_dir: str):
        """Run complete report generation"""
        logger.info("=" * 60)
        logger.info("STARTING CEO AI REPORT GENERATION")
        logger.info("=" * 60)
        
        try:
            # Load data
            metrics = self.load_pipeline_data(processed_data_dir)
            alerts = self.load_alerts(alerts_dir)
            
            logger.info(f"Loaded metrics: {metrics.get('total_opportunities', 0)} opportunities")
            logger.info(f"Loaded alerts: {alerts.get('total_alerts', 0)} alerts")
            
            # Generate report
            report = self.generate_report(metrics, alerts)
            
            # Save report
            filepath = self.save_report(report, output_dir)
            
            logger.info("=" * 60)
            logger.info("REPORT GENERATION COMPLETED SUCCESSFULLY")
            logger.info("=" * 60)
            
            print(f"\n✅ Report saved to: {filepath}")
            
            return True
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}", exc_info=True)
            return False


def main():
    parser = argparse.ArgumentParser(description='Generate CEO AI report')
    parser.add_argument('--processed-data', required=True, 
                       help='Directory with processed pipeline data')
    parser.add_argument('--alerts-data', required=True,
                       help='Directory with alerts data')
    parser.add_argument('--prompt-file', required=True,
                       help='System prompt file for AI')
    parser.add_argument('--output-report', required=True,
                       help='Output directory for report')
    parser.add_argument('--api-key', required=True,
                       help='OpenAI API Key (or compatible)')
    parser.add_argument('--model', default='gpt-4',
                       help='AI model to use (default: gpt-4)')
    
    args = parser.parse_args()
    
    generator = CEOAIReportGenerator(
        api_key=args.api_key,
        prompt_file=args.prompt_file,
        model=args.model
    )
    
    success = generator.run(
        processed_data_dir=args.processed_data,
        alerts_dir=args.alerts_data,
        output_dir=args.output_report
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
