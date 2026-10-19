# 01 — Master execution plan v3

## Mục tiêu giao hàng
Triển khai **toàn bộ game Ngôi Nhà Thứ Bảy**, không chỉ code skeleton, demo hay tài liệu. Agent chịu trách nhiệm trọn vòng sản xuất. Các yêu cầu product nằm trong `plan/backlog.json` R01–R18, chi tiết GDD ở `13_GDD_AGENT_EDITION.md` và canon ở `11_STORY_BIBLE.md`.

| Phạm vi Must | Định nghĩa hoàn thành |
|---|---|
| Campaign | 7 chương/7 đêm/7 nhà H01–H07; đường làng liên thông; mở đầu, cao trào, kết thúc |
| Puzzle/content | 14 puzzle P01–P14; 7 memory M01–M07; 14 evidence E01–E14 + 7 lore L01–L07 = 28 journal records tổng cộng |
| Endings | A/B luôn có sau main route; C cần đủ memory và tuyến sơ tán đúng; cả ba có playable resolution + credits |
| Core | X/Z 2.5D movement/camera; hai thực tại; interaction; stealth không combat; journal, safe save/load |
| Presentation | 3D stylized nhất quán, animation, ambience/cues/music, cinematic; không gameplay placeholder trong final |
| UX | Menu/settings/pause, 3 save slots, keyboard/gamepad, text sizing/reduced effects, VI/EN |
| Delivery | Windows x64 exported build, source + assets + reproducible pipeline + tests + licenses + support runbook |
| Public | Phát hành đúng build khi quyền/nền tảng đủ; không giả định tài liệu này là authorization pháp lý hoặc chi tiền |

**Ngoài 1.0:** combat, multiplayer, open world, jump platforming, physics water/crowd simulation, mobile/console/macOS retail, full voice acting, New Game+, DLC, cloud saves/achievements. Mac/Linux được phép là development/test host, không tự trở thành nền tảng retail.

## Mô hình agent
ORCHESTRATOR quản lý ledger và integration. GAMEPLAY_AGENT lập trình; NARRATIVE_AGENT viết/kiểm canon; ART_AGENT tạo model/material/animation; AUDIO_AGENT tạo và mix; LOCALIZATION_AGENT viết VI/EN; QA_AGENT chạy tests/runtime review; RELEASE_AGENT chuẩn bị phân phối; REVIEWER_AGENT kiểm độc lập với implementation pass. Một agent làm tuần tự tất cả mode là cấu hình hợp lệ. Không tính mode như nhiều nhân sự hay nhiều worker song song mặc định.

Khi có subagents thật: chỉ giao task độc lập, file scope rõ và contract version; mỗi branch/worktree có task ID. Shared files `project.godot`, InputMap, WorldController, SaveService, registries, localization catalog và ledger chỉ một writer. ORCHESTRATOR merge rồi chạy integration suite; review subagent không thay integration.

## Sprint nghĩa là gì trong v3?
Giữ 36 sprint ID để truy vết kế hoạch cũ, nhưng đó là **36 đợt thực thi theo kết quả**, không phải 72 tuần hay deadline cho AI. 146 story và 592 task được giữ ID. Kích thước S/M/L dùng chia context/độ phức tạp, không phải giờ công, token hay cost. Task quá rộng được tách bằng ADR thành subtasks; không xóa ID gốc.

| Wave | Đích đến | Hard gate |
|---|---|---|
| S01–S04 | Toolchain, movement/camera, switching, P0 puzzle | G0, G1 |
| S05–S10 | Story/save/animation/stealth/UI và vertical slice | G2 |
| S11–S12 | Multi-zone, save schema, templates, data authoring | G3 |
| S13–S24 | Sản xuất CH2–CH7: mỗi chương greybox/logic rồi final art/audio/QA | Chapter acceptance |
| S25–S26 | CH1 đầy đủ, ba ending, ghép toàn campaign | G4 |
| S27–S30 | Alpha, pacing, text lock, localization, accessibility | G5, G6 |
| S31–S34 | Performance, release package, RC, license/backup | G7_TECH và G7_PUBLIC tách biệt |
| S35–S36 | Public release được ủy quyền, support theo phiên, final handover | G8, G9 |

S10 chỉ hoàn thành demo CH1 10–15 phút; S25 mở rộng CH1 với P02/M01 và nhịp đầu chương. Không bỏ phần này vì đã có slice. Mục tiêu toàn campaign 4–6 giờ được đo ở Alpha; không kéo dài bằng backtracking rỗng. Không có cam kết ETA/cost chưa đo được.

## Thứ tự chọn việc
Mỗi task có `depends_on_tasks` đã mở rộng dependency story thành task IDs. Chỉ nhận khi tất cả dependency DONE hoặc NOT_APPLICABLE hợp lệ và hard gate trước đã đạt. Ưu tiên task đang làm; tiếp theo là task Ready ở sprint nhỏ nhất, rồi ID. Blocker ngoài không cản một nhánh độc lập nếu hard gate cho phép; đừng mở content production qua G1/G2/G3 đang fail.

Pre-G7 technical work có thể tiếp tục khi external store task bị chặn. S35 public yêu cầu G7_PUBLIC; local source/archive/maintenance prep có thể làm qua scratch/REWORK ticket không public, không đánh Done dependency public chưa hoàn thành.

## Default quyết định không cần hỏi
Dùng canon và puzzle specs đã chốt, stylized low-poly có kiểm visual, procedural toolchain khi không có dịch vụ sinh tài nguyên, data-driven small Resources/JSON, không framework/custom editor lớn. Paid budget=0 đến khi có authorization. Module names/state/IDs theo contracts. Giá trị tuning là initial defaults; agent được chỉnh với trước/sau evidence và không phá acceptance.

## Gates và bằng chứng
Gate kỹ thuật do REVIEWER_AGENT đánh giá từ artifacts thật. Khi chỉ có một agent, tách review pass và khai điều đó. External gates không agent tự phê duyệt thay nền tảng/chủ tài khoản. G0–G6 PASS không đồng nghĩa game bán được. G7_TECH PASS = release package đạt kỹ thuật; G7_PUBLIC PASS = điều kiện xuất bản đủ; G8 PASS = đã published thật.

Remediation RS01/02/03/04 giữ làm tên vùng sửa lỗi sau G1/G2/G4/G7. Tạo ticket từ lỗi thật, có reproducer và regression. Không giả tạo 4 sprint bug hoặc giới hạn số lần sửa bằng estimate cũ. Nếu core gate chưa đạt, sửa core trước nhân rộng content.

## Vòng chất lượng
Task nhỏ → local tests → rendered verification khi cần → review → evidence. Story close khi tất cả task terminal và story AC thật sự đạt. Sprint close khi toàn bộ story đạt, optional/external state ghi riêng và gate tương ứng đạt. Không tính tỷ lệ DONE thay cho mức hấp dẫn. Human playtest được khuyến khích khi có, nhưng không giao phần sản xuất cho con người và không dùng bot data giả lập feedback người thật.

## Kết thúc và báo cáo
Báo riêng ba trạng thái: TECHNICALLY_COMPLETE / READY_FOR_RELEASE / PUBLISHED. Handover phải gồm source, exported build, nguyên liệu art/audio, toolchain locks, manifest hashes, licenses, raw test logs, unresolved issue list và rebuild command. Artifact thiếu runtime được ghi đúng, không làm đẹp dashboard bằng dữ liệu giả.
