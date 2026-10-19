# 06 — Agent delivery, review, evidence và resume

## State machine
`NOT_STARTED → IN_PROGRESS → IN_REVIEW → DONE`. `READY` được tính từ dependency, không nhập tay. Chặn việc dùng BLOCKED_DEPENDENCY / BLOCKED_CAPABILITY / BLOCKED_EXTERNAL với reason/attempted/needed. Khi được gỡ, nhận lại bằng start sau khi recheck. Task conditional được NOT_APPLICABLE chỉ có lý do thực, evidence và reviewer; một Must feature không được skip. Task fail đang sửa vẫn IN_PROGRESS hoặc blocker, không DONE giả.

`IMPLEMENTED` mô tả code đã có nhưng chưa được coi là terminal status. `NOT_TESTED` là result của verification, không DONE. PASS artifact review của một task viết tài liệu không chứng minh game pass. Một report có `verification_kind=ARTIFACT_REVIEW` không được dùng thay runtime cho một task chạy executable.

## Definition of Ready
Dependency task IDs đã terminal hợp lệ; read_before được đọc; contract/schema đã xác định; output path rõ; tool capability đủ hoặc có plan unblock không giả; permission đủ nếu external action. Không có resource thì không tự nhận có; claim task để tạo blocker đúng chủng loại nếu cần.

## Definition of Done
Output thực, không chỉ tồn tại file rỗng. Acceptance từng mục có test hoặc document/asset review đúng loại. Integration scene thật và test tương ứng khi task ảnh hưởng gameplay. Evidence chứa task_id, timestamp thực, result, executor, review mode/result/file, revision/build hash phù hợp, artifacts path+sha256, checks có expected/observed/status, command/log/capture. Test runner must count >0 khi là runtime suite. JSON template trong gói chỉ minh họa, không phải evidence đã chạy.

Reviewer pass sau implementation: đọc diff + AC + output + raw test log; cố tìm một failure mode hoặc mismatch; ghi findings/resolution. Có subagent reviewer thật thì dùng nó; nếu không có thì cùng agent làm pass riêng với `self_review=true`. Không invent danh tính reviewer, không gọi self-review là độc lập.

## Dùng agentctl
`next`: đề xuất task theo dependencies và hard gates; ưu tiên task đang IN_PROGRESS/IN_REVIEW. `start`: claim + check deps/WIP. `review`: đặt IN_REVIEW. `finish`: validate evidence, artifact hashes, output globs, result, review, checks; mới ghi DONE. `block`: ghi loại/lý do; `skip`: chỉ conditional + verified NOT_APPLICABLE evidence. `gate`: ghi gate với evidence; G7 chia TECH/PUBLIC trong record.

Công cụ kiểm cấu trúc và bằng chứng file, **không chứng minh sự thật của một câu báo cáo**. Agent reviewer vẫn phải đối chiếu lệnh/log/runtime; không điền template sao cho qua validator rồi coi đã test. Không chỉnh validator để hạ tiêu chí task đang fail.

## Evidence paths và immutability
Mỗi task `reports/tasks/<ID>/evidence.json`, `review.md`, logs/captures. Artifact source có thể được task sau sửa; mỗi evidence nên tham chiếu snapshot/artifact version hoặc commit cụ thể. Không dùng hash hiện tại để tuyên bố task cũ đã fail nếu file tiến hóa hợp lệ; verifier kiểm hashes lúc đóng và archive evidence. Task mới phải xác nhận regression, không rewrite report cũ. Binary build + data + test logs cùng build ID.

Không đưa token, cookie, địa chỉ email riêng hoặc credentials vào evidence. Screenshot account cần redact và lưu tối thiểu. Evidence external gồm operation, account/app/channel/build, authorization ref và result thật; permission không tự phát sinh từ request “làm cả game”.

## Khi test fail
Giữ failing reproducer; xác định expected/observed; fix nhỏ; retest failed case + affected suites; reviewer kiểm diff. Nếu cùng lỗi lặp ba lượt không cải thiện, dừng vòng thử ngẫu nhiên, lập root-cause note/đổi cách kiểm hoặc capability blocker. Không bỏ test hoặc tự kéo timeout vô hạn. Bug production thêm `RW-<parent>-NN` qua manifest change có references và regression; ID gốc không mất.

## Session handoff
Trước context limit/ngắt phiên: lưu task/mode, repo root, branch/commit/tree, changed paths, commands+exit codes, validated vs untested, blockers/decisions, next concrete step, task IDs có thể tiếp tục. Không cần sao chép chain-of-thought; chỉ facts/decisions/actionable notes. Phiên sau kiểm filesystem/git và chạy test liên quan trước khi tiếp tục. Lưu task-level progress dù task chưa xong.

## Parallelism
Mặc định sequential. Chỉ mở song song khi subagent capability thực có, deps đã đủ, không shared files. ORCHESTRATOR giữ ledger lock; workers trả output vào branch/worktree riêng và không tự finish state chung. Merge từng nhánh, chạy integration, ghi actual evidence. Không giả định một agent có thể tự gọi hàng chục agent khi môi trường không hỗ trợ.

## CR / quyết định
Minor tuning theo contract có thể tự quyết với evidence. Đổi scope/canon/public target/paid budget/engine major/save contract cần ADR và impact/retest; scope hoặc chi phí ngoài quyền cần owner. Khi lỗi spec khiến không implement được, ghi conflict, chọn sửa ít rủi ro nhất không đổi product nếu được; đồng bộ canonical manifest và render views. Không duy trì hai backlog có status khác nhau.
