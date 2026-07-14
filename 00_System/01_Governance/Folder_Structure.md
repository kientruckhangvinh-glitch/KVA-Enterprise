[Folder_Structure.md](https://github.com/user-attachments/files/30016424/Folder_Structure.md)
# Folder Structure — cấu trúc thư mục KVA-Enterprise

Giải thích mục đích từng thư mục cấp cao trong repository.

| Thư mục | Nội dung |
|---|---|
| `00_System/` | Quy tắc vận hành, chuẩn code, convention — tài liệu bắt buộc đọc trước |
| `01_Dashboard/` | Báo cáo quản trị: CEO, CFO, COO, PM, Sales |
| `02_SOP/` | Quy trình vận hành chuẩn của các phòng ban |
| `03_Projects/` | Hồ sơ dự án — đang thi công, đã hoàn thành, template |
| `04_Knowledge/` | Kho tri thức: ISO, PMBOK, Lean, luật, kiến trúc |
| `05_AI/` | Prompt, agent, MCP server, log làm việc với Claude/ChatGPT |
| `06_Library/` | Thư viện kỹ thuật: CAD, SketchUp, vật liệu, kết cấu |
| `07_Templates/` | Mẫu văn thư: hợp đồng, báo giá, checklist, báo cáo |
| `08_Documents/` | Tài liệu nội bộ: hồ sơ công ty, biên bản họp, đào tạo |
| `09_Scripts/` | Mã nguồn xử lý: Python, JavaScript, shell utility |
| `10_Data/` | Dữ liệu thô và đã xử lý: CSV, JSON, DB dump |
| `11_Automation/` | Pipeline tự động: CI/CD, cronjob, workflow |
| `12_QA_QC/` | Kiểm soát chất lượng: quy trình kiểm tra, báo cáo đánh giá |
| `13_Training/` | Đào tạo, onboarding: slide, video, tài liệu hướng dẫn |
| `14_Release/` | Phát hành phiên bản: release notes, build package |
| `15_Assets/` | Tài nguyên thương hiệu: logo, hình ảnh, icon, font |
| `Archive/` | Lưu trữ dự án, tài liệu đã kết thúc |

## Nguyên tắc thêm thư mục mới

- Thư mục cấp cao mới cần đánh số thứ tự tiếp theo (`16_...`) và phải được cập nhật vào bảng trên.
- Không tạo thư mục trùng mục đích với thư mục đã có — nếu không chắc, đặt tạm trong `Archive/` hoặc hỏi trước khi tạo.
- Thư mục rỗng cần có file `.gitkeep` để Git giữ lại (xem `.gitignore` ở thư mục gốc).
