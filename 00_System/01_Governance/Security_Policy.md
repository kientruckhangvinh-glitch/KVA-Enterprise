[Security_Policy.md](https://github.com/user-attachments/files/30016433/Security_Policy.md)
# Security Policy — chính sách bảo mật

## Nguyên tắc chung

Repository `KVA-Enterprise` nên để **Private** trên GitHub, vì chứa dữ liệu nội bộ công ty (SOP, hồ sơ dự án, dashboard...), không phải mã nguồn mở.

## Không bao giờ commit lên GitHub

- File `.env` và mọi biến thể (`.env.local`, `.env.production`...)
- API key, token (OpenAI, Claude, Zalo OA, database credential...)
- File database thật (`.db`, `.sqlite`) chứa dữ liệu khách hàng
- Mật khẩu, private key, file chứng chỉ (`.pem`, `.key`)

Tất cả các mục trên đã được chặn sẵn trong `.gitignore` ở thư mục gốc — nhưng `.gitignore` chỉ chặn file **chưa từng được commit**. Nếu lỡ commit rồi, `.gitignore` không xoá nó khỏi lịch sử.

## Nếu lỡ commit secret lên GitHub

1. **Revoke ngay lập tức** key/token đó tại nơi cấp (GitHub Settings, OpenAI dashboard...) — coi như nó đã bị lộ vĩnh viễn, đổi bằng cách xoá và tạo cái mới.
2. Xoá khỏi lịch sử Git bằng `git filter-repo` hoặc BFG Repo-Cleaner (không chỉ xoá file ở commit mới nhất).
3. Force-push lại sau khi làm sạch lịch sử, thông báo cho các thành viên khác pull lại từ đầu.

## Quản lý Personal Access Token (PAT)

- Mỗi người dùng token riêng, không share chung một token.
- Khi tạo token, chỉ tick đúng quyền cần thiết (thường chỉ cần `repo`), không tick full quyền admin.
- Đặt hạn dùng (expiration) cho token thay vì chọn "No expiration".
- Token không dùng nữa thì revoke ngay trong GitHub Settings.

## Phân quyền truy cập

- Chỉ thêm collaborator khi thực sự cần, gỡ ngay khi người đó ngừng cộng tác.
- Dùng Branch protection cho `main` (xem `Branch_Strategy.md`) để tránh thay đổi không qua kiểm tra.

## Báo cáo sự cố bảo mật

Nếu phát hiện rò rỉ dữ liệu hoặc token, báo ngay cho Owner repository — không tự xử lý âm thầm rồi thôi, vì cần đánh giá phạm vi ảnh hưởng (đã bị truy cập chưa, cần đổi những gì).
