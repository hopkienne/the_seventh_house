# 13 — GDD Agent Edition 3.2

Gameplay hiện hành theo ADR-002/ADR-003 và `14_PUZZLE_DESIGN_BIBLE.md`. Canon v3 giữ nguyên cùng các bổ sung được ghi trong ADR. Đây là thiết kế phải triển khai, chưa phải tính năng đã chạy. Nghiên cứu so sánh có nguồn tại `docs/design/comparative_gameplay_research_v32.md`.

## Pillars
1. Bí ẩn được chơi: mỗi puzzle tạo vật chứng hoặc làm người chơi nhận ra sự bất nhất của ký ức.
2. Hai thực tại là gameplay cùng một tọa độ, không chỉ là bộ lọc màu.
3. Căng thẳng có tín hiệu, không combat; thất bại không xóa kiến thức bắt buộc.
4. Nhịp cảm xúc chuyển từ nghi ngờ → bằng chứng → đồng cảm với An → lựa chọn có giá.
5. Suy luận dẫn tới hành động: hiểu một quan hệ giúp chọn đường, cấu hình, chứng cứ hoặc thứ tự cứu người. Kết quả có phản hồi và được vận dụng lại.
6. Khám phá có chủ đích: mỗi nhánh có đầu mối để chọn, mỗi chương có một câu hỏi lớn và điểm gắn bó với người trong câu chuyện.

## Player fantasy / session loop
Minh trở về Hạ Vân sau khi mẹ mất. Quan sát căn phòng → inspect/lật/xoay vật thể → ghi và ghim manh mối → liên hệ thông tin giữa các phòng/hai thực tại → thử giả thuyết bằng thao tác hoặc vật phẩm → đọc phản hồi → mở đường và phát hiện sự thật. Sự kiện xóa nhà theo chapter flags, không wall-clock tự tước nội dung. Save tại thời điểm an toàn, checkpoint trước encounter/cinematic/ending. Tỷ trọng mục tiêu: 55% giải đố/tương tác, 25% khám phá, 15% hội thoại/cinematic, 5% sự kiện áp lực; chưa có số đo.

Vòng suy luận có cấu trúc trong từng card: câu hỏi → quan sát → giả thuyết → phép thử → phản chứng hoặc kết luận → kết quả. Giả thuyết là hướng thiết kế, không bắt người chơi chọn thêm menu sau mọi thao tác. Puzzle vật lý nhận lời giải qua world action; P07/P15/P17/P19/P23 cho liên kết chứng cứ có kiểu giới hạn, không parser văn bản tự do.

## Movement và camera
Đi bộ, chạy có kiểm soát, tương tác, nấp, đèn, journal, pause. Không jump/combat/crafting tổng quát; quest recipes được phép theo catalog. X trái/phải, Z chiều sâu, Y vertical. Camera perspective cinematic theo phòng/zone, không free orbit/mouse look; closeup vật thể mở UI cận cảnh. Di chuyển dự đoán được qua camera cuts, collision/volumes giới hạn cả chiều sâu. Keyboard/pad có thao tác thay thế mọi click/drag/rotate.

## Lantern / phases
Có đèn sau sửa kính và pickup P01; P02 dạy vượt rào. Q yêu cầu switch REAL↔ERASED qua WorldController ở cùng pose, sàn đích an toàn và không bị lock. Không battery/ammo/cooldown gây kẹt. Tường/fence/floor/door/LOS/AI/prompt đồng bộ. Reject có chữ/symbol/sound, giữ pose/inventory/flags, không teleport. Closeup muốn đổi phase phải đóng/rebind qua giao dịch world thật, không đổi riêng hình UI. Fade/âm là feedback sau commit.

## Interaction / inventory
E/nút tương tác hoặc click chọn một target trong tầm/LOS đúng phase; click xa không auto-use xuyên map. Closeup có zoom/flip/rotate/slots theo nấc. Khi Warn/Chase không mở closeup mới; tại vùng inspect an toàn, danger advancement dừng khi UI mở. Locks có owner và cleanup khi close/pause/focus.

Inventory quest-only hỗ trợ inspect/combine/use theo recipe cố định, không grid trọng lượng. Wrong-use không tiêu hao; combine nguyên tử, idempotent khi reload. Kính P18 dùng lại P20, đèn P26 thu lại, mồi P04 có reset/recharge. Journal có 28ID stable và các ghi chú/ghim nhỏ riêng; ghim không tự điền lời giải. NPC theo chapter/flags, không spoiler; thu evidence không làm mọi người lập tức miễn nhiễm quên.

## Puzzles
28 puzzle P01–P28:14 CORE,7 SUPPORT bắt buộc,7 SECRET. Mỗi chương 3 required+1 secret; các secret vẫn phải được sản xuất và kiểm thử. Mỗi card có scene/clue provenance/inference/actions/solution/items/rewards/persist/hints/scare/negative tests. Cần suy ra quan hệ để chọn thao tác; không để nguyên mã cạnh khóa. Tutorial dễ được ghi đúng là tutorial.

Mỗi puzzle 3.2 thêm ít nhất hai hướng quan sát với đầu mối khác nhau, giả thuyết có phản chứng, thought_path, feedback theo quan hệ, tri thức vận dụng và payoff. Không bắt bấm đủ clue nếu đáp án hợp lệ đã được suy ra; chỉ giữ điều kiện vật phẩm/evidence thật sự cần. Feedback không báo đúng/sai từng ô để tránh thử tuần tự thành lời giải. Không tăng số thao tác chỉ để kéo dài thời lượng.

CH02 cho P05/P06 song song, P07 hội tụ; P06 có lối ERASED trước chìa, chìa P05 mở shortcut REAL. CH03 có đèn P09 và console/vết bùn P11 ở cùng bờ A trước cầu P10. CH05 cho mô hình/nhật ký thường P19 mở từ entry song song thư P17, cả hai dẫn P18. CH07 cho mở hộp P25 và cửa P26 theo hai thứ tự, P28 chờ cả hai. Nhánh P04/P08/P16/P24 mở sớm hơn ở phòng đã tiếp cận được, không khóa main.

M01..M06 từ secret sáu chương, M07 từ hộp tuổi thơ P25 main. P27 cần cả 7M để tạo route_plan_ready, không khóa A/B. P28 cho thử tuyến trong record, dùng lại kiến thức nước/cửa/cổng để đưa 3 nhóm an toàn; chỉ sau đó evacuation_route_validated và final C confirmation. Có đường revisit trước quyết định; sai thử tuyến trả checkpoint, giữ clue, không forced B. Nước tăng theo decision beats, không khi đọc/journal/pause.

P04 chấp nhận hai vị trí mồi có đường cover thực. P16 có đường thư viện và gallery cao tới cổng sau. Ở P28, cả sáu thứ tự chuyển nhóm đều có phương án đúng: thư viện chỉ dùng trước crossing đầu, gallery còn dùng về sau; tổng tám kết hợp thứ tự/tuyến hợp lệ. `specs/ending_c_decisions.json` là hợp đồng điều kiện. Trước commit có preview nước hiện tại/kế tiếp; crossing đã commit mới tăng beat. GIỮ/MỞ của lõi khác thao tác cần 1/3/2 ở cổng sân. Chỉ khi ba nhóm an toàn mới TRẢ ở lõi. Retry giữ nhóm đã an toàn và không tự chọn B.

## Liên kết kiến thức và nhân vật

`specs/gameplay_reasoning.json` định nghĩa các luật K_PHASE/K_TRACE/K_WATER/K_SEQUENCE/K_AUTH/K_HOLD_OPEN/K_IDENTITY/K_CAUSAL/K_SOUND với nơi dạy và nơi dùng lại. K-ID là trace authoring, không là tiền tệ hoặc read-gate. Main có nguồn học ở main; luật từ nhánh bí mật chỉ làm rõ hoặc phục vụ nhánh tương ứng. P19 tự có mẫu kiểm nguồn khi người chơi chưa làm P17. Luật phải xuất hiện qua quan sát/feedback thật, không chỉ câu thoại nhắc lại ở cuối game.

Mỗi chương có bonding_beat dùng prop/NPC đang có: xếp bát cùng bà Liên, kiểm dây bến với ông Phúc, phục hồi bài tập cho bác Tư, lật trang mẹ viết lại. Các beat này tạo ngữ cảnh cho mất mát, không thêm quest bắt buộc hoặc thay số journal records. Callback tùy thuộc nguồn đã thấy, tránh spoil chương sau. P23 phải chứng minh cùng người, quan hệ gia đình và vai trò ở tháp; không suy danh tính chỉ từ một ô tên được thử đúng.

## Stealth
Knocker FSM Dormant/Patrol/Investigate/Warn/Chase/Search/Return/Capture; cue gõ/caption/animation trước chase. Chỉ biết người chơi từ LOS/sound events và last seen position; không đọc player transform xuyên phase để truy đuổi. Nấp tại vùng định sẵn, không crouch simulation phức tạp. Capture fade → checkpoint; clue đã commit giữ nguyên. Hiệu ứng quên chỉ trình bày tạm, không xóa lời giải đã bắt buộc thu.

Nhịp anticipation→commitment→aftermath có khoảng nghỉ; không buộc mọi puzzle kết thúc bằng scare. Tối đa một encounter cường độ cao được dàn dựng ở CH01(optional), CH04 và CH06; CH07 dùng áp lực quyết định. CH02/CH03/CH05 không chèn chase. Ranh giới threat/closeup rõ, phản hồi nguy cơ có hình/chữ; ý nghĩa của dấu vết có thể bí ẩn nhưng luật sàn, range và input không bị làm mơ hồ.

## Narrative structure
CH1 Họ đã từng ở đây; CH2 Bữa cơm thiếu một người; CH3 Dấu nước trên tường; CH4 Ngôi trường không tồn tại; CH5 Những trang mẹ giấu; CH6 Người mặc áo mưa vàng; CH7 Cánh cửa thứ bảy. Trường/bến/tháp/đồi là khu phụ, không làm thành nhà số 8. Các chi tiết timeline và kết thúc trong Story Bible có ưu tiên hơn pitch ban đầu.

## Presentation
Tạo 3D low-poly stylized có silhouette và texture/material được kiểm soát; làng Việt hư cấu, trời mưa, gỗ/tường cũ/mái ngói. Không sao chép exact assets/nhân vật game tham khảo. REAL ấm nhưng không tư ơi quảng cáo; ERASED lạnh và thiếu hụt cấu trúc, điểm vàng áo mưa An có giới hạn. Không full-face acting; camera/pose/sound đủ gánh cảm xúc. Bộ final phải nhất quán và nhìn được trong gameplay camera.

## UI và accessibility
Main/New/Continue/Load/Settings/Credits/Quit; pause không phá timers/transaction. 3 slot + autosave/backup, settings riêng. Keyboard rebind, gamepad focus/hotplug, scale chữ 100/125/150%, captions cue quan trọng, reduce shake/flash, phase không chỉ dựa màu. VI/EN đầy đủ trước Beta. Hints không dựa riêng vào nghe cao độ.

## Full-game acceptance
New Game → CH1…CH7 → A/B/C → credits; Continue/recovery; cả 28 puzzle đúng/sai/partial-load/revisit; main 21 không cần secret; keyboard/pad/mouse closeup và recipe transactions. Kiểm 128 memory masks cùng plan/trial/validation/identity/main flags, không dependency vòng. CH01 P01–P04 hoàn chỉnh là gate G2 trước nhân rộng; mục tiêu 35 phút chưa đo. Toàn game 4–6 giờ, tổng chapter targets 320 phút, chưa playtest. Không critical placeholders; exported Windows runtime thật. Headless chỉ là bằng chứng một phần, không thay render/GPU/âm thanh/gamepad hoặc trải nghiệm người thật.

Nghiệm thu 3.2: cả hai hướng điều tra, mọi alternate solution được nêu, feedback không per-slot oracle, callback đúng provenance, cue/recovery và cả tám kế hoạch C qua input/runtime thật. Static models chỉ kiểm tính nhất quán. Playtest người chưa biết đáp án ghi riêng giả thuyết/thao tác/hint/lý do mắc; khi chưa có dữ liệu giữ HUMAN_USABILITY_NOT_ASSESSED. Không lấy kết quả nghiên cứu game tham chiếu làm kết quả của game này.

Điều kiện vật lý và thông tin: P10 nhận thông tin từ P09/P11 nhưng không kiểm hai solved flags để cho qua cầu; giải sớm hợp lệ vẫn được nhận, chapterexit cần cả ba. P18 thực sự cần cửa phòng từ P17 và kính từ hộc mô hình P19; nguồn REFLECTOR được chuyển sang P19. Đây không là yêu cầu phải click đọc đủ clue.
