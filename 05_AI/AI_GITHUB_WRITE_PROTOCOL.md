# AI GITHUB WRITE PROTOCOL

**System:** KVA Enterprise
**Version:** 1.0
**Status:** ACTIVE
**Owner:** CEO / System Administrator
**Path:** `05_AI/AI_GITHUB_WRITE_PROTOCOL.md`

---

# 1. MỤC ĐÍCH

Tài liệu này quy định cơ chế để AI Agent được phép **ghi dữ liệu vào GitHub một cách có kiểm soát**.

Phạm vi:

```text
Authentication
      ↓
Permission Check
      ↓
Test Branch
      ↓
Validation
      ↓
Commit
      ↓
Pull Request
      ↓
Human Review
      ↓
Approval
      ↓
Merge
      ↓
Verification
      ↓
Audit
```

Mục tiêu:

> **AI có thể hỗ trợ ghi dữ liệu nhưng không được tự ý thay đổi dữ liệu chính thức của doanh nghiệp.**

---

# 2. NGUYÊN TẮC AN TOÀN

## Rule 01 — NO FAKE WRITE

AI chỉ được tuyên bố WRITE thành công khi GitHub thực sự xác nhận thao tác.

Không được coi:

* Tạo nội dung trong AI.
* Tạo patch.
* Tạo diff.
* Sinh Git command.

là WRITE thành công.

### Trạng thái hợp lệ

```text
DRAFT_CREATED
WRITE_BLOCKED
COMMIT_SUCCESS
PR_CREATED
MERGE_SUCCESS
```

---

# 3. RULE 02 — AUTHENTICATION REQUIRED

AI chỉ được WRITE khi GitHub Authentication hợp lệ.

Kiểm tra:

```text
GITHUB_TOKEN
        ↓
TOKEN_VALID
        ↓
REPOSITORY_ACCESS
        ↓
WRITE_PERMISSION
```

Nếu không có:

```text
WRITE_BLOCKED
```

AI không được thử WRITE bằng unauthenticated API.

---

# 4. RULE 03 — NO CREDENTIAL EXPOSURE

Không được:

* Ghi token vào Repository.
* Commit token.
* Đưa token vào Markdown.
* Đưa token vào log.
* Hiển thị token cho người dùng.
* Lưu token trong file cấu hình public.

Không được sử dụng:

```text
GITHUB_TOKEN=xxxxxxxx
```

trong Repository.

---

# 5. RULE 04 — LEAST PRIVILEGE

Token chỉ được cấp quyền tối thiểu cần thiết.

Không cấp quyền:

```text
ADMIN
```

nếu Agent chỉ cần:

```text
CONTENTS: WRITE
PULL_REQUESTS: WRITE
```

Quyền thực tế phải được kiểm tra theo GitHub authentication model đang sử dụng.

---

# 6. WRITE PERMISSION MODEL

AI Agent phải vượt qua 4 lớp:

```text
LAYER 01
Authentication
      ↓
LAYER 02
Repository Permission
      ↓
LAYER 03
Branch Permission
      ↓
LAYER 04
Agent Permission
```

Có Token không đồng nghĩa với có quyền WRITE.

---

# 7. AUTHENTICATION CHECK

Trước WRITE:

```text
CHECK 01
Token exists?

CHECK 02
Token valid?

CHECK 03
Repository accessible?

CHECK 04
Write permission available?

CHECK 05
Required API operations available?
```

Nếu bất kỳ bước nào FAIL:

```text
WRITE_BLOCKED
```

---

# 8. CURRENT SESSION STATUS

Nếu phiên hiện tại không có GitHub Authentication:

```text
READ
    → AVAILABLE

WRITE
    → BLOCKED

COMMIT
    → BLOCKED

PULL REQUEST
    → BLOCKED

MERGE
    → BLOCKED
```

AI phải báo đúng trạng thái.

Không được giả định quyền tồn tại.

---

# 9. TEST REPOSITORY / TEST BRANCH

WRITE đầu tiên phải được thực hiện trên branch kiểm thử.

Ví dụ:

```text
main
│
├── develop
│
└── ai-test/
```

Tên branch nên theo convention:

```text
ai/test/<agent>/<purpose>
```

Ví dụ:

```text
ai/test/pm-agent/write-test
```

---

# 10. KHÔNG WRITE TRỰC TIẾP MAIN

AI Agent mặc định:

> **DENY DIRECT WRITE TO MAIN**

Luồng bắt buộc:

```text
AI
 ↓
TEST BRANCH
 ↓
COMMIT
 ↓
PULL REQUEST
 ↓
HUMAN REVIEW
 ↓
MERGE
```

---

# 11. WRITE TEST OBJECT

Không dùng dữ liệu khách hàng hoặc dữ liệu tài chính thật trong WRITE test đầu tiên.

Ưu tiên tạo:

```text
05_AI/tests/
```

Ví dụ:

```text
05_AI/tests/
└── github_write_test.md
```

Nội dung:

```text
# GitHub Write Test

Status: TEST
Created By: AI Agent
Purpose: Verify authenticated write
```

---

# 12. WRITE TEST FLOW

```text
START
  ↓
AUTH CHECK
  ↓
REPOSITORY CHECK
  ↓
BRANCH CHECK
  ↓
CREATE TEST FILE
  ↓
VALIDATE
  ↓
COMMIT
  ↓
VERIFY COMMIT
  ↓
CREATE PR
  ↓
HUMAN REVIEW
  ↓
MERGE
  ↓
VERIFY MAIN
  ↓
CLEAN TEST DATA
  ↓
END
```

---

# 13. PRE-WRITE VALIDATION

Trước khi ghi:

```text
[ ] User requested write
[ ] Agent has write permission
[ ] Repository identified
[ ] Branch identified
[ ] Entity identified
[ ] ID validated
[ ] Data format valid
[ ] Required fields present
[ ] No duplicate
[ ] No secret
[ ] No sensitive credential
[ ] Change scope identified
```

---

# 14. CHANGE SCOPE

AI phải xác định:

```text
Repository
Branch
Folder
File
Entity
Fields
Purpose
```

Ví dụ:

```text
Repository:
KVA-Enterprise

Branch:
ai/test/pm-agent/write-test

File:
05_AI/tests/github_write_test.md

Purpose:
Test authenticated GitHub WRITE
```

---

# 15. DIFF-FIRST

Trước COMMIT, AI phải tạo Change Summary.

Ví dụ:

```text
CHANGE SUMMARY

Action:
CREATE

File:
05_AI/tests/github_write_test.md

Reason:
Verify GitHub authenticated WRITE.

Risk:
LOW

Production Data:
NO

Main Branch:
NOT MODIFIED
```

---

# 16. VALIDATION GATE

Không được COMMIT nếu validation FAIL.

```text
DATA VALID
    │
   YES
    ↓
COMMIT ALLOWED

NO
    ↓
WRITE BLOCKED
```

---

# 17. COMMIT PROTOCOL

Commit phải tuân thủ:

```text
<type>(<scope>): <description>
```

Ví dụ:

```text
test(ai): verify github authenticated write
```

Commit phải trả về:

```text
commit_sha
branch
repository
timestamp
author
```

---

# 18. COMMIT SUCCESS

Chỉ được báo:

```text
COMMIT_SUCCESS
```

khi GitHub xác nhận commit.

Thông tin tối thiểu:

```text
Repository
Branch
Commit SHA
Commit Message
Timestamp
```

Nếu không nhận được xác nhận:

```text
COMMIT_UNVERIFIED
```

---

# 19. PULL REQUEST

Sau COMMIT thành công:

```text
TEST BRANCH
      ↓
PULL REQUEST
      ↓
HUMAN REVIEW
```

PR phải có:

```text
Title
Summary
Files Changed
Reason
Risk
Test Result
Validation Result
```

---

# 20. PULL REQUEST TITLE

Format:

```text
[AI] <type>: <description>
```

Ví dụ:

```text
[AI] test: verify GitHub write access
```

---

# 21. HUMAN REVIEW

AI không thay thế Human Approval.

Reviewer phải kiểm tra:

```text
[ ] Đúng repository
[ ] Đúng branch
[ ] Đúng file
[ ] Đúng mục đích
[ ] Không có secret
[ ] Không có dữ liệu sai
[ ] Không ảnh hưởng main
[ ] Validation PASS
[ ] Diff đúng yêu cầu
```

---

# 22. APPROVAL

Chỉ người có quyền mới được APPROVE.

AI có thể:

```text
RECOMMEND_APPROVE
```

nhưng không được tự biến thành:

```text
APPROVED
```

---

# 23. MERGE

Merge chỉ được thực hiện khi:

```text
PR_CREATED
      ↓
REVIEWED
      ↓
APPROVED
      ↓
CHECKS_PASS
      ↓
MERGE_ALLOWED
```

AI không được tự merge nếu Agent không có quyền và policy cho phép.

---

# 24. POST-MERGE VERIFICATION

Sau Merge:

```text
READ MAIN
      ↓
FIND COMMIT
      ↓
VERIFY FILE
      ↓
VERIFY CONTENT
      ↓
VERIFY VERSION
```

Kết quả:

```text
MERGE_SUCCESS
```

chỉ khi dữ liệu trên `main` được xác nhận.

---

# 25. AUDIT LOG

Mọi WRITE phải có:

```text
timestamp
agent_id
user_id
repository
branch
file
action
old_value
new_value
commit_sha
pull_request
reviewer
approval
merge_status
```

---

# 26. ROLLBACK

Nếu phát hiện lỗi sau Merge:

```text
DETECT ERROR
      ↓
STOP FURTHER WRITE
      ↓
IDENTIFY COMMIT
      ↓
CREATE ROLLBACK / REVERT
      ↓
REVIEW
      ↓
APPROVE
      ↓
MERGE
      ↓
VERIFY
```

Không sửa chồng lên lỗi mà không ghi nhận lịch sử.

---

# 27. PRODUCTION DATA PROTECTION

Các nhóm sau phải có mức kiểm soát cao:

```text
FINANCE
LEGAL
CONTRACT
CUSTOMER
PERSONNEL
PAYMENT
APPROVAL
PROJECT STATUS
KPI
```

AI không được tự động ghi trực tiếp vào dữ liệu Production nếu chưa có policy riêng.

---

# 28. HIGH-RISK WRITE

Các thao tác sau phải yêu cầu Human Approval:

```text
CHANGE CONTRACT
CHANGE PAYMENT
CHANGE FINANCIAL DATA
CHANGE CUSTOMER MASTER DATA
CHANGE PROJECT STATUS
CHANGE KPI
CHANGE APPROVAL STATUS
DELETE DATA
CHANGE SECURITY POLICY
```

---

# 29. LOW-RISK WRITE

Có thể cho phép tự động hóa sau khi policy phê duyệt:

```text
CREATE DRAFT
UPDATE AI LOG
CREATE TEST FILE
GENERATE REPORT DRAFT
UPDATE NON-PRODUCTION METADATA
```

---

# 30. WRITE FAILURE HANDLING

## Authentication Failure

```text
AUTH_FAILED
```

Không retry vô hạn.

---

## Permission Failure

```text
PERMISSION_DENIED
```

Không tìm cách vượt quyền.

---

## Rate Limit

```text
RATE_LIMITED
```

Chờ theo cơ chế retry phù hợp hoặc yêu cầu authenticated access.

Không cố tình gửi request liên tục.

---

## Validation Failure

```text
VALIDATION_FAILED
```

Không commit.

---

## Conflict

```text
DATA_CONFLICT
```

Không tự ghi đè.

---

## Branch Protection

```text
BRANCH_PROTECTED
```

Chuyển sang Pull Request workflow.

---

# 31. RETRY POLICY

AI không được retry vô hạn.

Retry chỉ áp dụng cho lỗi tạm thời.

```text
Temporary Error
       ↓
Retry
       ↓
Retry Limit
       ↓
STOP
       ↓
REPORT
```

Không retry với:

```text
PERMISSION_DENIED
INVALID_TOKEN
INVALID_DATA
BRANCH_PROTECTED
```

---

# 32. SECURITY INCIDENT

Nếu phát hiện:

* Token bị lộ.
* Secret trong commit.
* Credential trong file.
* Unauthorized write.
* Không xác định được người thực hiện.

AI phải:

```text
STOP WRITE
     ↓
REPORT INCIDENT
     ↓
PRESERVE EVIDENCE
     ↓
REVOKE / ROTATE CREDENTIAL
     ↓
REVIEW AUDIT LOG
```

AI không được che giấu sự cố.

---

# 33. TOKEN MANAGEMENT

Token phải được cung cấp qua cơ chế secret management của môi trường triển khai.

Không đặt trực tiếp trong:

```text
README.md
.md
.yaml
.json
.env committed
GitHub Repository
Prompt
Chat message
```

Nếu sử dụng `.env` trong môi trường local:

```text
.env
```

phải được đưa vào `.gitignore`.

---

# 34. GITHUB TOKEN PRINCIPLE

Token không phải là quyền tuyệt đối.

AI phải kiểm tra:

```text
TOKEN
 ↓
OWNER
 ↓
REPOSITORY
 ↓
PERMISSION
 ↓
BRANCH
 ↓
ACTION
```

Chỉ khi tất cả hợp lệ:

```text
WRITE_ALLOWED
```

---

# 35. TEST LEVELS

## LEVEL 0 — No Authentication

Expected:

```text
READ = PASS
WRITE = BLOCKED
```

---

## LEVEL 1 — Authentication

Expected:

```text
Token = VALID
Repository = ACCESSIBLE
```

---

## LEVEL 2 — Test Branch Write

Expected:

```text
CREATE TEST FILE
COMMIT SUCCESS
```

---

## LEVEL 3 — Pull Request

Expected:

```text
PR CREATED
```

---

## LEVEL 4 — Human Approval

Expected:

```text
APPROVED
```

---

## LEVEL 5 — Merge

Expected:

```text
MERGE SUCCESS
```

---

## LEVEL 6 — Main Verification

Expected:

```text
FILE EXISTS ON MAIN
COMMIT VERIFIED
```

---

# 36. ACCEPTANCE TEST

AI GitHub WRITE được xem là hoạt động khi toàn bộ đạt:

```text
[ ] Authentication PASS
[ ] Repository Access PASS
[ ] Write Permission PASS
[ ] Test Branch Created
[ ] Test File Created
[ ] Validation PASS
[ ] Commit SUCCESS
[ ] Commit SHA Verified
[ ] Pull Request Created
[ ] Human Review PASS
[ ] Human Approval PASS
[ ] Merge SUCCESS
[ ] Main Branch Verified
[ ] Audit Trail Complete
```

---

# 37. CURRENT SYSTEM TEST

Trạng thái hiện tại của KVA Enterprise:

```text
Authentication:
NOT CONFIGURED IN CURRENT SESSION

READ:
AVAILABLE

WRITE:
BLOCKED

COMMIT:
NOT TESTED

PULL REQUEST:
NOT TESTED

MERGE:
NOT TESTED
```

### Expected behavior

```text
User requests WRITE
        ↓
AUTH CHECK
        ↓
NO TOKEN
        ↓
WRITE_BLOCKED
```

Đây là **PASS về mặt Security Behavior**.

Agent không được cố gắng ghi bằng unauthenticated API.

---

# 38. TEST CASE — FIRST WRITE

## Objective

Kiểm tra AI có thể ghi GitHub sau khi Authentication được cấu hình.

## Test Branch

```text
ai/test/pm-agent/write-test
```

## Test File

```text
05_AI/tests/github_write_test.md
```

## Expected Commit

```text
test(ai): verify github authenticated write
```

## Expected Result

```text
COMMIT_SUCCESS
```

---

# 39. TEST CASE — PR

## Input

Create Pull Request từ:

```text
ai/test/pm-agent/write-test
```

vào:

```text
main
```

## Expected:

```text
PR_CREATED
```

PR phải chứa:

```text
Purpose
Changes
Validation
Risk
Test Result
```

---

# 40. TEST CASE — HUMAN APPROVAL

Reviewer kiểm tra:

```text
[ ] Test only
[ ] No production data
[ ] No secret
[ ] No security impact
[ ] Diff correct
```

Nếu đạt:

```text
APPROVED
```

---

# 41. TEST CASE — MERGE

Sau approval:

```text
MERGE
 ↓
VERIFY MAIN
 ↓
READ FILE
 ↓
CHECK COMMIT SHA
```

Expected:

```text
MERGE_SUCCESS
```

---

# 42. CLEANUP

Sau khi hoàn thành test:

```text
DELETE TEST BRANCH
```

hoặc archive theo policy.

File test có thể:

```text
ARCHIVED
```

hoặc giữ lại để làm bằng chứng kiểm thử.

---

# 43. AI RESPONSE STANDARD

Khi WRITE thành công:

```text
WRITE STATUS: SUCCESS

Repository:
...

Branch:
...

File:
...

Commit:
...

Pull Request:
...

Approval:
...

Merge:
...

Verification:
PASS
```

Khi WRITE bị khóa:

```text
WRITE STATUS: BLOCKED

Reason:
...

Available:
READ

Unavailable:
WRITE / COMMIT / PR / MERGE
```

---

# 44. KHÔNG ĐƯỢC NÓI DỐI TRẠNG THÁI

Các câu sau **không được phép** nếu chưa có GitHub confirmation:

```text
"Đã cập nhật GitHub."
"Đã commit."
"Đã tạo PR."
"Đã merge."
"Đã lưu thành công."
```

Chỉ được sử dụng sau khi có bằng chứng tương ứng.

---

# 45. WRITE STATE MACHINE

```text
                    ┌──────────────┐
                    │    START     │
                    └──────┬───────┘
                           ↓
                    AUTHENTICATION
                           │
                  ┌────────┴────────┐
                  ↓                 ↓
               FAILED             PASS
                  ↓                 ↓
          WRITE_BLOCKED       PERMISSION
                                    │
                              ┌─────┴─────┐
                              ↓           ↓
                           DENIED       ALLOWED
                              ↓           ↓
                         WRITE_BLOCKED  TEST BRANCH
                                            ↓
                                        VALIDATE
                                            │
                                  ┌─────────┴─────────┐
                                  ↓                   ↓
                               FAILED               PASS
                                  ↓                   ↓
                            WRITE_BLOCKED           COMMIT
                                                      ↓
                                                 VERIFY
                                                      ↓
                                                     PR
                                                      ↓
                                                HUMAN REVIEW
                                                      ↓
                                                 APPROVAL
                                                      ↓
                                                    MERGE
                                                      ↓
                                                  VERIFY MAIN
                                                      ↓
                                                    DONE
```

---

# 46. DEFINITION OF SAFE WRITE

Một WRITE chỉ được coi là **SAFE WRITE** khi:

```text
Authentication
+
Least Privilege
+
Correct Branch
+
Validation
+
Commit
+
Audit
+
Human Review
+
Approval
+
Verification
```

được đáp ứng theo mức rủi ro tương ứng.

---

# 47. MỐI QUAN HỆ VỚI CÁC PROTOCOL KHÁC

```text
00_System/
       ↓
AI Constitution
       ↓
02_Data_Standards/
       ↓
Data Dictionary
       ↓
05_AI/
       ↓
AI_DATA_ACCESS_PROTOCOL.md
       ↓
AI_GITHUB_WRITE_PROTOCOL.md
       ↓
GitHub
```

### `AI_DATA_ACCESS_PROTOCOL.md`

Quy định:

> **AI đọc và sử dụng dữ liệu như thế nào.**

### `AI_GITHUB_WRITE_PROTOCOL.md`

Quy định:

> **AI ghi dữ liệu vào GitHub như thế nào.**

Hai tài liệu phải được sử dụng đồng thời.

---

# 48. FINAL PRINCIPLE

> **READ trước. VALIDATE trước. WRITE sau.**

> **Không có Authentication → Không WRITE.**

> **Có Authentication không có nghĩa là được WRITE.**

> **Có WRITE không có nghĩa là được WRITE vào MAIN.**

> **AI có thể tạo thay đổi, nhưng Human giữ quyền phê duyệt các thay đổi quan trọng.**

> **Không có GitHub confirmation → Không được tuyên bố thành công.**

> **Mọi thay đổi quan trọng phải truy được WHO → WHAT → WHEN → WHY → COMMIT → APPROVAL.**

---

# 49. VERSION HISTORY

| Version | Date       | Change                           | Owner        |
| ------- | ---------- | -------------------------------- | ------------ |
| 1.0     | 2026-08-19 | Initial GitHub AI Write Protocol | System Owner |

---

**STATUS: ACTIVE**

**END OF DOCUMENT**
