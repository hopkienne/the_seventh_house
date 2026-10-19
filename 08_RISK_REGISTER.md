# 08 — Agent execution risk register

| ID | Rủi ro | Trigger | Mode xử lý | Mitigation |
| --- | --- | --- | --- | --- |
| RK01 | Agent chỉ làm prototype rồi dừng | Kết thúc ở G1/G2 dù scope còn | ORCHESTRATOR | Next-task loop, full-game gates, explicit no-demo DoD |
| RK02 | Thiếu Godot/render/Windows | Probe thất bại hoặc chỉ headless | ORCHESTRATOR | Capability ledger; làm nhánh phù hợp, không giả runtime pass |
| RK03 | Art procedural không đạt | Silhouette/rig/lighting không đọc được | ART_AGENT | Golden sample trong game, rerender/review, giữ source có thể sửa |
| RK04 | Audio/cue không kiểm thực | Chỉ peak analysis, không mix capture | AUDIO_AGENT | Nghe/capture theo capability, captions, NOT_TESTED khi thiếu |
| RK05 | Canon/puzzle thay mỗi phiên | Tên/luật/đáp án tự đổi | NARRATIVE_AGENT | Canon+14 specs+stable IDs và ADR |
| RK06 | False DONE / fake evidence | Zero tests, template PASS, dummy artifact | REVIEWER_AGENT | Output/hash/checks + raw logs + explicit review, no fake harness |
| RK07 | Mất tiến độ sau context reset | Phiên mới rebuild từ đầu | ORCHESTRATOR | Ledger + handoff + working-tree verify |
| RK08 | Concurrent agent conflict | Nhiều writer shared files/ledger | ORCHESTRATOR | Sequential default, worktree file scope, ledger lock |
| RK09 | Save/world softlock nhân rộng | Switch unsafe hoặc state không persist | GAMEPLAY_AGENT | G1/G3 hard gates, golden saves, rollback tests |
| RK10 | Asset license không rõ | Nguồn chỉ ghi free/AI-generated | RELEASE_AGENT | Provenance/license audit; replace/block release |
| RK11 | Vượt quyền/chi phí | Tự dùng API, publish, khai identity | RELEASE_AGENT | Spend 0 default, owner authorization scoped |
| RK12 | Headless FPS bị dùng làm GPU benchmark | Thiếu render/hardware metadata | QA_AGENT | Performance native rendered only, fixed routes |
| RK13 | Bot data giả feedback người chơi | Báo tám người thử từ tám profiles | QA_AGENT | Scenario coverage label; HUMAN_USABILITY_NOT_ASSESSED |
| RK14 | Generated views lệch canonical | Excel được sửa như board thứ hai | ORCHESTRATOR | State JSON authoritative; views regenerate/snapshot tag |
| RK15 | Public blocker chặn sai phần local | Chưa account nên dừng làm game | ORCHESTRATOR | Tách G7_TECH/G7_PUBLIC và external queue |
| RK16 | Chronological/calendar giả | Dùng lại 72 tuần/2.958h cho AI | ORCHESTRATOR | Wave/complexity only; đo actual khi thật được cung cấp |

Agent ghi issue thật phát sinh vào ledger/report, không đánh risks CLOSED chỉ vì đã có mitigation trên giấy. Khi cần capability/permission, tạo external request gắn task.
