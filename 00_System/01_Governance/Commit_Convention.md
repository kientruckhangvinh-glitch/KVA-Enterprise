[Commit_Convention.md](https://github.com/user-attachments/files/30016388/Commit_Convention.md)
# Commit Convention — chuẩn viết commit message

Áp dụng chuẩn **Conventional Commits**.

## Cấu trúc

```
loai(pham-vi): mo ta ngan gon o thi hien tai

Mo ta chi tiet hon neu can (tuy chon)
```

## Các loại (type)

| Type | Khi nào dùng |
|---|---|
| `feat` | Thêm tính năng mới |
| `fix` | Sửa lỗi |
| `docs` | Chỉ thay đổi tài liệu |
| `style` | Format code, không đổi logic (khoảng trắng, dấu chấm phẩy...) |
| `refactor` | Tái cấu trúc code, không thêm tính năng, không sửa lỗi |
| `test` | Thêm hoặc sửa test |
| `chore` | Việc lặt vặt: cập nhật dependency, config, `.gitignore` |
| `perf` | Cải thiện hiệu năng |

## Ví dụ thực tế (theo TaskFlow)

```
feat(api): them endpoint tao task moi

fix(auth): sua loi token het han khong redirect ve login

docs(readme): cap nhat huong dan cai dat cho Windows

refactor(backend): tach logic CRUD ra service layer rieng

chore: cap nhat .gitignore cho Python va Node.js
```

## Quy tắc viết

- Dòng đầu tiên **dưới 72 ký tự**, không có dấu chấm cuối câu.
- Dùng động từ ở dạng nguyên mẫu/hiện tại: "them", "sua", "xoa" — không dùng "đã thêm", "added".
- Phạm vi (scope) trong ngoặc đơn là tuỳ chọn, dùng khi cần chỉ rõ phần nào bị ảnh hưởng: `api`, `frontend`, `backend`, `docs`...
- Không viết chung chung như `update code`, `fix bug` — phải nói rõ sửa gì.
