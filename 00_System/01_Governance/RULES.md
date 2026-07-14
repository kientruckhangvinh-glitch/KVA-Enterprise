[RULES.md](https://github.com/user-attachments/files/30016255/RULES.md)
# Rules — nguyên tắc quản trị chung

## Mục đích

Tài liệu này là "hiến pháp" cho repository KVA Enterprise: các nguyên tắc nền tảng mà mọi quy trình khác (workflow, branch, commit...) phải tuân theo.

## Nguyên tắc cốt lõi

1. **Một nguồn sự thật (Single source of truth)** — Repository GitHub là nơi lưu trữ chính thức duy nhất. Không làm việc lâu dài trên bản sao local không đồng bộ.
2. **Không commit secret** — API key, mật khẩu, Personal Access Token, file `.env` tuyệt đối không được đưa lên GitHub. Xem chi tiết tại `Security_Policy.md`.
3. **Mọi thay đổi đều có commit rõ ràng** — không commit gộp nhiều việc không liên quan vào một lần.
4. **Nhánh `main` luôn ở trạng thái chạy được** — không push thẳng code lỗi hoặc chưa test lên `main`.
5. **Tài liệu đi cùng code** — thay đổi cấu trúc, quy trình, hoặc quy ước thì phải cập nhật tài liệu tương ứng trong `00_System/`.

## Phạm vi sử dụng AI (Claude, ChatGPT, Copilot...)

- AI được dùng để hỗ trợ viết code, tài liệu, review — nhưng người dùng chịu trách nhiệm cuối cùng về nội dung commit lên repo.
- Không dán dữ liệu nội bộ nhạy cảm (thông tin khách hàng, hợp đồng, số liệu tài chính) vào AI công cộng nếu chưa được ẩn danh.
- Log/kết quả làm việc với AI có thể lưu tại `05_AI/` để tái sử dụng, không lưu trong code repo chính nếu chứa thông tin nhạy cảm.

## Phân quyền cơ bản

| Vai trò | Quyền |
|---|---|
| Owner | Toàn quyền, quản lý settings repo |
| Maintainer | Merge PR vào `main`, quản lý branch protection |
| Contributor | Tạo branch, mở Pull Request, không merge trực tiếp vào `main` |

## Vi phạm

Commit thẳng vào `main` không qua review, hoặc lộ secret lên GitHub, cần được xử lý ngay: revoke key bị lộ, revert commit, thông báo cho Owner/Maintainer.
