[Branch_Strategy.md](https://github.com/user-attachments/files/30016361/Branch_Strategy.md)
# Branch Strategy — chiến lược nhánh

## Nhánh chính

| Nhánh | Mục đích | Ai được push trực tiếp |
|---|---|---|
| `main` | Code luôn chạy được, đại diện phiên bản mới nhất đã duyệt | Không ai (chỉ merge qua PR) |

## Nhánh làm việc

Đặt tên theo mẫu: `loai/mo-ta-ngan-gon` (chữ thường, cách nhau bằng dấu gạch ngang)

| Tiền tố | Dùng khi | Ví dụ |
|---|---|---|
| `feature/` | Thêm tính năng mới | `feature/taskflow-crud-api` |
| `fix/` | Sửa lỗi không khẩn cấp | `fix/login-validation` |
| `hotfix/` | Sửa lỗi khẩn cấp trên production | `hotfix/api-crash-500` |
| `docs/` | Chỉ thay đổi tài liệu | `docs/update-readme` |
| `refactor/` | Tái cấu trúc code, không đổi hành vi | `refactor/fastapi-routes` |
| `chore/` | Việc lặt vặt: cập nhật dependency, config | `chore/update-gitignore` |

## Quy tắc

- Một nhánh chỉ giải quyết **một việc** — không gộp nhiều tính năng không liên quan vào một nhánh.
- Nhánh sống càng ngắn càng tốt — mở PR sớm, tránh nhánh tồn tại quá 1-2 tuần dễ bị lệch với `main`.
- Trước khi mở PR, đồng bộ với `main` mới nhất:
  ```
  git checkout feature/ten-nhanh
  git merge main
  ```
  (hoặc `git rebase main` nếu quen dùng rebase)

## Bảo vệ nhánh `main`

Trên GitHub, vào Settings → Branches → Add rule cho `main`:
- Require pull request before merging
- Require at least 1 approval (nếu có từ 2 người trở lên)
