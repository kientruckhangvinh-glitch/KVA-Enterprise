[Workflow.md](https://github.com/user-attachments/files/30016321/Workflow.md)
# Workflow — quy trình làm việc

Áp dụng mô hình **GitHub Flow** đơn giản, phù hợp team nhỏ.

## Quy trình từ task đến merge

1. **Lấy code mới nhất**
   ```
   git checkout main
   git pull origin main
   ```

2. **Tạo nhánh mới** cho task (xem quy tắc đặt tên tại `Branch_Strategy.md`)
   ```
   git checkout -b feature/ten-tinh-nang
   ```

3. **Làm việc và commit thường xuyên** — mỗi commit là một thay đổi có ý nghĩa (xem `Commit_Convention.md`)
   ```
   git add .
   git commit -m "feat: mo ta ngan gon"
   ```

4. **Đẩy nhánh lên GitHub**
   ```
   git push -u origin feature/ten-tinh-nang
   ```

5. **Mở Pull Request (PR)** trên GitHub — mô tả rõ: làm gì, tại sao, cách test.

6. **Review** — ít nhất 1 người khác xem qua trước khi merge (nếu chỉ làm một mình, tự kiểm tra lại diff trước khi merge).

7. **Merge vào `main`** — dùng "Squash and merge" để lịch sử `main` gọn gàng, mỗi PR là một commit.

8. **Xoá nhánh đã merge** — GitHub có nút xoá nhánh ngay sau khi merge, nên dùng để tránh rác nhánh cũ.

## Khi có lỗi khẩn cấp trên production

Dùng nhánh `hotfix/` thay vì `feature/`, xử lý và merge nhanh, ưu tiên hơn các PR đang chờ khác.

## Quy tắc cho AI agent tự động (MCP, script)

Nếu để AI agent tự tạo commit/PR (ví dụ qua MCP server), agent vẫn phải:
- Tạo nhánh riêng, không commit thẳng vào `main`
- Viết commit message theo đúng `Commit_Convention.md`
- Không tự động merge — merge luôn cần người xác nhận
