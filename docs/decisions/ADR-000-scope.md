# ADR-000 — Áp dụng baseline Full Game v3

Trạng thái: ACCEPTED cho thực thi local theo yêu cầu hiện tại của chủ dự án. Không phải quyền public release.

## Bối cảnh và bằng chứng

Repository nhập vào chỉ chứa execution pack, 592 task chưa thực thi. Validator cấu trúc PASS, không có source game hoặc Git metadata ban đầu. `docs/product_scope.md` áp dụng GDD/canon v3; `docs/requirements.md` dẫn R01–R18 về đúng story/gate chuẩn. Audit và raw probes tại `reports/tasks/T-010103/` xác nhận Python/Git/LFS và Godot portable 4.7.2 stable; chưa xác nhận render Forward+, audio hoặc gamepad vật lý.

## Quyết định

1. Giữ toàn bộ 7 chương/7 nhà, 14 puzzle, 7 memory, 28 records (14 E + 7 L + 7 M), cả 3 ending, save/recovery, UI VI/EN và Windows x64. Không tạo scope delta vì không có implementation cũ khác baseline.
2. Giữ Godot 4.7.2 stable + matching templates, GDScript, 3D stylized, X/Z movement và camera cinematic. Portable binary đã báo `4.7.2.stable.official.ed1daf0bf`; templates và runtime sẽ được kiểm riêng khi bootstrap. Không đổi renderer hoặc engine pin để che lỗi môi trường.
3. Thực thi tuần tự, một task WIP. Codex primary là writer ledger/integration, làm lần lượt các mode chuyên môn. Review là pass riêng, khai `self_review=true`; không giả có reviewer độc lập.
4. Dùng `plan/backlog.json` làm định nghĩa và `state/task_state.json` làm trạng thái. `agentctl` kiểm dependency/WIP/evidence trước DONE; tài liệu và views không có trạng thái độc lập. Prototype/slice là milestone, không thay full campaign.
5. Tự quyết implementation/tuning trong contract, không chờ owner ký từng quyết định kỹ thuật. Có conflict baseline: lập ADR, phân tích impact/regression, đồng bộ manifest và views; không sửa thầm canon/scope hoặc tiêu chí gate.
6. Chỉ đưa thay đổi scope ngoài quyền, mua dịch vụ và thao tác public/legal/account vào permission queue với đề xuất cụ thể. Thiếu capability là capability queue; chưa cần owner action nếu còn đường local hợp lệ. Paid spend=0, publish=false giữ nguyên.

## Hệ quả và xác nhận

Headless chỉ chứng minh logic đã chạy; GPU/render, cảm nhận art/audio, Windows smoke và pad thật có evidence riêng. Không qua G0–G9 khi thiếu điều kiện. Capture không xóa clue, switch không teleport, puzzle không tự đổi WorldController/save schema.

Mỗi task có artifact, hash, checks, raw log phù hợp, self-review, cập nhật agentctl, handoff rồi chọn Ready tiếp theo. Trước Git bootstrap dùng artifact-tree SHA256 thật để định danh evidence; sau bootstrap ghi commit/tree và working tree trong handoff. Không tuyên bố TECHNICALLY_COMPLETE, READY_FOR_RELEASE hoặc PUBLISHED khi mới hoàn thành task tài liệu.

Không phát sinh phí, scope delta, public authorization hoặc tài khoản mới từ ADR này.
