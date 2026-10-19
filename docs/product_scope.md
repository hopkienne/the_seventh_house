# Phạm vi sản phẩm 1.0 — Ngôi Nhà Thứ Bảy

Baseline áp dụng: v3, từ `13_GDD_AGENT_EDITION.md`, `01_MASTER_PRODUCTION_PLAN.md`, `plan/backlog.json` và các catalog trong `specs/`. Đây là phạm vi phải triển khai, không phải tuyên bố các tính năng đã hoàn thành.

## Phạm vi bắt buộc

- 7 chương CH01–CH07, 7 nhà H01–H07, đường làng liên thông. Trường, bến, tháp và đồi là khu phụ, không thêm nhà thứ tám.
- 14 puzzle chính P01–P14, đáp án và state theo `specs/puzzles/`; có input đúng/sai, feedback, hints, persist/reset và regression load.
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

New Game → CH1…CH7 → từng ending → credits; Continue sau restart; corrupt-save recovery; 14 puzzle với đúng/sai/load; 7 memory revisit; 128 tổ hợp memory eligibility và điều kiện tuyến sơ tán. Đo pacing mục tiêu 4–6 giờ ở Alpha, không tăng thời lượng bằng backtracking rỗng. Windows runtime, render/GPU và gamepad vật lý được ghi riêng; headless không thay các phép kiểm đó.

Prototype P0 và vertical slice CH1 10–15 phút là milestone. CH1 còn cần phần mở rộng ở S25. Không dừng triển khai ở G1/G2; chỉ mở wave tiếp theo khi hard gate đã đạt.

## Ngoài 1.0

Combat, multiplayer, open world, jump platforming, crafting, physics water/crowd simulation, mobile/console/macOS retail, full voice acting, New Game+, DLC và cloud saves/achievements. Linux/macOS chỉ có thể là development/test host.

## Trạng thái nhập repository và quyền hạn

Kiểm tra đầu phiên: chỉ có execution pack, không có `project.godot`, source game hay Git metadata. Ledger có 592 task NOT_STARTED; plan validator PASS chỉ cho cấu trúc tài liệu. Không có implementation cũ để reconcile, vì vậy không phát sinh scope delta hoặc thay canon.

Chỉ thay đổi/test local trong repository được cấp. Paid budget mặc định 0. Không mua tài nguyên, gửi dữ liệu riêng, ký pháp lý, đổi giá hoặc publish chưa được ủy quyền. Thiếu công cụ ghi BLOCKED_CAPABILITY; thiếu tài khoản/quyền ngoài ghi BLOCKED_EXTERNAL, tiếp tục nhánh Ready độc lập khi gate cho phép.

`IMPLEMENTED`, `VERIFIED`, `DONE`, `TECHNICALLY_COMPLETE`, `READY_FOR_RELEASE`, `PUBLISHED` có ý nghĩa khác nhau. Đóng task qua agentctl với artifact/hash/checks/review thật; self-review phải khai rõ. Baseline đổi cần ADR và đồng bộ canonical manifest/cards.
