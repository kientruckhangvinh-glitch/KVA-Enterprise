# KVA ENTERPRISE

# DATA STANDARDS

**Version:** 1.0
**Status:** ACTIVE
**Owner:** CEO / System Administrator
**Folder:** `02_Data_Standards/`

---

# 1. MỤC ĐÍCH

`02_Data_Standards/` là lớp **chuẩn hóa dữ liệu** của KVA Enterprise.

Mục tiêu là đảm bảo:

> **Con người, AI Agent, Dashboard, SOP, Database và các hệ thống phần mềm đều hiểu và sử dụng dữ liệu theo cùng một chuẩn.**

Folder này không phải nơi lưu toàn bộ dữ liệu nghiệp vụ.

Nó là nơi quy định:

* Dữ liệu là gì.
* Dữ liệu được đặt tên thế nào.
* ID được tạo ra sao.
* Các đối tượng liên kết với nhau thế nào.
* Trường dữ liệu nào bắt buộc.
* Giá trị nào được phép.
* AI được phép làm gì với dữ liệu.
* Dữ liệu nào được xem là nguồn chính thức.

---

# 2. VAI TRÒ TRONG KIẾN TRÚC KVA ENTERPRISE

Mô hình tổng thể:

```text
                    KVA ENTERPRISE
                          │
              ┌───────────┴───────────┐
              │                       │
           PEOPLE                     AI
              │                       │
              └───────────┬───────────┘
                          ↓
                    DATA STANDARDS
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
        Data Model      ID Rule     Data Quality
             │            │            │
             └────────────┼────────────┘
                          ↓
                  BUSINESS DATA
                          │
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
      SOP              PROJECT           DASHBOARD
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ↓
                    AI AGENTS
                          │
                          ↓
                    DECISION SUPPORT
```

---

# 3. CẤU TRÚC FOLDER

```text
02_Data_Standards/
│
├── README.md
├── Data_Dictionary.md
└── ID_Convention.md
```

## README.md

Tài liệu hướng dẫn sử dụng Data Standards.

## Data_Dictionary.md

Từ điển dữ liệu.

Định nghĩa:

* Entity.
* Field.
* Data type.
* Required field.
* Status.
* Relation.
* Evidence.
* Data ownership.

## ID_Convention.md

Quy định mã định danh duy nhất.

Ví dụ:

```text
CUS-2026-000001
PROJ-2026-000001
SITE-2026-000001
TASK-2026-000001
DOC-2026-000001
IMG-2026-000001
```

---

# 4. NGUYÊN TẮC CỐT LÕI

## Rule 01 — ONE DATA / ONE DEFINITION

Một loại dữ liệu chỉ có một định nghĩa chuẩn.

Không được:

```text
Customer Name
Client Name
Khách hàng
Tên KH
```

cùng tồn tại với ý nghĩa khác nhau nếu không được quy định.

---

## Rule 02 — ONE ENTITY / ONE ID

Mỗi entity có một ID duy nhất.

Ví dụ:

```text
customer_id = CUS-2026-000001
```

ID không được thay đổi chỉ vì tên hoặc thông tin đối tượng thay đổi.

---

## Rule 03 — SOURCE OF TRUTH

Mỗi dữ liệu quan trọng phải xác định được nguồn chính.

Ví dụ:

```text
Tiến độ
    ↓
Project Schedule
    ↓
Approved Version
```

Không lấy một tin nhắn không xác nhận làm nguồn chính nếu đã có hồ sơ chính thức.

---

## Rule 04 — NO GUESSING

AI không được tự tạo dữ liệu.

Nếu thiếu dữ liệu:

> **KHÔNG ĐỦ DỮ LIỆU KẾT LUẬN**

---

## Rule 05 — EVIDENCE FIRST

Thông tin quan trọng phải có bằng chứng khi cần.

Ví dụ:

```text
QUALITY
    ↓
QC Checklist
    ↓
Inspection Record
    ↓
Photo Evidence
```

---

# 5. NGUỒN DỮ LIỆU ƯU TIÊN

Khi có nhiều nguồn khác nhau:

```text
01. User Confirmed
02. Official Repository
03. Approved SOP
04. Checklist / Acceptance Record
05. Database
06. Project Documents
07. Technical Standards
08. Law / Regulation
09. Web
10. AI Knowledge
```

Nguồn ở cấp thấp không được tự động ghi đè nguồn cấp cao.

---

# 6. DATA MODEL CỐT LÕI

KVA Enterprise sử dụng mô hình:

```text
CUSTOMER
    │
    ↓
PROJECT
    │
    ├── CONTRACT
    │
    ├── SITE
    │      ├── TASK
    │      ├── ISSUE
    │      └── IMAGE
    │
    ├── DOCUMENT
    │
    ├── COST
    │
    ├── PAYMENT
    │
    └── REPORT
```

Đây là cấu trúc quan hệ nền tảng.

AI Agent phải hiểu quan hệ này trước khi truy vấn dữ liệu.

---

# 7. ENTITY CHÍNH

| Entity   | Ý nghĩa    | ID            |
| -------- | ---------- | ------------- |
| Customer | Khách hàng | `customer_id` |
| Project  | Dự án      | `project_id`  |
| Site     | Công trình | `site_id`     |
| Contract | Hợp đồng   | `contract_id` |
| Task     | Công việc  | `task_id`     |
| Document | Hồ sơ      | `document_id` |
| Image    | Hình ảnh   | `image_id`    |
| Issue    | Phát sinh  | `issue_id`    |
| Cost     | Chi phí    | `cost_id`     |
| Payment  | Thanh toán | `payment_id`  |
| KPI      | Chỉ số     | `kpi_id`      |
| Report   | Báo cáo    | `report_id`   |
| User     | Nhân sự    | `user_id`     |
| Role     | Vai trò    | `role_id`     |

Chi tiết từng entity xem:

`Data_Dictionary.md`

---

# 8. QUY TẮC ĐẶT TÊN FIELD

Field sử dụng:

```text
snake_case
```

Ví dụ:

```text
customer_id
project_id
project_name
start_date
planned_end_date
actual_end_date
created_at
updated_at
```

Không sử dụng tùy tiện:

```text
CustomerID
CustomerId
customerID
TênKháchHàng
```

---

# 9. QUY TẮC THỜI GIAN

Ngày:

```text
YYYY-MM-DD
```

Ví dụ:

```text
2026-08-19
```

Ngày + giờ:

```text
YYYY-MM-DD HH:MM:SS
```

Ví dụ:

```text
2026-08-19 21:30:00
```

Không dùng các định dạng ngày tháng không thống nhất trong dữ liệu hệ thống.

---

# 10. QUY TẮC TIỀN TỆ

Mọi giá trị tiền phải có:

```text
amount
currency
```

Ví dụ:

```text
amount: 1500000000
currency: VND
```

Không ghi:

```text
1.5 tỷ
```

làm giá trị dữ liệu chính.

Có thể dùng cách viết này trong giao diện báo cáo, nhưng database phải lưu giá trị số.

---

# 11. QUY TẮC PHẦN TRĂM

Tỷ lệ phải có đơn vị rõ ràng.

Ví dụ:

```text
conversion_rate = 25%
```

Không được ghi:

```text
25
```

nếu không xác định đó là `25%` hay `25 đơn vị`.

---

# 12. DATA QUALITY

Mỗi record quan trọng phải kiểm tra:

```text
[ ] Có ID
[ ] ID duy nhất
[ ] Đúng Entity
[ ] Đủ Required Fields
[ ] Đúng Data Type
[ ] Đúng Unit
[ ] Relation hợp lệ
[ ] Có Source
[ ] Có Timestamp
[ ] Có Owner
[ ] Không Duplicate
```

---

# 13. AI AGENT — QUY TẮC BẮT BUỘC

AI Agent phải:

```text
READ
 ↓
IDENTIFY
 ↓
VALIDATE
 ↓
RELATE
 ↓
ANALYZE
 ↓
RESPOND
```

Không được:

```text
READ
 ↓
GUESS
 ↓
WRITE
```

---

# 14. FACT / INFERENCE / ASSUMPTION

AI phải phân biệt:

| Type         | Ý nghĩa             |
| ------------ | ------------------- |
| `FACT`       | Dữ liệu đã xác nhận |
| `INFERENCE`  | Suy luận từ dữ liệu |
| `ASSUMPTION` | Giả định            |
| `UNKNOWN`    | Chưa biết           |

Ví dụ:

```text
FACT:
Công trình chậm 3 ngày.

INFERENCE:
Có thể liên quan đến vật tư.

ASSUMPTION:
Nhà cung cấp giao hàng trễ.

UNKNOWN:
Chưa có biên bản xác nhận nguyên nhân.
```

Không được biến `ASSUMPTION` thành `FACT`.

---

# 15. QUY TRÌNH AI TRUY XUẤT DỮ LIỆU

Khi nhận câu hỏi:

> "Tình hình công trình hiện tại?"

AI phải thực hiện:

```text
1. Xác định Project
2. Xác định Site
3. Kiểm tra Progress
4. Kiểm tra Quality
5. Kiểm tra Safety
6. Kiểm tra Cost
7. Kiểm tra Open Issues
8. Kiểm tra Evidence mới nhất
9. Xác định dữ liệu thiếu
10. Đưa ra kết luận
```

---

# 16. QUY TRÌNH CREATE DATA

Trước khi tạo record:

```text
CHECK ENTITY
      ↓
CHECK ID
      ↓
CHECK DUPLICATE
      ↓
CHECK REQUIRED FIELD
      ↓
CHECK RELATION
      ↓
CHECK PERMISSION
      ↓
CREATE
      ↓
AUDIT LOG
```

---

# 17. QUY TRÌNH UPDATE DATA

```text
IDENTIFY RECORD
      ↓
CHECK PERMISSION
      ↓
READ CURRENT VALUE
      ↓
CHANGE
      ↓
SAVE OLD VALUE
      ↓
SAVE NEW VALUE
      ↓
RECORD USER
      ↓
RECORD TIME
      ↓
RECORD REASON
```

---

# 18. QUY TẮC DELETE

Dữ liệu nghiệp vụ quan trọng không được xóa tùy tiện.

Ưu tiên:

```text
ARCHIVED
SUPERSEDED
CANCELLED
INACTIVE
```

thay cho:

```text
DELETE
```

---

# 19. VERSION CONTROL

Dữ liệu/tài liệu quan trọng phải có:

```text
version
created_at
updated_at
updated_by
change_reason
previous_version
```

Mục tiêu:

> Có thể truy lại lịch sử thay đổi.

---

# 20. DATA GOVERNANCE

### CEO

Quyết định cuối cùng về chính sách dữ liệu.

### System Administrator

Quản trị hệ thống và quyền.

### Data Owner

Chịu trách nhiệm về dữ liệu thuộc phạm vi quản lý.

### Data Steward

Kiểm soát chất lượng và chuẩn hóa.

### User

Nhập và sử dụng dữ liệu theo quy trình.

### AI Agent

Phân tích và hỗ trợ quyết định theo quyền được cấp.

---

# 21. AI KHÔNG ĐƯỢC TỰ ĐỘNG

AI không mặc nhiên được:

* Xóa dữ liệu.
* Sửa dữ liệu tài chính.
* Sửa dữ liệu pháp lý.
* Phê duyệt hợp đồng.
* Phê duyệt nghiệm thu.
* Thay đổi KPI chính thức.
* Thay đổi ID.
* Xác nhận một thông tin chưa có bằng chứng.

AI có thể:

* Phát hiện lỗi.
* Phát hiện trùng.
* Đề xuất sửa.
* Phân tích.
* Cảnh báo.
* Tạo draft.
* Yêu cầu người có thẩm quyền xác nhận.

---

# 22. KHI DỮ LIỆU MÂU THUẪN

AI không được tự chọn một giá trị mà không giải thích.

Phải:

```text
1. Xác định các nguồn.
2. Xác định thời gian.
3. Xác định phiên bản.
4. Xác định mức độ tin cậy.
5. Áp dụng Source Priority.
6. Báo cáo mâu thuẫn.
```

Nếu vẫn không thể xác định:

> **CONFLICT — CHƯA ĐỦ CƠ SỞ XÁC ĐỊNH GIÁ TRỊ ĐÚNG**

---

# 23. KHI DỮ LIỆU THIẾU

AI phải trả lời theo cấu trúc:

```text
Dữ liệu đã có:
...

Dữ liệu còn thiếu:
...

Ảnh hưởng:
...

Đề nghị bổ sung:
...
```

Không được tự điền dữ liệu còn thiếu.

---

# 24. DATA → SOP → EVIDENCE

KVA Enterprise không quản trị bằng dữ liệu đơn thuần.

Chuỗi vận hành chuẩn:

```text
DATA
 ↓
SOP
 ↓
TASK
 ↓
EXECUTION
 ↓
EVIDENCE
 ↓
QC
 ↓
APPROVAL
 ↓
REPORT
 ↓
DASHBOARD
 ↓
DECISION
```

Đây là nguyên tắc kết nối giữa:

* Data Standards.
* SOP.
* Project Management.
* Construction Management.
* Dashboard.
* AI Agent.

---

# 25. CẤU TRÚC AI AGENT

AI Agent khi làm việc với dữ liệu phải đọc theo thứ tự:

```text
00_System/
      ↓
02_Data_Standards/
      ↓
03_Projects/
      ↓
04_SOP/
      ↓
Evidence
      ↓
Analysis
```

Không được bỏ qua Data Standards khi xử lý dữ liệu doanh nghiệp.

---

# 26. CHECKLIST TRƯỚC KHI BAN HÀNH DATA

```text
- [ ] Entity đã được định nghĩa
- [ ] ID đã được định nghĩa
- [ ] Field đã được định nghĩa
- [ ] Data Type đã được xác định
- [ ] Required Field đã được xác định
- [ ] Unit đã được xác định
- [ ] Status đã được xác định
- [ ] Relation đã được xác định
- [ ] Source đã được xác định
- [ ] Owner đã được xác định
- [ ] Quyền truy cập đã được xác định
- [ ] Quy tắc AI đã được xác định
- [ ] Version đã được ghi nhận
```

---

# 27. FILE LIÊN QUAN

```text
00_System/
├── AI_Constitution.md
├── RULES.md
├── Workflow.md
├── Security_Policy.md
└── Naming_Convention.md

02_Data_Standards/
├── README.md
├── Data_Dictionary.md
└── ID_Convention.md

04_SOP/
05_AI/
01_Dashboard/
03_Projects/
```

---

# 28. QUY TẮC CUỐI CÙNG

> **Nếu dữ liệu không có định nghĩa → không sử dụng như dữ liệu chuẩn.**

> **Nếu dữ liệu không có nguồn → không coi là FACT.**

> **Nếu dữ liệu không có ID → không coi là entity chính thức.**

> **Nếu dữ liệu mâu thuẫn → không tự chọn nếu chưa đủ căn cứ.**

> **Nếu dữ liệu thiếu → báo thiếu, không bịa.**

> **Nếu AI không chắc chắn → phải nói rõ mức độ chắc chắn.**

---

# 29. SUCCESS CRITERIA

`02_Data_Standards/` được xem là hoạt động tốt khi:

```text
Human
  ↓
hiểu dữ liệu

AI Agent
  ↓
hiểu dữ liệu

Dashboard
  ↓
đọc cùng dữ liệu

SOP
  ↓
tạo cùng chuẩn dữ liệu

Database
  ↓
lưu đúng cấu trúc

CEO
  ↓
nhận được báo cáo đáng tin cậy
```

Mục tiêu cuối cùng:

> **ONE COMPANY — ONE DATA LANGUAGE — ONE SOURCE OF TRUTH**

---

**Document Owner:** KVA Enterprise
**Version:** 1.0
**Status:** ACTIVE
**Last Updated:** 2026-08-19

## END OF DOCUMENT
