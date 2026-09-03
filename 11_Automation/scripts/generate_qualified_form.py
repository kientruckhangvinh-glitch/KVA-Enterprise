# Giả lập logic render BM-SAL-01
def render_bm_sal_01(deal_data):
    # 1. Check 4 yếu tố Qualified
    qualified_score = sum([
        deal_data['is_real_estate_verified'],
        deal_data['is_budget_matched'],
        deal_data['decision_maker_name'] != '',
        deal_data['is_timeline_valid']
    ])
    
    status = "ĐẠT CHUẨN QUALIFIED" if qualified_score == 4 else "CHƯA ĐẠT"
    
    # 2. Check Tài chính
    financial_warning = ""
    if deal_data['is_below_floor_price']:
        financial_warning = "️ CẢNH BÁO: GIÁ DƯỚI SÀN - CHUYỂN BM-SAL-03 ĐỂ CEO DUYỆT"
        
    # 3. Xuất PDF (Dùng thư viện fpdf hoặc reportlab)
    # ... code xuất PDF ...
