# 01_DASHBOARD · BUỒNG LÁI CỦA DOANH NGHIỆP
Phiên bản v1.0 · Người giữ module: CEO (duyệt) · PM Office (vận hành)
Văn bản kèm: 00_Nguyen_Tac_Bao_Cao.md (LUẬT báo cáo) ·
00_System/Security_Policy.md (bảo mật) ·
02_SOP/00_He_Thong_Quan_Tri/SOP-CEO-002 & 003 (họp & báo cáo)

──────────────────────────────────────────
## 1. MỤC ĐÍCH
──────────────────────────────────────────
1.1. MỘT chỗ nhìn toàn cảnh: TIỀN – VIỆC – KHÁCH – NGƯỜI.
1.2. Ra quyết định theo dữ liệu có nguồn, không theo cảm xúc.
1.3. Lịch sử mọi kỳ kinh doanh lưu vĩnh viễn qua git —
     1 năm sau vẫn trả lời được: "Tuần này năm ngoái tồn quỹ bao nhiêu,
     dự án nào đỏ đèn?"
1.4. Dashboard KHÔNG phải:
     - kho dữ liệu (dữ liệu gốc sống ở 03_Projects / 10_Data / 12_QA_QC)
     - nơi nhập liệu hai lần
     - nơi truy cứu cá nhân (đèn đỏ là để sửa việc, không để phạt người)

──────────────────────────────────────────
## 2. VAI TRÒ · AI ĐIỀN, AI ĐỌC
──────────────────────────────────────────
| Vai trò | Điền block | Đọc | Ghi chú |
|---|---|---|---|
| CEO | — (chỉ chốt mục "Cần quyết định") | Tất cả | Người quyết, không phải người kể |
| PM Office | 01_CEO (tổng hợp tuần) | Tất cả | Đóng báo cáo thứ 6 |
| Kế toán | 02_CFO + mục TIỀN tuần | Block mình + CEO | |
| PM | 03_PM_COO | Block mình + CEO | |
| Sales | 04_Sales | Block mình + CEO + Marketing | |
| Marketing | 06_Marketing | Block mình + CEO + Sales | |
| Lead thiết kế | 05_Thiet_Ke | Block mình + CEO | |
| Nhân viên mới | — | Block INT theo phân quyền | 30 ngày đầu chỉ đọc |

Quyền đọc chi tiết theo Security_Policy Điều 4.

──────────────────────────────────────────
## 3. NHỊP ĐIỆU BÁO CÁO
──────────────────────────────────────────
### Chu kỳ tuần
| Mốc | Việc | Người |
|---|---|---|
| 17h thứ 5 | Điền xong block vai trò (2026-Wxx.md) | từng vai trò |
| 17h thứ 6 | Đóng Báo cáo CEO tuần | PM Office |
| 8h30 thứ 2 | Giao ban 30' theo dashboard | toàn công ty |

### Chu kỳ tháng
| Mốc | Việc | Người |
|---|---|---|
| Ngày 3 | Điền báo cáo tháng block mình | từng vai trò |
| Ngày 5 | Đóng 02_CFO tháng + họp review CEO | CFO/CEO |

### Chu kỳ quý
- Rà soát KPI: chỉ số nào 3 kỳ không ai nhìn → đề xuất bỏ; thiếu → tu chính.
- Ban hành lại ngưỡng đèn 🟢🟡 trong Từ điển KPI.

──────────────────────────────────────────
## 4. CẤU TRÚC MODULE
──────────────────────────────────────────
01_Dashboard/
├── README.md                  ← file này
├── 00_Nguyen_Tac_Bao_Cao.md   ← luật (nguồn duy nhất của mọi quy tắc)
├── 01_CEO/      Mau_Tuan · Mau_Thang · 2026/
├── 02_CFO/      Mau_Thang · 2026/
├── 03_PM_COO/   Mau_Tuan_DuAn · 2026/
├── 04_Sales/    Mau_Tuan · 2026/
├── 05_Thiet_Ke/ Mau_Tuan · 2026/
└── 06_Marketing/ Mau_Tuan · 2026/

──────────────────────────────────────────
## 5. DÒNG DỮ LIỆU
──────────────────────────────────────────
10_Data/TaiChinh ────────→ 02_CFO ──
03_Projects + 12_QA_QC ──→ 03_PM_COO ─┤
sheet lead ──────────────→ 04_Sales ──┼─→ 01_CEO ─→ giao ban thứ 2
03_Projects (block TK) ──→ 05_Thiet_Ke ┤
10_Data/Marketing ───────→ 06_Marketing ┘

Nguyên tắc: block vai trò là TRẠM trung chuyển một chiều —
số liệu chỉ chảy VỀ 01_CEO, không chảy ngược.

──────────────────────────────────────────
## 6. QUY ƯỚC ĐẶT TÊN & COMMIT
──────────────────────────────────────────
- Tuần: 2026-W33.md (tuần ISO) · Tháng: 2026-08_Thang.md
- File mẫu: Mau_*.md — KHÔNG điền dữ liệu vào file mẫu.
- Commit: "Bao cao W33: [vai trò]" · VD "Bao cao W33: Marketing"
- Đính chính: xem Luật Điều 3.

──────────────────────────────────────────
## 7. HƯỚNG DẪN 5 PHÚT CHO NGƯỜI MỚI
──────────────────────────────────────────
1. Mở 01_CEO/2026/ file tuần mới nhất → nhìn Trạng thái tổng + mục 🔴.
2. Mở block của vai trò mình → đọc 2 kỳ gần nhất để hiểu "giọng" điền.
3. Đọc 00_Nguyen_Tac_Bao_Cao.md (15 phút) TRƯỚC khi điền lần đầu.
4. Hỏi PM Office nếu không chắc nguồn của một con số —
   tuyệt đối không đoán.

──────────────────────────────────────────
## 8. FAQ
──────────────────────────────────────────
Q: Điền nhầm số?      → A: Không sửa kỳ đóng; đính chính theo Luật Điều 3.
Q: Muốn thêm chỉ số?  → A: Tu chính theo Luật Điều 4 (Issue → CEO duyệt).
Q: Thiếu nguồn?       → A: Trả về theo Luật Điều 1 — không phải lỗi của ai,
                           là lỗi của hệ thống thu thập, ghi nhận để sửa.
Q: Họp có cần đọc to? → A: Không. Đọc trước ở nhà; họp chỉ bàn 🔴 (Luật Phần III).

──────────────────────────────────────────
## 9. LỊCH SỬ PHIÊN BẢN
──────────────────────────────────────────
v1.0 · …/…/2026 · Ban hành 6 block: CEO, CFO, PM_COO, Sales, Thiet_Ke, Marketing.
