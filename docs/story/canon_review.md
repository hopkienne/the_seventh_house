# Review continuity v3 — ST-0102

Kết quả: PASS cho artifact authoring. Reviewer: codex-primary, `self_review=true`, pass riêng sau khi viết timeline/rules/reveal matrix. Không phải review độc lập hoặc game QA.

| Case | Expected từ Story Bible | Observed | Kết quả |
| --- | --- | --- | --- |
| CAN-01 | Minh kích hoạt trước, mẹ ổn định/duy trì | Timeline tách rõ hai hành động, world rule 1 không gán mẹ khởi động | PASS |
| CAN-02 | Minh nhớ lần xóa mới trước đèn, chưa nhớ An | Timeline và rule 2 giữ đúng; CH1 text chỉ nói nhà biến mất | PASS |
| CAN-03 | Mẹ mất ký ức trực tiếp nhưng có vật chứng/ghi chép | Rule 5 và CH5 text không gán miễn nhiễm cho mẹ | PASS |
| CAN-04 | An 6→21; Minh 9→24 sau 15 năm | Timeline/rule 3/ending matrix khớp, không cộng tuổi hai nhánh | PASS |
| CAN-05 | ERASED là record, không tùy chọn năm; switch an toàn | Rule 4 giữ cùng tọa độ/sàn đích; không teleport/battery softlock | PASS |
| CAN-06 | CH1–CH5 không tiết lộ danh tính em gái | Các text VI có key trước CH6 không gọi An/em gái; exposition production tách khỏi text runtime | PASS |
| CAN-07 | Ít nhất hai dấu báo trước CH1–CH3 | M01 sketch, M02 stitch và M03 assembly bám đúng cạnh catalog; condition chỉ phát sau thu | PASS |
| CAN-08 | Bảy nhà riêng, phụ cảnh không thành nhà thứ tám | Chapter catalog H01–H07; trường H04/tháp H06/bến/đồi là khu phụ | PASS |
| CAN-09 | Mỗi memory nối một cạnh route, không miss vĩnh viễn | Bijection M01–M07, bảy cạnh liên tục H07_FRONT→HILL, missable=false | PASS |
| CAN-10 | A/B không cần optional; C cần đủ M + identity + route | Matrix giữ đúng; unknown/duplicate ID không bù memory thiếu | PASS |
| CAN-11 | A có giá, B mất mát, C cứu qua route; B/C reset tuổi | Tất cả được viết, credits/checkpoint và epilogue 15 năm thống nhất | PASS |
| CAN-12 | Không dependency vòng mở ending | Làm rõ “main xong” là P13 + CH6 reveal trước resolution P14 | PASS sau sửa trước khi đóng T-010203 |

## Lệnh kiểm đã chạy

`python tools/check_narrative_contract.py`: 81 static checks PASS, 11 translation keys độc nhất, 11 once flags độc nhất, 3 early foreshadows; kiểm cả UTF-8, chapter bounds, spoiler lexical, catalog edge/persistence và route connectivity. Raw report tại `reports/tasks/T-010204/narrative_checks.json`.

`python tools/validate_plan.py`: PASS cho document package. Script không chạy Godot hoặc diễn giải nghĩa văn học; continuity nghĩa câu được đối chiếu thủ công ở bảng trên.

## Test reveal cần giữ cho integration sau

1. Xem M02 trước M01, load, rồi thu M01: journal giữ cả hai, hint nối phát một lần; không mở C sớm.
2. Skip từng cinematic so với xem hết: cùng final flags, không grant memory chưa thu; không lặp reward khi load/reenter.
3. Capture sau essential evidence: checkpoint restore vẫn giữ clue, optional eligibility không bị đổi.
4. 128 tập memory × hai trạng thái identity × route × main: 1.024 cases; A/B theo main boundary, C theo đủ tập/identity/route/main.
5. Route C thất bại rồi load checkpoint: không mất memory, không forced B, cho retry hoặc chọn A/B trước final confirmation.
6. Chạy rendered từng A/B/C tới credits: đúng tuổi/giá, không đem cảnh cứu tất cả của C vào B.

Các test integration này **NOT_TESTED**: engine project/StoryState/cinematic/ending chưa được triển khai trong story tài liệu này. Không có blocker về canon còn mở; runtime acceptance tiếp tục ở các task phụ thuộc thích hợp, không ghi gameplay PASS từ 81 static checks.
