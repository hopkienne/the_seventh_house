# Bắt đầu ở đây — Agent execution pack v3

**Đối tượng đọc:** agent được giao làm toàn bộ dự án. **Trạng thái khi bàn giao gói:** NOT_STARTED; tất cả task chưa thực thi. Đây là tài liệu + công cụ quản lý thực thi, không phải source game hay một daemon tự chạy.

## 1. Đặt gói vào repository
Giải nén. Nếu repository trống, dùng thư mục chứa `AGENTS.md` làm root. Nếu repo đã có code, đối chiếu và merge tài liệu có kiểm soát; không chép đè `AGENTS.md`/state/game files của repo mà không đọc. Đầu tiên ghi `git status`, nhánh hiện tại và inventory các file đang tồn tại. Kết quả ở v1/v2 là tài liệu, không phải code hoàn thành.

## 2. Chạy ba lệnh có sẵn trong gói
```bash
python tools/validate_plan.py
python tools/agentctl.py summary
python tools/agentctl.py next
```
Dùng `python3` nếu Python 3 trên máy dùng tên đó. Chạy từ root. Các script trên chỉ đọc/kiểm tra kế hoạch, không cài phần mềm, gọi API trả phí hoặc làm game. `next` không tự thực thi task.

## 3. Đọc context đúng mức
Đọc `AGENTS.md` → `01_MASTER_PRODUCTION_PLAN.md` → `10_ENVIRONMENT_AND_COMMANDS.md` → `tasks/T-010101.md` và story tương ứng. Tạo capability report trong T-010103. Tên game/góc nhìn/engine/phạm vi đã có mặc định; không hỏi lại.

## 4. Vòng làm việc
Chọn task Ready từ dependency graph → claim bằng `agentctl start` → implement output thật → chạy verification → lưu evidence và review → `agentctl finish` → chọn task tiếp theo. Script sẽ từ chối DONE nếu thiếu evidence, output, test result hoặc dependency.

```bash
python tools/agentctl.py start T-010101 --executor primary-agent
# Agent thực sự tạo/sửa output và kiểm tra nó ở bước này.
# Tạo reports/tasks/T-010101/evidence.json theo templates/EVIDENCE.example.json.
python tools/agentctl.py review T-010101
python tools/agentctl.py finish T-010101 --evidence reports/tasks/T-010101/evidence.json
```
Không chạy `finish` với template chưa điền hoặc artifact chưa có. Không sửa JSON state bằng cách search-replace hàng loạt để qua gate.

## 5. Khi phiên bị ngắt
Dùng `RESUME_AGENT_PROMPT.md`. Đọc handoff và ledger, kiểm repo/test lại thay đổi dở; tiếp tục task đang làm. Không reset tiến độ chỉ vì context mới. Không mở task mới chỉ để né task fail.

## 6. Khi thiếu công cụ hoặc quyền
Thử khả năng thực, ghi blocker cụ thể. Ví dụ không có Windows runtime thì vẫn tạo exported .exe nếu templates sẵn nhưng Windows smoke chưa được kiểm chứng. Làm nhánh không phụ thuộc; không gọi game hoàn chỉnh đã kiểm thử Windows. Chỉ hỏi chủ dự án về yêu cầu không tự cung cấp được (credential, quyền publish, ngân sách, target hardware access).

## 7. Kết quả cuối
Bảy chương đầy đủ và cả ba ending, assets và audio final, save, UI VI/EN, QA, build, source/rebuild, license và handover. Public release cần gate ngoài. Khi chưa có quyền public, bàn giao `READY_FOR_RELEASE` với external queue, không dùng chữ PUBLISHED.
