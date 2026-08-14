# NGUYÊN TẮC BÁO CÁO · v1.0
Mã: DASH-RULE-v1.0 · Áp dụng: mọi block của 01_Dashboard
Ban hành: …/…/2026 · Phê duyệt: CEO · Rà soát: mỗi quý

──────────────────────────────────────────
## PHẦN I · NGUYÊN TẮC CỐT LÕI
──────────────────────────────────────────

## Điều 1. No source, no number
1.1. Mọi con số phải ghi nguồn [module/file].
     ĐÚNG: "Tồn quỹ 420M (nguồn: 10_Data/TaiChinh/2026-W33.md)"
     SAI:  "Tồn quỹ khoảng 400M"
1.2. Số không nguồn = không tồn tại; người tổng hợp được quyền trả về,
     không cần xin phép.

## Điều 2. Dashboard ≠ kho dữ liệu
2.1. Dashboard chỉ TỔNG HỢP. Dữ liệu gốc sống tại:
     tiền → 10_Data/TaiChinh · dự án → 03_Projects ·
     chất lượng → 12_QA_QC · lead → 10_Data/Marketing.
2.2. Cấm nhập liệu song song hai nơi — lệch nhau thì nguồn gốc thắng.

## Điều 3. Mỗi kỳ một file
3.1. Tuần: 2026-W33.md · Tháng: 2026-08_Thang.md (đặt trong thư mục 2026/).
3.2. Kỳ đã đóng KHÔNG chỉnh sửa.
3.3. Đính chính: ghi vào file kỳ hiện tại + commit message
     "Đính chính W33: …" + một dòng trong CHANGELOG.md.
     (Git vẫn giữ lịch sử như lớp dự phòng, nhưng quy tắc làm việc là 3.2–3.3.)

## Điều 4. Mẫu cố định
4.1. Mọi block điền theo Mau_*.md tương ứng — điền, không viết lại từ đầu.
4.2. Thêm/bỏ/sửa cột = tu chính: mở Issue → CEO duyệt → cập nhật Mau_*.md,
     tăng phiên bản mẫu, ghi CHANGELOG.md.
4.3. Mỗi quý rà soát: KPI nào 3 kỳ liền không ai nhìn → đề xuất bỏ.

## Điều 5. Ngôn ngữ đèn giao thông
5.1. 🟢 đạt · 🟡 lệch <10% hoặc cần theo dõi · 🔴 lệch ≥10% / quá hạn / cần quyết.
5.2. Mỗi 🔴 BẮT BUỘC kèm 1 đề xuất xử lý. Báo đỏ suông = trả về.
5.3. 🟡 lặp lại 2 tuần liên tiếp → tự động nâng thành 🔴.

## Điều 6. Kỷ luật thời gian
| Mốc | Việc | Người |
|---|---|---|
| 17h thứ 5 | Điền xong block vai trò | từng vai trò |
| 17h thứ 6 | Đóng Báo cáo CEO tuần | PM Office |
| 8h30 thứ 2 | Giao ban theo dashboard | toàn bộ |
| Ngày 5 | Báo cáo tháng + rà soát KPI | từng vai trò |
6.2. Trễ: ghi công khai "trễ …h" ngay trong báo cáo; lần 1 nhắc nhở,
     lần 2 trở đi nêu trong giao ban.

## Điều 7. Bảo mật
7.1. Block chứa số MẬT (tiền, công nợ, lương) phân quyền theo
     Security_Policy Điều 4.
7.2. Không chụp màn hình báo cáo gửi ra ngoài; gửi ngoài = xuất PDF có duyệt.

──────────────────────────────────────────
## PHẦN II · TỪ ĐIỂN KPI (định nghĩa chuẩn, chống mỗi người hiểu một kiểu)
──────────────────────────────────────────
| KPI | Công thức / định nghĩa | Nguồn | Chủ sở hữu | Ngưỡng tham khảo* |
|---|---|---|---|---|
| Tồn quỹ cuối tuần | Số dư tiền mặt + ngân hàng cuối tuần | 10_Data/TaiChinh | Kế toán | ≥ 3 tháng chi phí cố định |
| Công nợ >60 ngày | Tổng phải thu quá hạn 60 ngày | 10_Data/TaiChinh | Kế toán | ≤ 10% doanh thu quý |
| CAC / HĐ ký | Chi MKT ÷ số HĐ ký (nguồn MKT) | 10_Data/Marketing | Marketing | ≤ 8tr/HĐ |
| Lead A | Lead đủ 4 trường + phân khúc A | 10_Data/Marketing | Marketing | theo kế hoạch tuần |
| Lead → Khảo sát | Số khảo sát ÷ số lead | sheet lead | Marketing | ≥ 30% |
| Lệch tiến độ | Lũy kế thực tế − lũy kế kế hoạch | biên bản tuần dự án | PM | ≥ −10% là 🔴 |
| Phát sinh treo | PS chưa duyệt > 7 ngày | 03_Projects | PM | 0 |
| Nghiệm thu đạt lần 1 | Lượt đạt ÷ lượt kiểm tra | 12_QA_QC | QA/PM | ≥ 90% |
| Số vòng sửa thiết kế | Lượt revision/hồ sơ | 03_Projects block TK | Lead TK | ≤ 2 vòng |
| Pipeline | Tổng giá trị cơ hội đang theo | sheet lead | Sales | ≥ 3× kế hoạch tháng |
(* Con số minh họa — công ty tự quyết và ghi vào bản ban hành.)

──────────────────────────────────────────
## PHẦN III · THỂ THỨC HỌP GIAO BAN THỨ 2 (30 phút)
──────────────────────────────────────────
8.1. Trước họp: MỌI người tự đọc báo cáo. Ai chưa đọc → không phát biểu kể lể.
8.2. Trình tự:
     (1) PM Office quét đèn toàn bảng — 2 phút.
     (2) Từng 🔴: chủ sở hữu nêu nguyên nhân + đề xuất — ≤3 phút/đèn.
     (3) CEO chốt tại chỗ: hành động + người + hạn; ghi vào mục 6 kỳ sau.
     (4) 🟡 chỉ nêu khi thành xu hướng 2 tuần.
8.3. Cấm trong phòng họp: đọc lại báo cáo thành lời; kể chuyện từ đầu;
     truy cứu cá nhân — việc đó họp 1-1 riêng.

──────────────────────────────────────────
## PHẦN IV · CHECKLIST NGƯỜI TỔNG HỢP (đóng báo cáo CEO, thứ 6)
──────────────────────────────────────────
- [ ] Đủ 5 block vai trò trước 17h thứ 5?
- [ ] Mọi con số có nguồn (Điều 1)?
- [ ] Mọi 🔴 có đề xuất xử lý (Điều 5.2)?
- [ ] Số lũy kế khớp báo cáo tuần trước?
- [ ] Commit + đặt tên đúng chuẩn (2026-Wxx.md)?
- [ ] Gửi link cho toàn công ty trước 17h thứ 6?

──────────────────────────────────────────
## PHẦN V · VI PHẠM THƯỜNG GẶP & XỬ LÝ
──────────────────────────────────────────
| # | Vi phạm | Xử lý |
|---|---|---|
| 1 | Số không nguồn | Trả về, không hỏi lại |
| 2 | 🔴 không đề xuất | Trả về trong họp |
| 3 | Sửa file kỳ đã đóng | Nhắc nhở + đính chính đúng Điều 3.3 |
| 4 | 3 tuần liền toàn 🟢 nhưng sự cố vẫn nổ | Audit nguồn dữ liệu block đó |
| 5 | Tự ý thêm cột vào mẫu | Gỡ + hướng dẫn tu chính Điều 4.2 |

## Điều 9. Tu chính văn bản này
Theo quy trình tu chính của 00_System/Governance_Rules;
mọi sửa đổi tăng phiên bản và ghi CHANGELOG.md.
