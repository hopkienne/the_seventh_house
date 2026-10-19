# 14 — Puzzle Design Bible / gameplay 3.2

Baseline 3.2 phát triển đề xuất 28 puzzle theo ADR-002/ADR-003 và nghiên cứu `docs/design/comparative_gameplay_research_v32.md`. Đây là hợp đồng để triển khai, chưa phải 28 puzzle chạy được. Catalog là `specs/puzzle_catalog.json`; card được sinh từ catalog. Review 3.1 giữ làm lịch sử, các trường reasoning/thought_path/observation_routes 3.2 mới là yêu cầu hiện hành.

## Trải nghiệm hướng tới

**Quan sát → ghi nhận → đặt giả thuyết → thử thao tác → đọc phản hồi → mở không gian hoặc hiểu biết mới.** Người chơi phải hiểu một quan hệ để biết làm gì, thay vì chỉ đọc mã cạnh khóa. Hai thực tại phải thay đổi thông tin, cấu trúc đường đi hoặc điều kiện của cơ cấu. Không thêm luật tùy tiện mỗi chương; complexity tăng từ ánh xạ đơn giản tới loại trừ nhiều điều kiện và tái vận dụng.

Giữ môi trường 3D, movement X/Z2.5D, camera điện ảnh theo phòng, Godot 4.7.2 và Windowsx 64. Tương tác vật thể mở closeup phẳng có phóng to/lật/xoay/kéo theo nấc. Từng thao tác có lựa chọn keyboard/pad tương đương; không cần pixel hunting hoặc kéo chuột chính xác. Tỷ trọng mục tiêu:55% giải đố/tương tác,25% khám phá,15% hội thoại/cinematic,5% sự kiện áp lực. Chỉ đo trên build thật, không suy ra từ số dòng hoặc task.

## Cấu trúc và độ khó

| Chương | SUPPORT bắt buộc | CORE bắt buộc | SECRET tùy chọn | Mảnh | Mục tiêu phút |
| --- | --- | --- | --- | --- | --- |
| CH01 | P01 | P02, P03 | P04 | M01 từ P04 | 35 |
| CH02 | P06 | P05, P07 | P08 | M02 từ P08 | 40 |
| CH03 | P09 | P10, P11 | P12 | M03 từ P12 | 45 |
| CH04 | P13 | P14, P15 | P16 | M04 từ P16 | 50 |
| CH05 | P17 | P18, P19 | P20 | M05 từ P20 | 45 |
| CH06 | P21 | P22, P23 | P24 | M06 từ P24 | 50 |
| CH07 | P25 | P26, P28 | P27 | M07 từ P25 | 55 |

Tổng 28 =14CORE+7SUPPORT+7SECRET. Main cần 21, các SECRET vẫn là nội dung bắt buộc phải sản xuất và kiểm thử. Tổng 320 phút (~5 giờ 20) là dự to án nội dung chưa playtest, không là cam kết thời lượng. P28 là synthesis/resolution có tương tác và lựa chọn đạo đức; không tuyên bố nó là câu đố logic với một đáp án đạo đức đúng.

CH01 dạy thao tác/luật; CH02 suy ra danh tính qua đồ sinh hoạt; CH03 lập tuyến và quan hệ cơ cấu; CH04 quan hệ thứ tự và tài liệu; CH05 kiểm độ tin cậy nguồn; CH06 suy luận nhân quả/danh tính; CH07 dùng lại kiến thức vào cứu người. Không dùng chung công thức “hai puzzle rồi reveal” để định nhịp mọi chương.

## Hợp đồng suy luận và manh mối

Mỗi puzzle phải có: scene và target ID; điều kiện entry; vị trí vật/phong bì/ngăn; ít nhất hai quan sát có provenance; thao tác suy luận; hành động khả dụng; dữ liệu đáp án có đơn vị/hướng; phản hồi sai; reward; persistent fields; hint 3 cấp; scare trigger; ca exploit; test/capture. Không để coding agent tự bịa đáp án từ tên puzzle.

Clue không phải toàn bộ lời giải. Ngoại lệ P01 là bài dạy đọc kim/đối chiếu nơi khác, P02/P10 là bài áp dụng luật không gian. Chấp nhận puzzle dễ có mục đích, không gắn nhãn “suy luận sâu” cho mọi lần lấy đồ. P13 có giải quan hệ, P14 là thi hành chuỗi dependency dùng lại kết quả ấy; không tính hai lần cùng một phát hiện là hai thử thách suy luận độc lập.

Không bắt xem clue mới chấp nhận đáp án đúng, trừ khi cần physical item hoặc evidence đã commit cho quan hệ chứng minh. Inspection flags dùng unlock/hints/provenance, không tạo khóa vô hình lên đáp án đã được suy ra. Journal giữ nguyên nội dung đã quan sát, có snapshot/caption/ghim; không tự điền khóa hoặc tự ghép giả thuyết đúng. P23 phải chọn đúng liên kết và quan hệ, không chỉ đủ 3 record tự phát cinematic.

Mỗi câu cần phản hồi chỉ ra loại bất nhất, không lộ ngay toàn đáp án: mép không nối, kim chưa đồng thuận, nguồn thư thiếu dấu thật, nhánh qua nền ngập, quan hệ không được vật chứng hỗ trợ. Không phạt sai bằng mất vật phẩm essential hoặc reset chương.

## Inventory, closeup và phase

Quest inventory có inspect/combine/use, không weight/grid/crafting tổng quát. Recipe đầu vào/output cố định; consume inputs chỉ trong transaction cùng output grant đã commit. Output unique; dùng sai target không consume. Kính P18 dùng tiếp P20 và tháo được; đèn P26 lấy lại được; mồi P04 reset/recharge được, không nguồn hữu hạn làm mất M01. Đồ tuổi thơ P25 là record props, không lấy con quay của P04 làm main dependency.

Mở closeup chỉ sau range/LOS/phase check. Inventory/journal không cho dùng vật từ bất kỳ đâu trong map. Closeup bắt đầu tại pose an toàn, acquire lock có owner. Khi closeup mở, AI/danger advancement dừng; thông tin quan sát/snapshot giữ nguyên tới đóng. Pause/focus/menu không rò lock. Q trong closeup chỉ khả dụng khi đối tượng được đánh dấu phase_inspectable: đóng view, request WorldController tại cùng pose, safety validate, mở lại view ở trạng thái tương ứng; reject giữ pose/state và view hợp lệ. Không có “đổi lớp UI” vượt sàn/tường.

Closeup không cho chase áp sát bất ngờ. Không xóa threat miễn phí bằng spam mở view: khi đã Warn/Chase không vào closeup; người chơi phải thoát về safe inspect zone, hoặc hoàn tất authored safe boundary. P04 dùng inventory tại cover/bệ an toàn, rồi đóng và thực hiện mồi trong world. Mọi feedback âm có caption/icon; clue không chỉ màu, cao độ, flash hoặc vật nhỏ vài pixel.

## State, rewards và retry

`LOCKED → AVAILABLE → IN_PROGRESS → SOLVED`; wrong input không là terminal. Puzzle có `required_for_main` độc lập role; chapterexit chỉ check 3 requiredpuzzles. SOLVED monotonic trừ NewGame/replay slot riêng; action/rewardidempotent. Item/state/story/world/journal giao qua services và registry, không puzzle ghi savefile trực tiếp. Snapshot partial gồm slots/angles/selection/combined-items/recipe-commit/once-presentation theo từng card. Cancel/close giữ tentative state nhất quán; reset local không xóa clue hoặc reward.

E01–E14 là evidence chính; M01–M07 là memory; L01–L07 là lore. Clue IDs nhỏ như P11_C2 chỉ là ghi chú/ghim. 28 puzzle không yêu cầu 28E. Reward source duy nhất có trong catalogs; P23 collect E12 trước khi xác nhận, `reward_committed` bảo vệ duplicate sau solve. Thiếu E bắt buộc cho biết nơi quay lại, không grant giả; thiếu memory không chặn main.

## Tuyến C và luật thời gian

M01..M06 từ SECRET của sáu chương; M07 từ P25. P27 nối đủ 7 fragment, đúng orientations/ports và ba điểm nhập nhóm → `route_plan_ready=true`. Flag này là kế hoạch, chưa là chứng minh đã sơ tán. P28 chọn Ctrial khi mainready + reveal + đủ M + plan; A/B không yêu cầu plan. Các quyết định tại bến/trường/sân được thử trong record đêm lũ. Khi ba nhóm có mặt ở đồi → `evacuation_route_validated=true`; chỉ lúc ấy finalconfirm C khả dụng. Chọn A/B là giao dị ch riêng; không đòi P28 solved trước khi mở P28.

Nước chỉ tăng theo decision beats có cue; không tăng khi đọc, inventory, journal, pause hoặc loss of focus. Chọn sai quay checkpoint ngay trước quyết định giữ kiến thức; không forced B. Trường có SCHOOL_EXIT_KEY tại tủ ẩn đã mở P16, trong trial có bản record tương ứng nên không yêu cầu tiêu hao chìa quest quá khứ; nếu P16 chưa giải không vàoCtrial. B/C chỉ trả thời gian saufinalconfirm, cơ thể 9/6 tuổi và epilogue 24/21 đúng canon. Không cho người trưởng thành đứng trong lịch sử thực rồi bỏ qua paradox.

## Kinh dị và nhịp

Scare gắn khám phá có once ID và cleanup; không phải puzzle nào cũng có apparition. CH01 phản bội ảnh; CH02 nếp sinh hoạt còn người vắng; CH03 nước như ký ức; CH04 xóa hồ sơ; CH05 nghỉ áp lực, đồng cảm mẹ; CH06 reveal; CH07 hành động có giá. Giữ cues trong noaudio/reducedeffects. Ảnh/evidence neo không bị scare xóa thật. Kẻ Gõ Cửa không biết tọa độ player xuyên phase; closeup không là nơi capture.

## Thứ tự sản xuất và nghiệm thu

G1 kiểm thuật nền P02, không đại diện chapter hấp dẫn. S07 thêm 6 task hệ dùng chung T-070205..210; author P01..03; S08 author P04 và Knocker. G2 yêu cầu CH01 hoàn chỉnh cả 4 puzzle cùng art/audio/UI/save/accessibility, rồi mới nhân rộng qua G3 sang CH02. S25 audit/polish CH01; không đợi S25 mới thêm puzzle.

Mỗi puzzle có happy/wrong/reload/exploit/access fixtures qua input implementation thật; reward exactlyonce, unsafe switch giữ state, replay không debug grant. P11 finite solver chỉ kiểm tính nhất quán đáp án thiết kế; không chứng minh runtime. CH01 cần blind playtest khi có người thật: ghi ai giải được không hint, nhầm luật gì, số lần quay lại, thời gian mắc, lúc hiểu câu chuyện. Không gọi bot biết đáp án là playtester. Khi chưa có dữ liệu ghi HUMAN_USABILITY_NOT_ASSESSED; không chốt người chơi thích bằng staticvalidator hoặc exit 0.

Mã Mxx/Hxx và góc chuẩn trong catalog là ID/fixture authoring, không hiển thị số thứ tự để người chơi chỉ xếp 1→7. Mặt mảnh bản đồ phải dùng địa danh, dấu hướng và cổng nối quan sát được. P15 lưu trang danh sách bị xóa trong E08 sau khi mở tủ; P19 lưu trang mẹ về người con ở tháp trong E10 để P23 có chứng cứ thực, không gán thông tin mới cho record ở phút cuối.

## Chiều sâu 3.2: câu hỏi, phản chứng và phép thử

Mỗi card có `reasoning.question`, hai giả thuyết trở lên, nguồn hỗ trợ/phản chứng, `thought_path` và hai `observation_routes`. Đây là dữ liệu authoring để làm rõ trải nghiệm nhận thức; người chơi không phải đọc các H-ID/K-ID hoặc điền thêm bảng sau mỗi puzzle. Các cảnh P07/P15/P17/P19/P23 cho liên kết có kiểu để biểu đạt suy luận. Các cơ cấu khác nhận câu trả lời qua hành động vật lý.

Ví dụ CH02: người chơi có thể bắt đầu bằng bát hoặc phòng trống. Dấu mòn và lịch sử sửa áo loại khả năng đồ khách/đồ quyên góp. P07 hội tụ hai nguồn để xác định người trong ảnh. Từ đó, một phát hiện về Hạnh được dùng lại khi tìm tuyến thoát, không chỉ mở một ngăn đồ.

Nguồn của mỗi giả thuyết phải thật sự quan sát được. Observation route không đơn thuần là đi ngược một walkthrough: phải có đầu mối khác và một lý do để chọn. Cả hai cùng dẫn tới thông tin đủ để thử lời giải; các chứng cứ bắt buộc khi chứng minh danh tính vẫn phải thu. Clue pins lưu quan sát, không gắn sẵn nhãn đâu là kết luận đúng.

Phản hồi sai nhận xét loại mâu thuẫn của một nhóm quan hệ, không bật xanh/đỏ từng ô hoặc điền phần đã đúng cho người chơi thử hết phần còn lại. Phản hồi cơ khí thật như hai kim cùng chuyển vẫn phải thấy được, vì đó là dữ liệu để suy ra luật. Không phạt người chơi bằng timer/hết vật khi đang kiểm giả thuyết.

## Nhánh điều tra và điều kiện thực

CH02 cho P05/P06 độc lập, P07 hội tụ. P06 vào phòng qua ERASED/Shared ngay từ entry; chìa P05 chỉ mở shortcut REAL. CH03 đặt cả console/vết bùn P11 và đồ sửa đèn P09 ở bờ A; chúng cung cấp thông tin cho P10, không là solved/read-gate để cấm lời giải qua cầu sớm hợp lệ. Chapterexit vẫn cần đủ ba puzzle main.

CH05 cho P17/P19 độc lập: thư P17 mở phòng kín, mô hình P19 trả kính ở hộc thật. P18 cần cả chìa/note và kính; không chỉ kiểm đã đọc hai bài. P19 tự có mẫu kiểm nguồn để không bị kẹt nếu làm trước P17. CH07 cho P25/P26 theo hai thứ tự; P28 vẫn cần cả hai cho mainready. Nhánh secret P04/P08/P16/P24 mở từ những phòng đã tiếp cận hợp lệ, không khóa cốt truyện chính.

Dependency vật lý và liên kết thông tin là hai trường riêng. `depends_on` không được dùng như khóa nếu chỉ có lý do “phải đọc note trước”; `information_inputs` ghi quan hệ hiểu biết. WorldController vẫn kiểm pose/sàn/LOS, mọi route sớm đúng luật đều phải được chấp nhận. G2/G3 kiểm điều này bằng input thật.

## Luật được học và vận dụng lại

`specs/gameplay_reasoning.json` là ma trận nguồn dạy/nguồn dùng, không là registry currency runtime. Mỗi luật dùng ở main có cách học tại main; một nhánh có thể chỉ củng cố luật sớm hơn. Callback cần provenance và chapter guard, không tự xác nhận một giả thuyết người chơi chưa kiểm chứng. P15 bác bỏ quan hệ chuông-gây-vỡ đập; P19 dùng nhận thức ấy để đọc món nợ; P23 tách quan hệ gia đình và vai trò người ở lại; P28 vận dụng thành quyết định.

Không bắt mọi manh mối đều có công dụng như chìa khóa. Chi tiết đời thường có thể tạo gắn bó hoặc hiểu ngữ cảnh, nhưng không dùng hàng chục vật vô nghĩa để che clue cần tìm. Nội dung quanh từng hotspot phải giải thích vì sao nhân vật lại làm cơ cấu ấy: dụng cụ xưởng, máy ghi mực nước, hồ sơ trường hoặc đồ mẹ chuẩn bị, không một chuỗi khóa tùy ý ở mọi căn nhà.

## Tension và trách nhiệm

Mỗi card xác định REST/ANTICIPATION/COMMITMENT/AFTERMATH/REFLECTION, cue và lựa chọn thực. Chỉ thay trạng thái trong nguyên tắc đã dạy. Có thể bất định về ý nghĩa tiếng gõ hoặc bóng người, nhưng luật an toàn/range/input không được cố ý mơ hồ. CH05 giữ khoảng lặng, không thêm chase vì tăng độ khó.

P04 có hai socket mồi FAR_TABLE/LOFT_POST và cover thật; một đường tìm kiếm tới NEAR_HATCH là phương án sai. Cả hai cách đúng phải có replays, không chỉ hai button cho cùng một animation. Safecloseup không tăng danger; Warn/Chase chặn mở mới, không phải một phím đóng băng miễn phí.

P16 ghi hai đường CLASS3A→LIBRARY→REAR_GATE và CLASS3A→UPPER_GALLERY→REAR_GATE. Trong trial P28, thư viện chỉ an toàn ở beat 0, gallery ở beat 0/1/2. Cả sáu thứ tự nhóm có thể dùng gallery; hai thứ tự cứu trường đầu có thêm lựa chọn thư viện, tạo tám kế hoạch. Preview báo điều kiện trước crossing; crossing đã commit tăng beat. Việc đọc/đổi kế hoạch/pause không tăng beat.

GIỮ/MỞ/TRẢ của lõi và cần 1/3/2 của cổng sân là hai target/transaction khác nhau. Dùng 1/3/2 ở cổng không được trả thời gian sớm. `crossing_order` chứa ba nhóm duy nhất là nguồn tiến trình; cached safe_groups/water_beat phải khớp, load mâu thuẫn bị từ chối/khôi phục checkpoint, không tự grant nhóm đã cứu. Chỉ đủ nhóm+validation+explicit confirmation mới TRẢ ở lõi. A/B vẫn là lựa chọn hợp lệ với hậu quả canon.

## Nghiệm thu và nghiên cứu

Đọc nghiên cứu so sánh có nguồn sơ cấp để hiểu nguyên tắc và giới hạn, không nhập co-op/openworld/sanity hoặc puzzle/asset từ game khác. Matrix thay đổi của cả 28 câu được sinh ở `docs/design/puzzle_depth_matrix_v32.md`.

Static tests kiểm nguồn/refutation, tri thức reachable, nhánh không tạo khóa ẩn, finite valve/seating/time/source/route constraints và tám kế hoạch C. Chúng không đánh giá clue dễ đọc hay cảm xúc. Runtime cần REASON/ROUTES/FEEDBACK/TENSION cho từng card, cùng bộ wrong/load/access/revisit hiện có. Ghi HUMAN_USABILITY_NOT_ASSESSED khi chưa có người mới chơi; không gọi một bot đọc đáp án là blind playtest.
