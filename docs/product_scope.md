# Phạm vi sản phẩm 1.0 — Ngôi Nhà Thứ Bảy

Baseline áp dụng: gameplay3.2 theo ADR-002/ADR-003, GDD, Puzzle Design Bible và catalogs. Canon v3 được giữ cùng bổ sung giờ hư cấu trong ADR. Đây là phạm vi phải triển khai, không phải tuyên bố đã hoàn thành.

## Phạm vi bắt buộc

- 7 chương CH01–CH07, 7 nhà H01–H07, đường làng liên thông. Trường, bến, tháp và đồi là khu phụ, không thêm nhà thứ tám.
- 28 puzzle P01–P28:14CORE+7SUPPORT bắt buộc+7SECRET. Main cần21; cả28đều phải sản xuất/kiểm thử. Đáp án,clue provenance,inference,state theo catalogs/cards.
- 7 memory M01–M07, có thể quay lại trước quyết định cuối; không khóa ending A/B.
- 28 journal records: 14 evidence E01–E14 + 7 lore L01–L07 + 7 memory M01–M07. Inventory như đèn/chìa khóa không tính thêm record.
- 3 ending A/B/C có playable resolution và credits. A/B luôn khả dụng sau main route; C cần đủ memory và tuyến sơ tán đúng theo canon.
- Minh khám phá Hạ Vân, dùng đèn chuyển REAL/ERASED tại cùng tọa độ. Switch phải an toàn, có lý do từ chối; không teleport hoặc dùng pin đèn gây kẹt.
- Godot 4.7.2 stable và export templates trùng phiên bản là baseline mong muốn; GDScript, môi trường 3D stylized, movement X/Z 2.5D, camera perspective cinematic theo zone. Binary thực phải được xác minh trước khi code API.
- Interaction có range/LOS/priority; stealth không combat, capture về checkpoint và giữ essential clue đã commit. Puzzle không tự thay WorldController hay save schema.
- Save/load/recovery, 3 save slots + autosave/backup, settings riêng. Menu, pause, journal, keyboard rebind và gamepad focus/hotplug.
- UI VI/EN, text 100/125/150%, captions cue quan trọng, giảm shake/flash; phase không chỉ phân biệt bằng màu.
- Agent sản xuất code, art 3D, animation, audio thật, cinematic, localization, QA, build Windows x64, source/rebuild pipeline, license và tài liệu bảo trì. Final art phải được xem trong gameplay; audio phải được nghe khi capability cho phép.

## Nghiệm thu toàn game

New Game → CH1…CH7 → từng ending → credits; Continue sau restart; corrupt-save recovery; 28 puzzle với đúng/sai/load; 7 memory revisit; 128 tổ hợp memory eligibility và điều kiện tuyến sơ tán. Đo pacing mục tiêu 4–6 giờ ở Alpha, không tăng thời lượng bằng backtracking rỗng. Windows runtime, render/GPU và gamepad vật lý được ghi riêng; headless không thay các phép kiểm đó.

G1 là fixture kỹ thuật P02; G2 yêu cầu CH01 P01–P04 hoàn chỉnh, mục tiêu35phút chưa đo. S25audit/polish/revisit, không hoãn puzzle. Không nhân rộng quaG2/G3chưa đạt. Closeup/inventory/quest recipes/journal pins/hints là phạm vi mới phải triển khai.

## Ngoài 1.0

Combat, multiplayer, open world, jump platforming, crafting tổng quát (quest recipes được phép), physics water/crowd simulation, mobile/console/macOS retail, full voice acting, New Game+, DLC và cloud saves/achievements. Linux/macOS chỉ có thể là development/test host.

## Trạng thái nhập repository và quyền hạn

Lịch sử tại lần nhập baseline v3, không phải hiện trạng: chỉ có execution pack, không có `project.godot`, source game hay Git metadata. Ledger có 592 task NOT_STARTED; plan validator PASS chỉ cho cấu trúc tài liệu. Không có implementation cũ để reconcile, vì vậy không phát sinh scope delta hoặc thay canon.

Chỉ thay đổi/test local trong repository được cấp. Paid budget mặc định 0. Không mua tài nguyên, gửi dữ liệu riêng, ký pháp lý, đổi giá hoặc publish chưa được ủy quyền. Thiếu công cụ ghi BLOCKED_CAPABILITY; thiếu tài khoản/quyền ngoài ghi BLOCKED_EXTERNAL, tiếp tục nhánh Ready độc lập khi gate cho phép.

`IMPLEMENTED`, `VERIFIED`, `DONE`, `TECHNICALLY_COMPLETE`, `READY_FOR_RELEASE`, `PUBLISHED` có ý nghĩa khác nhau. Đóng task qua agentctl với artifact/hash/checks/review thật; self-review phải khai rõ. Baseline đổi cần ADR và đồng bộ canonical manifest/cards.

ADR-002 là scope delta được chủ dự án yêu cầu:28puzzle và các hệ tương tác mới;602task, tiến độ thực chỉ ởledger. Giữ evidence cũ, không diễn giải đoạn lịch sử ở trên là repo hiện chưa có project/source.

Gameplay3.2 hiện hành theo ADR-003: xem `docs/design/comparative_gameplay_research_v32.md`, `docs/design/puzzle_depth_matrix_v32.md` và reasoning trong catalog/cards. 28puzzle/21main-required/7secret và28journalIDs giữ nguyên. Định nghĩa602task, trạngthái chỉ ởledger. Kiểm reasoning/routes/tension riêng, không coi tài liệu hoặc finite model là runtime/human playtest.
