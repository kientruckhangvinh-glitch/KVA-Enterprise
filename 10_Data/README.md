# 10_Data - Raw & Processed Data Repository

## 📋 Mô tả
Repository lưu trữ dữ liệu thô và đã xử lý cho hệ thống Sales Pipeline (SOP-SAL-001)

## 📂 Cấu trúc dữ liệu

### Raw Data (`/raw`)
- **opportunities/**: Cơ hội kinh doanh từ CRM
  - Format: CSV, JSON
  - Fields: opportunity_id, customer_id, stage, estimated_value, probability, etc.
  
- **leads/**: Lead chưa được qualify
  - Source: Marketing, Website, Referrals
  
- **customers/**: Master data khách hàng
  - Includes: Customer profiles, contact info, history

- **activities/**: Sales activities log
  - Calls, meetings, emails, proposals

### Processed Data (`/processed`)
- **pipeline_analysis/**: Phân tích pipeline theo SOP-SAL-001
  - Weighted Pipeline calculations
  - Stage conversion rates
  - Sales cycle analysis

- **forecasts/**: Dự báo doanh thu
  - Monthly/Quarterly/Yearly forecasts
  - Best case / Base case / Worst case

- **kpi_reports/**: KPI sales team
  - Win rate, Average deal size
  - Sales performance by person

### Alerts (`/alerts`)
- Cảnh báo tự động từ RULE-SAL-001 đến RULE-SAL-007
- Stale opportunities (>7 days, >14 days)
- Overdue deals
- Low margin alerts

### CEO Reports (`/ceo_reports`)
- Weekly reports (Section 11 SOP-SAL-001)
- Monthly summaries
- Critical opportunities

## 🔄 Data Flow
