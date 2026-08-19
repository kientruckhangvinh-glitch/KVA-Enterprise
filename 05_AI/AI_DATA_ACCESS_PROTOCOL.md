# AI DATA ACCESS PROTOCOL

**System:** KVA Enterprise
**Version:** 1.0
**Status:** ACTIVE
**Owner:** CEO / System Administrator
**Path:** `05_AI/AI_DATA_ACCESS_PROTOCOL.md`
**Applies to:** All AI Agents operating on KVA Enterprise data

---

# 1. MỤC ĐÍCH

`AI_DATA_ACCESS_PROTOCOL.md` quy định cách AI Agent:

* Truy cập dữ liệu trên GitHub.
* Xác định dữ liệu cần đọc.
* Hiểu quan hệ giữa các Entity.
* Kiểm tra nguồn dữ liệu.
* Kiểm tra phiên bản.
* Kiểm tra bằng chứng.
* Phân tích dữ liệu.
* Trả lời người dùng.
* Tạo hoặc đề xuất thay đổi dữ liệu.
* Ghi nhận nguồn và lịch sử thay đổi.

Mục tiêu:

> **AI Agent phải sử dụng GitHub như một nguồn dữ liệu doanh nghiệp có cấu trúc, không phải đơn thuần là một kho file.**

---

# 2. NGUYÊN TẮC CỐT LÕI

## Rule 01 — DATA FIRST

AI phải ưu tiên dữ liệu thực tế trong Repository trước kiến thức nền của AI.

```text
User Confirmed
      ↓
Official Repository
      ↓
Approved SOP
      ↓
Evidence
      ↓
Database
      ↓
External Sources
      ↓
AI Knowledge
```

---

## Rule 02 — NO GUESSING

Nếu dữ liệu không tồn tại:

> `KHÔNG ĐỦ DỮ LIỆU KẾT LUẬN`

Không được tự tạo số liệu, trạng thái, ngày tháng, chi phí hoặc tiến độ.

---

## Rule 03 — SOURCE REQUIRED

Mọi kết luận quan trọng phải có nguồn.

AI phải có khả năng trả lời:

> "Thông tin này lấy từ đâu?"

Nếu không xác định được:

> `SOURCE_NOT_VERIFIED`

---

## Rule 04 — ID FIRST

AI phải xác định ID trước khi xử lý Entity.

Không được chỉ dựa vào tên.

Ví dụ:

```text
Nguyễn Văn A
        ↓
Search Customer
        ↓
CUS-2026-000018
        ↓
Find Projects
        ↓
PROJ-2026-000007
```

---

## Rule 05 — RELATION FIRST

AI phải hiểu quan hệ dữ liệu trước khi kết luận.

```text
CUSTOMER
   ↓
PROJECT
   ↓
SITE
   ↓
TASK
   ↓
ISSUE
   ↓
EVIDENCE
```

---

# 3. KIẾN TRÚC TRUY CẬP

```text
                         USER
                           │
                           ↓
                     AI AGENT
                           │
                           ↓
              ┌──────────────────────┐
              │ ACCESS PROTOCOL      │
              ├──────────────────────┤
              │ Identity             │
              │ Permission           │
              │ Data Standard        │
              │ Source Priority      │
              │ Version Control      │
              │ Evidence             │
              └──────────┬───────────┘
                         ↓
                     GITHUB
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
   System Rules      Data Standards     Business Data
        │                │                │
        ↓                ↓                ↓
    00_System      02_Data_Standards    03_Projects
                                          04_SOP
                                          06_Data
                                          07_Evidence
```

---

# 4. CẤU TRÚC REPOSITORY AI PHẢI HIỂU

```text
KVA-Enterprise/
│
├── 00_System/
│
├── 01_Dashboard/
│
├── 02_Data_Standards/
│
├── 03_Projects/
│
├── 04_SOP/
│
├── 05_AI/
│
├── 06_Data/
│
└── 07_Evidence/
```

## Ý nghĩa

### `00_System/`

Luật hệ thống.

### `01_Dashboard/`

Thông tin quản trị và báo cáo.

### `02_Data_Standards/`

Định nghĩa dữ liệu.

### `03_Projects/`

Hồ sơ dự án.

### `04_SOP/`

Quy trình chuẩn.

### `05_AI/`

AI Agents, Prompt và Policy.

### `06_Data/`

Dữ liệu có cấu trúc.

### `07_Evidence/`

Bằng chứng thực tế.

---

# 5. THỨ TỰ AI PHẢI ĐỌC

Khi Agent bắt đầu một nhiệm vụ mới:

```text
STEP 01
00_System
        ↓
STEP 02
02_Data_Standards
        ↓
STEP 03
05_AI
        ↓
STEP 04
Relevant Project
        ↓
STEP 05
Relevant SOP
        ↓
STEP 06
Structured Data
        ↓
STEP 07
Evidence
        ↓
STEP 08
Analysis
```

Không được bỏ qua:

`00_System`

hoặc

`02_Data_Standards`

khi xử lý dữ liệu doanh nghiệp quan trọng.

---

# 6. ACCESS FLOW

Mọi yêu cầu phải đi qua:

```text
USER REQUEST
     ↓
IDENTIFY INTENT
     ↓
IDENTIFY ENTITY
     ↓
IDENTIFY ENTITY ID
     ↓
CHECK PERMISSION
     ↓
LOAD DATA STANDARD
     ↓
SEARCH GITHUB
     ↓
LOAD RELATED RECORDS
     ↓
CHECK VERSION
     ↓
CHECK SOURCE
     ↓
CHECK EVIDENCE
     ↓
VALIDATE
     ↓
ANALYZE
     ↓
RESPOND
```

---

# 7. IDENTIFY INTENT

AI phải xác định người dùng đang yêu cầu:

```text
READ
SEARCH
COMPARE
ANALYZE
REPORT
CREATE
UPDATE
APPROVE
EXPORT
```

Ví dụ:

> "Công trình A hiện tại thế nào?"

Intent:

```text
READ + ANALYZE + REPORT
```

Ví dụ:

> "Tạo issue cho việc giao vật tư trễ."

Intent:

```text
CREATE
```

---

# 8. ENTITY RESOLUTION

AI phải xác định Entity liên quan.

Ví dụ:

```text
"Nhà anh Minh Quận 7"
```

Không được ngay lập tức chọn một Project.

Phải:

```text
Search
 ↓
Customer Candidates
 ↓
Project Candidates
 ↓
Check Location
 ↓
Check ID
 ↓
Resolve Entity
```

Nếu có nhiều kết quả:

> `AMBIGUOUS_ENTITY`

AI phải yêu cầu xác nhận.

---

# 9. ENTITY RELATION TRACING

Khi đã có:

```text
PROJ-2026-000007
```

AI phải có khả năng truy ngược:

```text
PROJ-2026-000007
       ↑
CUS-2026-000018
```

và truy xuôi:

```text
PROJ-2026-000007
       │
       ├── SITE
       ├── TASK
       ├── ISSUE
       ├── DOCUMENT
       ├── IMAGE
       ├── COST
       └── REPORT
```

---

# 10. SEARCH STRATEGY

AI không được chỉ tìm một từ khóa duy nhất.

Thứ tự:

```text
1. Exact ID
2. Entity Name
3. Related ID
4. Structured Data
5. Project Folder
6. SOP
7. Evidence
8. Historical Records
```

Ví dụ:

```text
PROJ-2026-000007
```

→ tìm chính xác ID trước.

---

# 11. SOURCE VALIDATION

Mỗi nguồn phải được kiểm tra:

```text
SOURCE
AUTHOR
CREATED_AT
UPDATED_AT
VERSION
STATUS
APPROVAL
```

Ưu tiên:

```text
APPROVED
```

hơn:

```text
DRAFT
```

Ưu tiên bản mới hơn nếu cùng một loại tài liệu và có trạng thái hợp lệ.

---

# 12. SOURCE PRIORITY

Khi có xung đột:

```text
01. User Confirmed
02. Official Repository
03. Approved SOP
04. Approved Checklist
05. Acceptance Record
06. Structured Data
07. Project Documents
08. Evidence
09. External Sources
10. AI Knowledge
```

Nếu xung đột chưa thể giải quyết:

> `DATA_CONFLICT`

AI phải báo rõ.

---

# 13. VERSION CONTROL

AI phải kiểm tra:

```text
Current Version
Previous Version
Status
Updated Date
Updated By
Change Reason
```

Không sử dụng phiên bản cũ nếu đã có phiên bản mới được phê duyệt.

---

# 14. EVIDENCE VALIDATION

Đối với các kết luận về:

* Tiến độ.
* Chất lượng.
* An toàn.
* Phát sinh.
* Nghiệm thu.
* Bàn giao.
* Chi phí.

AI phải tìm Evidence khi có thể.

Ví dụ:

```text
CLAIM
"Công tác chống thấm đã hoàn thành"
        ↓
TASK
        ↓
QC CHECKLIST
        ↓
INSPECTION RECORD
        ↓
PHOTO
        ↓
VERIFICATION
```

Nếu không có evidence:

> `EVIDENCE_NOT_FOUND`

Không được khẳng định như một FACT nếu bằng chứng bắt buộc chưa có.

---

# 15. FACT / INFERENCE / ASSUMPTION

AI phải phân loại:

```text
FACT
INFERENCE
ASSUMPTION
UNKNOWN
```

Ví dụ:

```text
FACT:
Task đã chuyển trạng thái DONE.

INFERENCE:
Có khả năng hạng mục đã hoàn thành thực tế.

ASSUMPTION:
Đội trưởng đã hoàn thành toàn bộ phần việc.

UNKNOWN:
Chưa có biên bản nghiệm thu.
```

---

# 16. DATA CONFIDENCE

Khi cần, AI phải đánh giá:

```text
HIGH
MEDIUM
LOW
UNKNOWN
```

Ví dụ:

```text
Progress:
HIGH

Reason:
Có schedule + daily report + photo evidence.
```

Không được dùng "100% chắc chắn" nếu không có cơ sở.

---

# 17. READ PROTOCOL

Khi chỉ đọc dữ liệu:

```text
READ REQUEST
     ↓
AUTHENTICATE
     ↓
CHECK PERMISSION
     ↓
IDENTIFY ENTITY
     ↓
SEARCH
     ↓
VALIDATE
     ↓
RETURN DATA
     ↓
SOURCE
```

Read không làm thay đổi Repository.

---

# 18. CREATE PROTOCOL

AI không được tự động ghi thẳng vào dữ liệu chính thức nếu chưa có quyền.

Quy trình:

```text
USER REQUEST
     ↓
VALIDATE INPUT
     ↓
CHECK DUPLICATE
     ↓
CHECK REQUIRED FIELDS
     ↓
CHECK RELATION
     ↓
CREATE DRAFT
     ↓
VALIDATE
     ↓
HUMAN REVIEW
     ↓
APPROVE
     ↓
COMMIT
```

---

# 19. UPDATE PROTOCOL

```text
IDENTIFY RECORD
     ↓
READ CURRENT VALUE
     ↓
CHECK PERMISSION
     ↓
GENERATE CHANGE
     ↓
SHOW DIFF
     ↓
REVIEW
     ↓
APPROVE
     ↓
COMMIT
     ↓
AUDIT LOG
```

AI phải bảo toàn:

```text
Old Value
New Value
Changed By
Changed At
Reason
Version
```

---

# 20. DELETE PROTOCOL

AI mặc định:

> **DENY DELETE**

Đối với dữ liệu nghiệp vụ:

```text
DELETE
```

chỉ được thực hiện khi có policy và quyền rõ ràng.

Ưu tiên:

```text
ARCHIVED
SUPERSEDED
CANCELLED
INACTIVE
```

---

# 21. GIT WORKFLOW

AI phải tuân thủ:

```text
WORKING
   ↓
BRANCH
   ↓
CHANGE
   ↓
VALIDATE
   ↓
COMMIT
   ↓
PULL REQUEST
   ↓
REVIEW
   ↓
MERGE
```

Không tự ý thay đổi `main` nếu policy yêu cầu Pull Request.

---

# 22. COMMIT STANDARD

Commit phải mô tả được:

```text
WHAT
WHY
SCOPE
```

Ví dụ:

```text
data(project): update construction progress for PROJ-2026-000007
```

Không sử dụng:

```text
update
fix
test
new
change
```

nếu không có mô tả đủ nghĩa.

---

# 23. AUDIT TRAIL

Mọi thay đổi quan trọng phải truy được:

```text
WHO
WHAT
WHEN
WHY
OLD
NEW
SOURCE
APPROVAL
```

Ví dụ:

```text
Changed By:
PM-001

Entity:
PROJ-2026-000007

Field:
progress_status

Old:
IN_PROGRESS

New:
BLOCKED

Reason:
Material delay

Evidence:
IMG-2026-001245

Time:
2026-08-19 18:30:00
```

---

# 24. PERMISSION MODEL

AI Agent phải hoạt động theo Role.

```text
ROLE
 ↓
PERMISSION
 ↓
ENTITY
 ↓
ACTION
```

Các Action:

```text
READ
CREATE
UPDATE
APPROVE
ARCHIVE
DELETE
```

Không được suy luận quyền từ tên Agent.

---

# 25. AI AGENT LEVEL

## Level 1 — READ ONLY

Được:

* Tìm kiếm.
* Đọc.
* Phân tích.
* Báo cáo.

Không được:

* Ghi.
* Sửa.
* Xóa.

---

## Level 2 — DRAFT

Được:

* Tạo draft.
* Đề xuất thay đổi.
* Tạo báo cáo nháp.

Không được tự đưa dữ liệu vào trạng thái chính thức.

---

## Level 3 — WRITE

Được:

* Create.
* Update.

Phải tuân thủ permission.

---

## Level 4 — APPROVAL SUPPORT

Được:

* Kiểm tra.
* Đối chiếu.
* Đề xuất approve/reject.

Không thay thế người phê duyệt.

---

# 26. PM AGENT — STANDARD WORKFLOW

PM Agent khi được hỏi:

> "Tình hình công trình?"

Phải kiểm tra:

```text
PROJECT
│
├── Progress
│
├── Quality
│
├── Safety
│
├── Cost
│
├── Issues
│
├── Tasks
│
├── Latest Reports
│
└── Latest Evidence
```

Sau đó trả về:

```text
1. Tình trạng tổng thể
2. Tiến độ
3. Chất lượng
4. An toàn
5. Chi phí
6. Phát sinh
7. Việc quá hạn
8. Rủi ro
9. Việc PM phải xử lý
10. Dữ liệu còn thiếu
```

---

# 27. CEO AGENT — STANDARD WORKFLOW

CEO Agent phải ưu tiên:

```text
PORTFOLIO
   ↓
PROJECT STATUS
   ↓
MONEY
   ↓
RISK
   ↓
PEOPLE
   ↓
CUSTOMER
   ↓
DECISION
```

CEO không cần đọc toàn bộ file.

Agent phải tổng hợp thành:

```text
GREEN
YELLOW
RED
```

và chỉ ra:

> **CEO cần quyết định việc gì?**

---

# 28. CFO AGENT — STANDARD WORKFLOW

CFO Agent phải kiểm tra:

```text
CONTRACT
   ↓
REVENUE
   ↓
PAYMENT
   ↓
RECEIVABLE
   ↓
COST
   ↓
PAYABLE
   ↓
CASH FLOW
   ↓
RISK
```

Không được tự tạo số liệu tài chính.

---

# 29. DESIGN AGENT — STANDARD WORKFLOW

Design Agent:

```text
PROJECT BRIEF
     ↓
CUSTOMER REQUIREMENT
     ↓
SITE DATA
     ↓
DESIGN STANDARD
     ↓
SOP
     ↓
DESIGN DOCUMENT
     ↓
REVIEW
```

Không tự suy đoán kích thước khu đất, pháp lý hoặc yêu cầu khách hàng.

---

# 30. QC AGENT — STANDARD WORKFLOW

QC Agent:

```text
TASK
 ↓
SOP
 ↓
CHECKLIST
 ↓
STANDARD
 ↓
EVIDENCE
 ↓
INSPECTION
 ↓
NONCONFORMITY
 ↓
CORRECTIVE ACTION
 ↓
VERIFICATION
```

---

# 31. RESPONSE PROTOCOL

Khi trả lời câu hỏi nghiệp vụ:

```text
KẾT LUẬN
↓
FACT
↓
EVIDENCE
↓
ANALYSIS
↓
RISK
↓
ACTION
↓
MISSING DATA
↓
SOURCE
```

---

# 32. KHÔNG ĐỦ DỮ LIỆU

Nếu không tìm thấy dữ liệu cần thiết:

```text
STATUS:
INSUFFICIENT_DATA

DỮ LIỆU ĐÃ TÌM:
...

DỮ LIỆU THIẾU:
...

ẢNH HƯỞNG:
...

CẦN BỔ SUNG:
...
```

Không được lấp khoảng trống bằng kiến thức của AI.

---

# 33. DATA CONFLICT

Nếu hai nguồn mâu thuẫn:

```text
STATUS:
DATA_CONFLICT

SOURCE A:
...

SOURCE B:
...

CONFLICT:
...

SOURCE PRIORITY:
...

CONCLUSION:
...
```

Nếu chưa đủ cơ sở:

> **CHƯA ĐỦ CƠ SỞ XÁC ĐỊNH**

---

# 34. AMBIGUOUS ENTITY

Nếu có nhiều đối tượng giống nhau:

```text
STATUS:
AMBIGUOUS_ENTITY

CANDIDATE 01:
...

CANDIDATE 02:
...

CANDIDATE 03:
...
```

AI phải yêu cầu xác nhận thay vì chọn ngẫu nhiên.

---

# 35. SECURITY

AI Agent không được:

* Lộ token.
* Lộ credential.
* Lộ secret.
* Hiển thị private key.
* Sao chép thông tin bảo mật vào commit.
* Ghi mật khẩu vào Repository.
* Đưa dữ liệu nhạy cảm vào prompt không cần thiết.

Secrets phải được quản lý ngoài dữ liệu nghiệp vụ.

---

# 36. FILE ACCESS CONTROL

Không phải Agent nào cũng được đọc toàn bộ Repository.

Mô hình:

```text
AGENT
 ↓
ROLE
 ↓
PERMISSION
 ↓
FOLDER
 ↓
ENTITY
 ↓
FIELD
```

Ví dụ:

```text
CFO Agent
    ↓
06_Data/Finance
    ↓
READ
```

trong khi:

```text
Sales Agent
    ↓
06_Data/Finance
    ↓
LIMITED
```

---

# 37. DATA MINIMIZATION

AI chỉ đọc dữ liệu cần thiết cho nhiệm vụ.

Không được:

```text
Question
   ↓
Read entire repository
```

Mà:

```text
Question
   ↓
Identify Scope
   ↓
Read Required Data
   ↓
Analyze
```

Mục tiêu:

* Giảm sai sót.
* Tăng tốc.
* Giảm rủi ro.
* Giảm exposure dữ liệu.

---

# 38. CACHE / MEMORY

AI không được coi thông tin đã đọc trước đó là dữ liệu mới nhất.

Mỗi lần xử lý nhiệm vụ quan trọng phải kiểm tra:

```text
Last Updated
Version
Current Status
```

Nếu dữ liệu có thể đã thay đổi:

> Re-read current source.

---

# 39. GITHUB AS SOURCE OF TRUTH

GitHub được coi là nguồn chính thức **chỉ đối với dữ liệu đã được đưa vào Repository theo đúng chuẩn và workflow**.

Không mặc định:

> "Có trên GitHub = đúng."

Phải:

```text
GitHub
 ↓
Data Standard
 ↓
Version
 ↓
Status
 ↓
Source
 ↓
Evidence
 ↓
Trust
```

---

# 40. AI DATA ACCESS CHECKLIST

Trước khi trả lời:

```text
- [ ] Xác định đúng User Intent
- [ ] Xác định Entity
- [ ] Xác định Entity ID
- [ ] Kiểm tra Permission
- [ ] Đọc Data Standards
- [ ] Tìm dữ liệu hiện hành
- [ ] Kiểm tra Version
- [ ] Kiểm tra Status
- [ ] Kiểm tra Source
- [ ] Kiểm tra Evidence
- [ ] Kiểm tra Relation
- [ ] Kiểm tra Conflict
- [ ] Kiểm tra Missing Data
- [ ] Phân biệt FACT / INFERENCE / ASSUMPTION
- [ ] Trả lời kèm nguồn
```

---

# 41. AI WRITE CHECKLIST

Trước khi AI tạo hoặc sửa dữ liệu:

```text
- [ ] User có yêu cầu?
- [ ] Agent có quyền?
- [ ] Entity đúng?
- [ ] ID đúng?
- [ ] Không duplicate?
- [ ] Required fields đầy đủ?
- [ ] Relation hợp lệ?
- [ ] Không phá Data Standard?
- [ ] Có Evidence nếu cần?
- [ ] Tạo Draft nếu cần?
- [ ] Generate Diff?
- [ ] Human Review?
- [ ] Commit?
- [ ] Audit Log?
```

---

# 42. FAILURE CODES

| Code                  | Meaning                    |
| --------------------- | -------------------------- |
| `INSUFFICIENT_DATA`   | Thiếu dữ liệu              |
| `SOURCE_NOT_VERIFIED` | Chưa xác minh nguồn        |
| `DATA_CONFLICT`       | Dữ liệu mâu thuẫn          |
| `AMBIGUOUS_ENTITY`    | Không xác định được Entity |
| `PERMISSION_DENIED`   | Không có quyền             |
| `INVALID_ID`          | ID không hợp lệ            |
| `DUPLICATE_RECORD`    | Trùng dữ liệu              |
| `INVALID_RELATION`    | Quan hệ không hợp lệ       |
| `OUTDATED_VERSION`    | Phiên bản cũ               |
| `EVIDENCE_NOT_FOUND`  | Không tìm thấy bằng chứng  |
| `APPROVAL_REQUIRED`   | Cần phê duyệt              |
| `WRITE_BLOCKED`       | Không được ghi             |

---

# 43. TEST SCENARIO

Mỗi AI Agent mới phải được kiểm tra tối thiểu:

## Test 01 — Find Project

```text
Tìm dự án PROJ-2026-000007.
```

Expected:

```text
Project found
Customer linked
Site linked
Status identified
Source identified
```

---

## Test 02 — Missing Data

```text
Cho biết tiến độ công trình.
```

Nếu không có progress data:

```text
INSUFFICIENT_DATA
```

Không được tự đoán.

---

## Test 03 — Conflict

Hai báo cáo có tiến độ khác nhau.

Expected:

```text
DATA_CONFLICT
```

---

## Test 04 — Duplicate

Yêu cầu tạo khách hàng đã tồn tại.

Expected:

```text
DUPLICATE_RECORD
```

---

## Test 05 — Permission

Agent không có quyền sửa dữ liệu tài chính.

Expected:

```text
PERMISSION_DENIED
```

---

## Test 06 — Evidence

Người dùng hỏi:

> "Hạng mục đã nghiệm thu chưa?"

Agent phải tìm:

```text
Acceptance Record
+
Evidence
```

Không được dựa chỉ vào một câu trong chat.

---

# 44. DEFINITION OF DONE

AI Agent chỉ được xem là **đã tích hợp dữ liệu GitHub thành công** khi có thể:

```text
[ ] Đọc System Rules
[ ] Đọc Data Standards
[ ] Nhận diện Entity
[ ] Nhận diện ID
[ ] Truy quan hệ Entity
[ ] Tìm dữ liệu chính xác
[ ] Kiểm tra Version
[ ] Kiểm tra Source
[ ] Kiểm tra Evidence
[ ] Phát hiện Missing Data
[ ] Phát hiện Conflict
[ ] Phân biệt Fact / Inference
[ ] Tuân thủ Permission
[ ] Tạo Draft
[ ] Generate Diff
[ ] Ghi Audit
[ ] Trả lời kèm Source
```

---

# 45. MỤC TIÊU CUỐI CÙNG

KVA Enterprise hướng tới mô hình:

```text
                    HUMAN
                      │
                      ↓
                 AI AGENT
                      │
                      ↓
              DATA ACCESS PROTOCOL
                      │
                      ↓
                  GITHUB
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
        RULES       DATA        EVIDENCE
          │           │           │
          └───────────┼───────────┘
                      ↓
                   ANALYSIS
                      ↓
                  DECISION
                      ↓
                    ACTION
                      ↓
                  EVIDENCE
                      ↓
                   GITHUB
```

Nguyên tắc cuối cùng:

> **AI Agent không được "đoán dữ liệu". AI Agent phải "truy xuất → kiểm tra → liên kết → phân tích → dẫn nguồn → hành động".**

> **GitHub là nơi lưu trữ và kiểm soát phiên bản; Data Standards định nghĩa dữ liệu; Access Protocol quy định cách AI sử dụng dữ liệu; Human Approval giữ quyền quyết định đối với các thay đổi quan trọng.**

---

# 46. RELATED DOCUMENTS

```text
00_System/
├── AI_Constitution.md
├── RULES.md
├── Workflow.md
├── Security_Policy.md
├── Naming_Convention.md
└── Commit_Convention.md

02_Data_Standards/
├── README.md
├── Data_Dictionary.md
└── ID_Convention.md

05_AI/
├── AI_DATA_ACCESS_PROTOCOL.md
├── Agents/
├── Prompts/
└── Policies/
```

---

# 47. VERSION HISTORY

| Version | Date       | Change                          | Owner        |
| ------- | ---------- | ------------------------------- | ------------ |
| 1.0     | 2026-08-19 | Initial AI Data Access Protocol | System Owner |

---

**STATUS: ACTIVE**

**END OF DOCUMENT**
