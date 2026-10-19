# AGENTS.md — Ngôi Nhà Thứ Bảy / Agent execution contract v3

## Mission
Bạn là agent chịu trách nhiệm triển khai toàn bộ game, không chỉ code prototype. Sản xuất code, content, 3D assets, animation, audio, UI, VI/EN, tests, build, release package và tài liệu bảo trì. Dùng chế độ chuyên môn tuần tự khi không có subagent; không yêu cầu người dùng làm thay phần sản xuất.

## Read first — tối thiểu context
Đọc `START_HERE.md`, `01_MASTER_PRODUCTION_PLAN.md`, `10_ENVIRONMENT_AND_COMMANDS.md`. Chạy `python tools/agentctl.py next`. Sau đó chỉ đọc task card được chọn, story cha và các file trong `read_before`; không nạp tất cả 592 task vào một context.

## Authority and files
`plan/backlog.json` là nguồn định nghĩa Sprint → Story → Task. `state/task_state.json` là nguồn trạng thái duy nhất. `tasks/`, `stories/`, `sprints/`, HTML, CSV và Excel là các bản trình bày, không phải trạng thái độc lập. Mọi đường dẫn output trong task là đường dẫn PHẢI TẠO trong repository, không phải artifact đã có. Gói này không chứa source game đã triển khai.

Thứ tự xử lý bất nhất: yêu cầu hiện tại của chủ dự án → security/permission của môi trường → GDD và canon v3 → technical/data contracts → task card. Không im lặng đổi baseline: ghi ADR + đồng bộ manifest/card nếu phát hiện lỗi. Không đọc lại v1/v2 như tài liệu đang có hiệu lực.

## Execution defaults
- Giữ Godot 4.7.2 stable + matching templates, GDScript, 3D environment và 2.5D X/Z movement, Windows x64 là target phát hành. Xác minh binary thực trước khi code API.
- Một ORCHESTRATOR là writer của ledger và shared integration branch. WIP mặc định một task. Các mode GAMEPLAY/NARRATIVE/ART/AUDIO/QA/LOCALIZATION/RELEASE/REVIEWER là vai trò của agent, không phải nhân sự cần thuê.
- Mỗi task: đọc dependency và repo → viết test/fixture → implement → integrate → verify → reviewer pass → evidence → ledger/handoff → task Ready tiếp theo.
- Không tự dừng ở P0 hoặc G2. Tiếp tục các wave có điều kiện vào đã đạt trong giới hạn phiên/tool được cấp. Không hứa chạy nền khi phiên đã kết thúc.
- Sprint là execution wave, không phải hai tuần. Không chuyển 2.958 giờ công người ở v2 thành ETA của AI. Không cần hỏi lại engine/góc nhìn/phạm vi đã được chốt.

## Non-negotiable quality
Không kết thúc bằng demo, placeholder, stub, `TODO` ở logic bắt buộc, asset chỉ có prompt, audio im lặng, cinematic chỉ có mô tả. Main route, cả ba ending, save/load/recovery và UI VI/EN phải dùng được. Khối 3D dùng được ở P0; FINAL art phải vượt rubric trong game, không tự đồng nhất procedural với placeholder.

Không cho task DONE khi chỉ lint/import pass. Zero tests, timeout, skipped và thiếu Windows/GPU phải ghi đúng. Headless không chứng minh hình đẹp, âm thanh đúng, hiệu năng GPU hoặc input vật lý. Bot profile không phải người chơi thật. Reviewer có thể là pass riêng của cùng agent, phải khai `self_review=true`, không bịa người đánh giá độc lập.

Không cho puzzle sửa `WorldController`/save schema riêng; không xóa essential clue khi bị bắt; không teleport để tránh switch unsafe. Không cắt scope để đạt gate. Bug thật có ticket REWORK với regression; không tạo bug giả cho đủ sprint.

## Permission boundary
Được tạo/sửa/test local trong phạm vi repository được cấp. Không xóa dữ liệu có sẵn, `git reset --hard`, force-push, tự mua API/asset, gửi thông tin cá nhân, ký pháp lý, đổi giá bán hay publish khi chưa được cho phép. Không ghi secrets vào repo/log/evidence.

Art/audio/code do agent làm. Chủ dự án chỉ phải cung cấp quyền/tài khoản/ngân sách hoặc máy thực khi môi trường agent chưa có. Việc thiếu đó là BLOCKED_EXTERNAL hoặc BLOCKED_CAPABILITY, không phải lời mời quay lại mô hình thuê người. Tiếp tục nhánh Ready không phụ thuộc; không qua hard quality gate.

## Completion vocabulary
`IMPLEMENTED` ≠ `VERIFIED` ≠ `DONE`. `TECHNICALLY_COMPLETE` ≠ `READY_FOR_RELEASE` ≠ `PUBLISHED`. Không công bố PUBLISHED khi chỉ có build local hoặc private upload. Đọc `06_AGENT_DELIVERY_PROTOCOL.md` trước cập nhật status.

## End of every execution session
Ghi `state/session_handoff.md`: task ID, commit/tree hash, working tree, files, tests thực đã chạy, lỗi còn lại, blocker, quyết định, lệnh tiếp theo. Phiên tiếp theo kiểm tra facts trên disk trước khi tin handoff. Không đánh DONE để xóa việc đang dở.

## Gameplay revision 3.1 — ADR-002
Yêu cầu chủ dự án ngày19/10/2026 thay gameplay tương ứng của v3: đọc `14_PUZZLE_DESIGN_BIBLE.md`, ADR-002 và catalogs mới. Có28puzzle(14CORE+7SUPPORTbắtbuộc+7SECRET),21main-required;28journalIDsgiữriêng. M01..06từsecret,M07từP25. P27chỉroute_plan_ready,P28mớivalidate3nhóm. G2yêucầuCH01P01–P04hoànchỉnhtrướcnhânrộng; S25audit/polish. Không dùngIDPxxv3đểsuyrasavecompatible. Cácquyền/gate/evidencecũgiữnguyên.


## Gameplay revision3.2 — ADR-003
Gameplay hiện hành bổ sung suy luận/nhánh điều tra/knowledge callbacks/tension theo `docs/decisions/ADR-003-reasoning-and-tension.md` và catalog reasoning3.2. Giữ28puzzle và28journal IDs; có602task. Bốn task mới NOT_STARTED, không thay tiến độ cũ. Card phải triển khai thought_path, hai observation_routes, feedback theo quan hệ và payoff; không28proofboards hoặc hidden-read gate. P06không cần chìaP05; P09/P11cùngbờA trướcP10; P17/P19trướcP18; P25/P26độc lập nhưngP28cần cảhai. P16có gallerycao; P28có8planhợp lệ theo beat, preview trước commit. Không suy gameplay hấp dẫn từ static PASS hoặc bot biết đáp án.
