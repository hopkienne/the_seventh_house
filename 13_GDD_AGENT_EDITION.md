# 13 — GDD Agent Edition v3

## Pillars
1. Bí ẩn được chơi: mỗi puzzle tạo vật chứng hoặc làm người chơi nhận ra sự bất nhất của ký ức.
2. Hai thực tại là gameplay cùng một tọa độ, không chỉ là bộ lọc màu.
3. Căng thẳng có tín hiệu, không combat; thất bại không xóa kiến thức bắt buộc.
4. Nhịp cảm xúc chuyển từ nghi ngờ → bằng chứng → đồng cảm với An → lựa chọn có giá.

## Player fantasy / session loop
Minh trở về Hạ Vân sau khi mẹ mất. Ban ngày hỏi chuyện/tìm chứng cứ; sự kiện đêm xóa nhà theo chapter flags; dùng đèn khám phá ERASED để tìm ký ức; đưa phát hiện trở lại REAL; giải puzzle; mở chương tiếp. Không có đồng hồ wall-clock tự tước mất nội dung. Save bất kỳ thời điểm an toàn và checkpoint trước encounter/cinematic/ending.

## Movement và camera
Đi bộ, chạy có kiểm soát, tương tác, nấp, đèn, journal, pause. Không jump/combat/crafting. X là trái/phải; Z là chiều sâu; Y vertical. Camera perspective cinematic theo zone và tracking, không free orbit/mouse look. Di chuyển vẫn dự đoán được qua camera cuts. Greybox giới hạn chiều sâu bằng collision + volumes, không chỉ bức hình nền.

## Lantern / phases
Có đèn sau pickup bắt buộc P01. Q yêu cầu switch REAL↔ERASED. Không battery/ammo/cooldown resource gây kẹt. Chỉ chuyển ở sàn đích an toàn và không bị lock. Tường/fence/floor/door/LOS/AI/prompt phải cùng phase. Switch thất bại trả reason có chữ/symbol/sound; không teleport. Fade/âm là feedback sau state transaction an toàn.

## Interaction / inventory
E hoặc nút south tương tác một target trong tầm và line of sight. Priority rõ, không qua tường. Inventory quest-only, không grid quản lý vật nặng. Essential items/flags idempotent. Evidence journal 28 IDs stable; ngoài evidence có inventory như key/lantern, không cộng chúng thành journal records. NPC điều kiện theo chapter và flags, không tự nói spoiler.

## Puzzles
Mỗi puzzle có states, input conditions, answer, feedback, hints tăng dần, persist/reset và negative tests. 14 file trong specs/puzzles là contract đáp án, không để coding agent tự invent. M01–M07 là optional route fragments, không khóa A/B. Cuối CH7 có đường quay lại ký ức đã mở trước quyết định; không permanently missable fragment.

## Stealth
Knocker FSM Dormant/Patrol/Investigate/Warn/Chase/Search/Return/Capture; cue gõ/caption/animation trước chase. Chỉ biết người chơi từ LOS/sound events và last seen position; không đọc player transform xuyên phase để truy đuổi. Nấp tại vùng định sẵn, không crouch simulation phức tạp. Capture fade → checkpoint; clue đã commit giữ nguyên. Hiệu ứng quên chỉ trình bày tạm, không xóa lời giải đã bắt buộc thu.

## Narrative structure
CH1 Họ đã từng ở đây; CH2 Bữa cơm thiếu một người; CH3 Dấu nước trên tường; CH4 Ngôi trường không tồn tại; CH5 Những trang mẹ giấu; CH6 Người mặc áo mưa vàng; CH7 Cánh cửa thứ bảy. Trường/bến/tháp/đồi là khu phụ, không làm thành nhà số 8. Các chi tiết timeline và kết thúc trong Story Bible có ưu tiên hơn pitch ban đầu.

## Presentation
Tạo 3D low-poly stylized có silhouette và texture/material được kiểm soát; làng Việt hư cấu, trời mưa, gỗ/tường cũ/mái ngói. Không sao chép exact assets/nhân vật game tham khảo. REAL ấm nhưng không tươi quảng cáo; ERASED lạnh và thiếu hụt cấu trúc, điểm vàng áo mưa An có giới hạn. Không full-face acting; camera/pose/sound đủ gánh cảm xúc. Bộ final phải nhất quán và nhìn được trong gameplay camera.

## UI và accessibility
Main/New/Continue/Load/Settings/Credits/Quit; pause không phá timers/transaction. 3 slot + autosave/backup, settings riêng. Keyboard rebind, gamepad focus/hotplug, scale chữ 100/125/150%, captions cue quan trọng, reduce shake/flash, phase không chỉ dựa màu. VI/EN đầy đủ trước Beta. Hints không dựa riêng vào nghe cao độ.

## Full-game acceptance
New Game → CH1…CH7 → A/B/C → credits; restart Continue; save corrupt recovery; cả 14 puzzle đúng/sai/load; 7 optional memory revisit; 128 combinations ending eligibility; no critical placeholders; exported Windows runtime thực. Development Linux/macOS headless pass là evidence một phần, không đại diện Windows/GPU/gamepad vật lý.
