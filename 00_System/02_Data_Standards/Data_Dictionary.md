# DATA DICTIONARY

## KVA Enterprise Data Standards

**Version:** 1.0
**Status:** Active
**Owner:** CEO / System Administrator
**Scope:** Toàn bộ dữ liệu vận hành KVA Enterprise
**Applies to:** Human Users · AI Agents · Dashboard · Workflow · SOP · Database · GitHub

---

# 1. MỤC ĐÍCH

`Data_Dictionary.md` là từ điển dữ liệu chuẩn của KVA Enterprise.

Tài liệu này quy định:

* Dữ liệu nào được phép tồn tại trong hệ thống.
* Ý nghĩa chính xác của từng trường dữ liệu.
* Kiểu dữ liệu.
* Đơn vị đo.
* Giá trị được phép.
* Quan hệ giữa các đối tượng.
* Nguồn dữ liệu.
* Quyền tạo và cập nhật.
* Quy tắc để AI Agent đọc, ghi và suy luận dữ liệu.

### Nguyên tắc cốt lõi

> **Một dữ liệu — một định nghĩa — một ID — một nguồn sự thật chính.**

AI Agent không được tự tạo dữ liệu nếu dữ liệu nguồn chưa tồn tại.

Nếu thiếu dữ liệu:

> `KHÔNG ĐỦ DỮ LIỆU KẾT LUẬN`

---

# 2. THỨ TỰ ƯU TIÊN NGUỒN DỮ LIỆU

Khi có mâu thuẫn giữa các nguồn, áp dụng thứ tự:

1. Dữ liệu người dùng xác nhận trực tiếp.
2. Dữ liệu chính thức trong Repository.
3. SOP đã ban hành.
4. Checklist / Biên bản nghiệm thu.
5. Database / hệ thống nghiệp vụ.
6. Hồ sơ dự án.
7. Tiêu chuẩn kỹ thuật.
8. Văn bản pháp luật.
9. Web / nguồn bên ngoài.
10. Kiến thức nền của AI.

AI không được lấy nguồn có độ ưu tiên thấp để phủ nhận nguồn có độ ưu tiên cao hơn.

---

# 3. KIỂU DỮ LIỆU CHUẨN

| Type          | Ý nghĩa                         |
| ------------- | ------------------------------- |
| `STRING`      | Chuỗi ký tự                     |
| `TEXT`        | Nội dung văn bản dài            |
| `INTEGER`     | Số nguyên                       |
| `DECIMAL`     | Số thập phân                    |
| `BOOLEAN`     | Có / Không                      |
| `DATE`        | Ngày `YYYY-MM-DD`               |
| `DATETIME`    | Ngày + giờ                      |
| `ENUM`        | Giá trị thuộc danh sách cố định |
| `ID`          | Mã định danh duy nhất           |
| `CURRENCY`    | Giá trị tiền tệ                 |
| `PERCENT`     | Tỷ lệ phần trăm                 |
| `URL`         | Đường dẫn tài nguyên            |
| `FILE_REF`    | Tham chiếu file                 |
| `IMAGE_REF`   | Tham chiếu hình ảnh             |
| `USER_ID`     | ID người dùng                   |
| `RELATION_ID` | ID liên kết đối tượng           |

---

# 4. NGUYÊN TẮC ID

Mọi đối tượng nghiệp vụ phải có ID duy nhất.

Ví dụ:

```text
CUS-000001
PROJ-2026-0001
SITE-2026-0001
CON-2026-0001
TASK-2026-000001
DOC-2026-000001
IMG-2026-000001
PAY-2026-000001
```

Không sử dụng:

* Tên khách hàng làm ID.
* Tên công trình làm ID.
* Số điện thoại làm ID.
* Địa chỉ làm ID.
* ID tự phát sinh bởi AI.

Chi tiết xem:

`02_Data_Standards/ID_Convention.md`

---

# 5. CUSTOMER — KHÁCH HÀNG

## Entity

`Customer`

## ID

`customer_id`

## Mục đích

Lưu thông tin khách hàng và lịch sử quan hệ với doanh nghiệp.

| Field            | Type     | Required | Description                                         |
| ---------------- | -------- | -------: | --------------------------------------------------- |
| `customer_id`    | ID       |      YES | ID duy nhất của khách hàng                          |
| `customer_name`  | STRING   |      YES | Tên khách hàng                                      |
| `customer_type`  | ENUM     |      YES | Cá nhân / doanh nghiệp                              |
| `phone`          | STRING   |       NO | Số điện thoại                                       |
| `email`          | STRING   |       NO | Email                                               |
| `address`        | TEXT     |       NO | Địa chỉ                                             |
| `source_id`      | ID       |       NO | Nguồn khách hàng                                    |
| `sales_owner_id` | USER_ID  |       NO | Nhân sự phụ trách                                   |
| `status`         | ENUM     |      YES | Lead / Qualified / Proposal / Won / Lost / Customer |
| `created_at`     | DATETIME |      YES | Thời điểm tạo                                       |
| `updated_at`     | DATETIME |      YES | Thời điểm cập nhật                                  |

### Quy tắc

AI không được tạo khách hàng mới nếu phát hiện thông tin có khả năng trùng.

Phải kiểm tra tối thiểu:

* Số điện thoại.
* Email.
* Tên.
* Dự án liên quan.

---

# 6. PROJECT — DỰ ÁN

## Entity

`Project`

## ID

`project_id`

Một khách hàng có thể có nhiều dự án.

| Field                | Type        | Required | Description                                          |
| -------------------- | ----------- | -------: | ---------------------------------------------------- |
| `project_id`         | ID          |      YES | ID dự án                                             |
| `customer_id`        | RELATION_ID |      YES | Khách hàng sở hữu                                    |
| `project_name`       | STRING      |      YES | Tên dự án                                            |
| `project_type`       | ENUM        |      YES | Nhà phố / Villa / Biệt thự / Khác                    |
| `location`           | TEXT        |      YES | Vị trí dự án                                         |
| `design_scope`       | ENUM        |       NO | Thiết kế / Thi công / Trọn gói                       |
| `project_manager_id` | USER_ID     |       NO | PM phụ trách                                         |
| `designer_id`        | USER_ID     |       NO | Người phụ trách thiết kế                             |
| `status`             | ENUM        |      YES | Lead / Design / Construction / Completed / Cancelled |
| `start_date`         | DATE        |       NO | Ngày bắt đầu                                         |
| `planned_end_date`   | DATE        |       NO | Ngày kết thúc kế hoạch                               |
| `actual_end_date`    | DATE        |       NO | Ngày kết thúc thực tế                                |

---

# 7. SITE — CÔNG TRÌNH

## Entity

`ConstructionSite`

## ID

`site_id`

Dùng để quản lý thực tế tại hiện trường.

| Field                 | Type        | Required |
| --------------------- | ----------- | -------: |
| `site_id`             | ID          |      YES |
| `project_id`          | RELATION_ID |      YES |
| `site_name`           | STRING      |      YES |
| `site_address`        | TEXT        |      YES |
| `site_manager_id`     | USER_ID     |       NO |
| `supervisor_id`       | USER_ID     |       NO |
| `team_leader_id`      | USER_ID     |       NO |
| `construction_status` | ENUM        |      YES |
| `safety_status`       | ENUM        |      YES |
| `quality_status`      | ENUM        |      YES |
| `progress_status`     | ENUM        |      YES |

### 4 trạng thái bắt buộc

```text
PROGRESS
QUALITY
SAFETY
COST
```

AI Agent khi báo cáo công trình phải ưu tiên kiểm tra đủ 4 nhóm này.

---

# 8. CONTRACT — HỢP ĐỒNG

## Entity

`Contract`

## ID

`contract_id`

| Field            | Type        | Required |
| ---------------- | ----------- | -------: |
| `contract_id`    | ID          |      YES |
| `customer_id`    | RELATION_ID |      YES |
| `project_id`     | RELATION_ID |      YES |
| `contract_type`  | ENUM        |      YES |
| `contract_value` | CURRENCY    |      YES |
| `currency`       | STRING      |      YES |
| `sign_date`      | DATE        |       NO |
| `start_date`     | DATE        |       NO |
| `end_date`       | DATE        |       NO |
| `payment_terms`  | TEXT        |       NO |
| `status`         | ENUM        |      YES |
| `document_ref`   | FILE_REF    |       NO |

---

# 9. TASK — CÔNG VIỆC

## Entity

`Task`

## ID

`task_id`

| Field           | Type        | Required |
| --------------- | ----------- | -------: |
| `task_id`       | ID          |      YES |
| `project_id`    | RELATION_ID |      YES |
| `task_name`     | STRING      |      YES |
| `description`   | TEXT        |       NO |
| `owner_id`      | USER_ID     |      YES |
| `priority`      | ENUM        |      YES |
| `status`        | ENUM        |      YES |
| `planned_start` | DATE        |       NO |
| `planned_end`   | DATE        |       NO |
| `actual_start`  | DATE        |       NO |
| `actual_end`    | DATE        |       NO |
| `dependency_id` | RELATION_ID |       NO |
| `evidence_ref`  | FILE_REF    |       NO |

### Status chuẩn

```text
TODO
IN_PROGRESS
BLOCKED
WAITING_APPROVAL
DONE
CANCELLED
```

---

# 10. DOCUMENT — HỒ SƠ

## Entity

`Document`

## ID

`document_id`

| Field           | Type        | Required |
| --------------- | ----------- | -------: |
| `document_id`   | ID          |      YES |
| `project_id`    | RELATION_ID |       NO |
| `document_type` | ENUM        |      YES |
| `document_name` | STRING      |      YES |
| `version`       | STRING      |      YES |
| `status`        | ENUM        |      YES |
| `owner_id`      | USER_ID     |      YES |
| `file_ref`      | FILE_REF    |      YES |
| `created_at`    | DATETIME    |      YES |
| `approved_at`   | DATETIME    |       NO |

### Document Status

```text
DRAFT
REVIEW
APPROVED
SUPERSEDED
ARCHIVED
```

AI không được sử dụng tài liệu `SUPERSEDED` hoặc `ARCHIVED` làm nguồn chính nếu đã có phiên bản `APPROVED` mới hơn.

---

# 11. IMAGE — HÌNH ẢNH

## Entity

`Image`

## ID

`image_id`

Hình ảnh thi công là **evidence**, không chỉ là file lưu trữ.

| Field                 | Type        | Required |
| --------------------- | ----------- | -------: |
| `image_id`            | ID          |      YES |
| `project_id`          | RELATION_ID |      YES |
| `site_id`             | RELATION_ID |       NO |
| `task_id`             | RELATION_ID |       NO |
| `capture_date`        | DATE        |      YES |
| `capture_time`        | DATETIME    |       NO |
| `location`            | STRING      |       NO |
| `category`            | ENUM        |      YES |
| `captured_by`         | USER_ID     |      YES |
| `description`         | TEXT        |       NO |
| `file_ref`            | IMAGE_REF   |      YES |
| `verification_status` | ENUM        |      YES |

### Category

```text
BEFORE
PROGRESS
AFTER
QC
SAFETY
ISSUE
MATERIAL
EQUIPMENT
HANDOVER
```

---

# 12. ISSUE — VẤN ĐỀ / PHÁT SINH

## Entity

`Issue`

## ID

`issue_id`

| Field               | Type        | Required |
| ------------------- | ----------- | -------: |
| `issue_id`          | ID          |      YES |
| `project_id`        | RELATION_ID |      YES |
| `site_id`           | RELATION_ID |       NO |
| `issue_type`        | ENUM        |      YES |
| `severity`          | ENUM        |      YES |
| `description`       | TEXT        |      YES |
| `reported_by`       | USER_ID     |      YES |
| `reported_at`       | DATETIME    |      YES |
| `owner_id`          | USER_ID     |       NO |
| `due_date`          | DATE        |       NO |
| `root_cause`        | TEXT        |       NO |
| `corrective_action` | TEXT        |       NO |
| `status`            | ENUM        |      YES |
| `evidence_ref`      | FILE_REF    |       NO |

### Severity

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### Status

```text
OPEN
INVESTIGATING
ACTION_REQUIRED
RESOLVED
VERIFIED
CLOSED
```

---

# 13. COST — CHI PHÍ

## Entity

`Cost`

## ID

`cost_id`

| Field              | Type        | Required |
| ------------------ | ----------- | -------: |
| `cost_id`          | ID          |      YES |
| `project_id`       | RELATION_ID |      YES |
| `cost_category`    | ENUM        |      YES |
| `description`      | TEXT        |      YES |
| `amount`           | CURRENCY    |      YES |
| `currency`         | STRING      |      YES |
| `transaction_date` | DATE        |      YES |
| `supplier_id`      | RELATION_ID |       NO |
| `document_ref`     | FILE_REF    |       NO |
| `approved_by`      | USER_ID     |       NO |
| `status`           | ENUM        |      YES |

AI không được suy đoán chi phí nếu không có chứng từ hoặc dữ liệu nguồn.

---

# 14. PAYMENT — THANH TOÁN

## Entity

`Payment`

## ID

`payment_id`

| Field          | Type        | Required |
| -------------- | ----------- | -------: |
| `payment_id`   | ID          |      YES |
| `project_id`   | RELATION_ID |      YES |
| `contract_id`  | RELATION_ID |       NO |
| `payment_type` | ENUM        |      YES |
| `amount`       | CURRENCY    |      YES |
| `due_date`     | DATE        |       NO |
| `paid_date`    | DATE        |       NO |
| `status`       | ENUM        |      YES |
| `document_ref` | FILE_REF    |       NO |

---

# 15. KPI — CHỈ SỐ

## Entity

`KPI`

## ID

`kpi_id`

Mỗi KPI bắt buộc phải có:

```text
KPI_ID
Tên KPI
Định nghĩa
Công thức
Đơn vị
Mục tiêu
Kỳ đo
Nguồn dữ liệu
Owner
Ngày cập nhật
```

### Nguyên tắc

Không được có KPI chỉ có con số mà không có:

* Đơn vị.
* Thời gian.
* Nguồn.
* Công thức.

---

# 16. REPORT — BÁO CÁO

## Entity

`Report`

## ID

`report_id`

| Field          | Type        | Required |
| -------------- | ----------- | -------: |
| `report_id`    | ID          |      YES |
| `report_type`  | ENUM        |      YES |
| `project_id`   | RELATION_ID |       NO |
| `period_start` | DATE        |      YES |
| `period_end`   | DATE        |      YES |
| `created_by`   | USER_ID     |      YES |
| `status`       | ENUM        |      YES |
| `source_refs`  | FILE_REF    |      YES |
| `created_at`   | DATETIME    |      YES |

---

# 17. USER — NHÂN SỰ

## Entity

`User`

## ID

`user_id`

| Field           | Type    | Required |
| --------------- | ------- | -------: |
| `user_id`       | ID      |      YES |
| `full_name`     | STRING  |      YES |
| `role_id`       | ID      |      YES |
| `department_id` | ID      |       NO |
| `status`        | ENUM    |      YES |
| `manager_id`    | USER_ID |       NO |

---

# 18. ROLE — VAI TRÒ

## Entity

`Role`

## ID

`role_id`

Ví dụ:

```text
CEO
COO
CFO
PM
DESIGNER
SUPERVISOR
TEAM_LEADER
SALES
MARKETING
ACCOUNTANT
ADMIN
AI_AGENT
```

Role xác định:

* Quyền xem.
* Quyền tạo.
* Quyền sửa.
* Quyền phê duyệt.
* Quyền xóa.

---

# 19. RELATIONSHIP MODEL

Quan hệ dữ liệu cốt lõi:

```text
CUSTOMER
   │
   └── PROJECT
          │
          ├── CONTRACT
          │
          ├── SITE
          │     ├── TASK
          │     ├── ISSUE
          │     └── IMAGE
          │
          ├── DOCUMENT
          │
          ├── COST
          │
          ├── PAYMENT
          │
          └── REPORT
```

Đây là cấu trúc quan trọng để AI Agent truy xuất dữ liệu.

Ví dụ:

```text
Customer
   ↓
Project
   ↓
Construction Site
   ↓
Task
   ↓
Issue
   ↓
Image Evidence
   ↓
Corrective Action
   ↓
Verification
   ↓
Report
```

---

# 20. DATA LINEAGE

Mỗi dữ liệu quan trọng phải truy được:

```text
DATA
 ↓
SOURCE
 ↓
CREATOR
 ↓
CREATED_AT
 ↓
UPDATED_AT
 ↓
APPROVER
 ↓
EVIDENCE
```

AI phải có khả năng trả lời:

> Dữ liệu này lấy từ đâu?

Nếu không xác định được nguồn:

> `SOURCE_NOT_VERIFIED`

---

# 21. QUY TẮC AI AGENT

AI Agent phải tuân thủ 10 nguyên tắc:

### Rule 01 — Không bịa dữ liệu

Không có dữ liệu → không được tự tạo.

### Rule 02 — Không đổi ID

ID hiện hữu phải được giữ nguyên.

### Rule 03 — Không tạo bản ghi trùng

Phải kiểm tra dữ liệu tồn tại trước khi tạo.

### Rule 04 — Không ghi đè dữ liệu quan trọng

Phải tạo version hoặc yêu cầu phê duyệt.

### Rule 05 — Không suy luận thành sự thật

Phân biệt:

```text
FACT
INFERENCE
ASSUMPTION
UNKNOWN
```

### Rule 06 — Luôn giữ nguồn

Mỗi kết luận quan trọng phải truy được về nguồn.

### Rule 07 — Không dùng tài liệu hết hiệu lực

Ưu tiên phiên bản mới nhất đã được phê duyệt.

### Rule 08 — Không tự thay đổi trạng thái

Các trạng thái quan trọng phải dựa trên dữ liệu hoặc quyền được cấp.

### Rule 09 — Không tự phê duyệt

AI có thể đề xuất nhưng không thay thế người có thẩm quyền.

### Rule 10 — Không đủ dữ liệu thì dừng

AI phải báo rõ dữ liệu còn thiếu.

---

# 22. FACT / INFERENCE / ASSUMPTION

AI phải phân loại thông tin:

| Type         | Ý nghĩa                |
| ------------ | ---------------------- |
| `FACT`       | Có bằng chứng xác nhận |
| `INFERENCE`  | Suy luận từ dữ liệu    |
| `ASSUMPTION` | Giả định cần xác nhận  |
| `UNKNOWN`    | Chưa có dữ liệu        |

Ví dụ:

```text
FACT:
Công trình chậm 3 ngày theo bảng tiến độ.

INFERENCE:
Nguyên nhân có khả năng liên quan đến việc chậm vật tư.

ASSUMPTION:
Giả định nhà cung cấp giao hàng chậm.

UNKNOWN:
Chưa có biên bản xác nhận nguyên nhân.
```

AI không được biến `INFERENCE` hoặc `ASSUMPTION` thành `FACT`.

---

# 23. DATA STATUS

Mọi dữ liệu nghiệp vụ quan trọng nên có trạng thái:

```text
DRAFT
ACTIVE
PENDING_REVIEW
APPROVED
REJECTED
SUPERSEDED
ARCHIVED
```

---

# 24. VERSION CONTROL

Tài liệu và dữ liệu có thay đổi quan trọng phải lưu:

```text
version
created_at
updated_at
updated_by
change_reason
previous_version
```

Không xóa lịch sử nếu dữ liệu có giá trị quản trị, pháp lý hoặc tài chính.

---

# 25. REQUIRED EVIDENCE

Các nhóm dữ liệu sau nên có bằng chứng:

| Data       | Evidence                  |
| ---------- | ------------------------- |
| Tiến độ    | Schedule / Photo / Report |
| Chất lượng | QC / Checklist / Photo    |
| An toàn    | Safety Checklist / Photo  |
| Chi phí    | Invoice / Voucher         |
| Thanh toán | Payment Evidence          |
| Phát sinh  | Issue Record / Photo      |
| Nghiệm thu | Acceptance Record         |
| Bàn giao   | Handover Record           |

---

# 26. QUY TẮC TRUY VẤN AI

Khi người dùng hỏi:

> "Công trình hiện tại thế nào?"

AI không được trả lời chung chung.

Phải truy vấn tối thiểu:

```text
PROJECT
→ PROGRESS
→ QUALITY
→ SAFETY
→ COST
→ OPEN ISSUES
→ LATEST EVIDENCE
```

Kết quả phải phân biệt:

```text
Đã xác nhận
Chưa xác nhận
Đang xử lý
Có rủi ro
Thiếu dữ liệu
```

---

# 27. QUY TẮC TẠO DỮ LIỆU

Trước khi CREATE:

```text
1. Kiểm tra entity.
2. Kiểm tra ID.
3. Kiểm tra duplicate.
4. Kiểm tra required fields.
5. Kiểm tra relation.
6. Kiểm tra permission.
7. Tạo record.
8. Ghi audit log.
```

---

# 28. QUY TẮC UPDATE

Trước khi UPDATE:

```text
1. Xác định record.
2. Kiểm tra quyền.
3. Xác định field thay đổi.
4. Lưu giá trị cũ.
5. Ghi giá trị mới.
6. Ghi người thay đổi.
7. Ghi thời gian.
8. Ghi lý do.
```

---

# 29. QUY TẮC DELETE

AI Agent mặc định:

> **KHÔNG ĐƯỢC DELETE dữ liệu nghiệp vụ quan trọng.**

Ưu tiên:

```text
ARCHIVE
INACTIVE
SUPERSEDED
CANCELLED
```

thay cho xóa vật lý.

---

# 30. DATA QUALITY CHECK

Mỗi record phải kiểm tra:

```text
[ ] Có ID
[ ] ID duy nhất
[ ] Đúng entity
[ ] Đủ trường bắt buộc
[ ] Đúng kiểu dữ liệu
[ ] Đúng đơn vị
[ ] Quan hệ hợp lệ
[ ] Có nguồn nếu cần
[ ] Có timestamp
[ ] Có owner
[ ] Không trùng
```

---

# 31. AI RESPONSE STANDARD

Khi trả lời dữ liệu doanh nghiệp, AI nên sử dụng cấu trúc:

```text
KẾT LUẬN
DỮ LIỆU XÁC NHẬN
DỮ LIỆU CÒN THIẾU
RỦI RO
HÀNH ĐỘNG ĐỀ XUẤT
NGUỒN DỮ LIỆU
```

Không được trình bày suy luận như dữ liệu chính thức.

---

# 32. DATA GOVERNANCE

## Data Owner

Người chịu trách nhiệm cuối cùng về tính đúng của dữ liệu.

## Data Steward

Người kiểm soát chất lượng và chuẩn hóa dữ liệu.

## Data User

Người sử dụng dữ liệu.

## AI Agent

Được phép:

* Đọc dữ liệu theo quyền.
* Phân tích.
* Đối chiếu.
* Phát hiện thiếu dữ liệu.
* Phát hiện bất thường.
* Đề xuất hành động.

AI Agent không mặc nhiên được:

* Xóa dữ liệu.
* Phê duyệt.
* Thay đổi dữ liệu pháp lý.
* Thay đổi dữ liệu tài chính.
* Thay đổi dữ liệu nhân sự quan trọng.

---

# 33. MỤC TIÊU CUỐI CÙNG

KVA Enterprise phải hình thành chuỗi:

```text
DATA
 ↓
STANDARD
 ↓
PROCESS
 ↓
EVIDENCE
 ↓
ANALYSIS
 ↓
DECISION
 ↓
ACTION
 ↓
RESULT
 ↓
LEARNING
```

Trong đó:

> **Data là nền móng.
> SOP là cách làm.
> Evidence là bằng chứng.
> AI là lớp phân tích và hỗ trợ quyết định.
> Con người giữ quyền quyết định cuối cùng.**

---

# 34. LIÊN KẾT HỆ THỐNG

Tài liệu này liên kết với:

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

03_Projects/
04_SOP/
05_AI/
01_Dashboard/
```

---

# 35. VERSION HISTORY

| Version | Date       | Change                             | Owner        |
| ------- | ---------- | ---------------------------------- | ------------ |
| 1.0     | 2026-08-19 | Initial Enterprise Data Dictionary | System Owner |

---

## END OF DOCUMENT
