#!/usr/bin/env python3
"""
process_and_alert.py
====================
Xử lý dữ liệu, tính Weighted Pipeline và kích hoạt cảnh báo (RULE-SAL-001 đến 007)
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path: str) -> dict:
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_rules(opp: dict, config: dict, today: datetime) -> list:
    """Kiểm tra các quy tắc cảnh báo SOP-SAL-001 Section 7"""
    alerts = []
    opp_id = opp.get('opportunity_id', 'UNKNOWN')
    stage = opp.get('stage', '').upper()
    value = float(opp.get('estimated_value', 0))
    margin = float(opp.get('gross_margin_estimate', 100))
    
    # RULE-SAL-001 & 002: Stale Opportunities
    last_activity = opp.get('last_activity_date')
    if last_activity and stage not in ['WON', 'LOST']:
        try:
            act_date = datetime.strptime(last_activity, '%Y-%m-%d')
            days_inactive = (today - act_date).days
            
            if days_inactive > 14:
                alerts.append({'rule': 'RULE-SAL-002', 'severity': 'HIGH_RISK', 'id': opp_id, 'msg': f'Không hoạt động {days_inactive} ngày'})
            elif days_inactive > 7:
                alerts.append({'rule': 'RULE-SAL-001', 'severity': 'WARNING', 'id': opp_id, 'msg': f'Không hoạt động {days_inactive} ngày'})
        except ValueError:
            pass

    # RULE-SAL-003: Overdue
    close_date = opp.get('expected_close_date')
    if close_date and stage not in ['WON', 'LOST']:
        try:
            if datetime.strptime(close_date, '%Y-%m-%d') < today:
                alerts.append({'rule': 'RULE-SAL-003', 'severity': 'OVERDUE', 'id': opp_id, 'msg': f'Quá hạn chốt: {close_date}'})
        except ValueError:
            pass

    # RULE-SAL-004: CEO Review Threshold
    if value >= config.get('CEO_REVIEW_THRESHOLD_VALUE', 5000000000) and stage not in ['WON', 'LOST']:
        alerts.append({'rule': 'RULE-SAL-004', 'severity': 'CEO_REVIEW', 'id': opp_id, 'msg': f'Giá trị cao: {value:,.0f} VND'})

    # RULE-SAL-005: Low Margin
    if margin < config.get('MIN_GROSS_MARGIN_ALLOWED', 15) and stage not in ['LOST']:
        alerts.append({'rule': 'RULE-SAL-005', 'severity': 'LOW_MARGIN', 'id': opp_id, 'msg': f'Biên lợi nhuận thấp: {margin}%'})

    return alerts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input JSON file from raw/')
    parser.add_argument('--config', required=True, help='System config JSON')
    parser.add_argument('--out-processed', required=True, help='Output dir for processed/')
    parser.add_argument('--out-alerts', required=True, help='Output dir for alerts/')
    
    args = parser.parse_args()
    config = load_config(args.config)
    today = datetime.now()

    logger.info(f"Loading data from {args.input}")
    with open(args.input, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    opportunities = raw_data.get('data', raw_data)
    processed_opps = []
    all_alerts = []
    
    total_value = 0
    total_weighted = 0

    for opp in opportunities:
        # 1. Calculate Weighted Value (SOP Section 6)
        prob = float(opp.get('probability', 0))
        value = float(opp.get('estimated_value', 0))
        weighted = value * (prob / 100)
        opp['weighted_value'] = round(weighted, 2)
        
        total_value += value
        total_weighted += weighted
        
        # 2. Check Rules
        alerts = check_rules(opp, config, today)
        all_alerts.extend(alerts)
        
        processed_opps.append(opp)

    # Save Processed Data
    Path(args.out_processed).mkdir(parents=True, exist_ok=True)
    with open(Path(args.out_processed) / 'pipeline_metrics.json', 'w', encoding='utf-8') as f:
        json.dump({
            'processed_at': today.isoformat(),
            'total_opportunities': len(processed_opps),
            'total_value': total_value,
            'total_weighted_value': total_weighted,
            'data': processed_opps
        }, f, indent=2, ensure_ascii=False)

    # Save Alerts
    Path(args.out_alerts).mkdir(parents=True, exist_ok=True)
    with open(Path(args.out_alerts) / 'pipeline_alerts.json', 'w', encoding='utf-8') as f:
        json.dump({
            'generated_at': today.isoformat(),
            'total_alerts': len(all_alerts),
            'alerts': all_alerts
        }, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Processed {len(processed_opps)} opportunities. Weighted Pipeline: {total_weighted:,.0f} VND")
    logger.info(f"⚠️ Generated {len(all_alerts)} alerts.")

if __name__ == '__main__':
    main()
