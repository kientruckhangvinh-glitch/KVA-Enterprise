[Naming_Convention.md](https://github.com/user-attachments/files/30016400/Naming_Convention.md)
# Naming Convention — chuẩn đặt tên

## Thư mục cấp cao (trong KVA-Enterprise)

Mẫu: `NN_TenThuMuc` — hai chữ số thứ tự + gạch dưới + tên viết hoa chữ đầu mỗi từ, không dấu cách.

```
00_System/
01_Dashboard/
02_SOP/
```

## File tài liệu (.md)

`PascalCase_With_Underscore.md` — mỗi từ viết hoa chữ đầu, nối bằng gạch dưới.

```
Branch_Strategy.md
Commit_Convention.md
```

## Code — Python (backend FastAPI)

- File, biến, hàm: `snake_case` — `task_service.py`, `def get_task_by_id():`
- Class: `PascalCase` — `class TaskModel:`
- Hằng số: `UPPER_SNAKE_CASE` — `MAX_RETRY_COUNT = 3`

## Code — TypeScript / React Native (frontend TaskFlow)

- Component file: `PascalCase.tsx` — `TaskList.tsx`, `AddTaskButton.tsx`
- Hook, util, biến: `camelCase` — `useTaskStore.ts`, `formatDate()`
- Type / Interface: `PascalCase` — `interface TaskItem { ... }`
- Hằng số: `UPPER_SNAKE_CASE` — `const API_BASE_URL = "..."`

## Nhánh Git

Xem chi tiết tại `Branch_Strategy.md` — mẫu chung: `loai/mo-ta-ngan-gon` (chữ thường, gạch ngang).

## Nguyên tắc chung

- Tên phải mô tả được **nó làm gì**, không dùng tên chung chung như `utils2.py`, `test.tsx`, `temp_file.md`.
- Không dùng tiếng Việt có dấu trong tên file/folder/biến — dùng không dấu hoặc tiếng Anh để tránh lỗi encoding trên các hệ điều hành khác nhau.
- Không dùng khoảng trắng trong tên file — thay bằng gạch dưới hoặc gạch ngang.
