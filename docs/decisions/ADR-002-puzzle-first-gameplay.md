# ADR-002 — Gameplay giải đố kinh dị, baseline 3.1

Ngày: 19/10/2026. Trạng thái: ACCEPTED cho cập nhật thiết kế local theo yêu cầu chủ dự án trong chat này. Không phải xác nhận game đã implement hoặc quyền publish. ADR này thay các phần gameplay/count/slice tương ứng của ADR-000; canon nhân vật và engine vẫn giữ, trừ bổ sung giờ hư cấu dưới đây.

## Nguồn và quyền quyết định

Chủ dự án cung cấp bản đánh giá cùng 28 puzzle và yêu cầu phân tích kỹ để cập nhật gameplay. Bản gốc được lưu nguyên nội dung tại `docs/design/owner_proposal_28_puzzles.txt`; SHA256 trong `reports/design/v31/migration.json`. Các hình/link trong bản gốc là tài liệu tham khảo chưa kiểm tra, không là asset được cấp phép hoặc nguồn xác nhận thiết kế Paper Bride. Chỉ tiếp thu hướng khám phá vật thể/cận cảnh, không sao chép nội dung hoặc tài nguyên game khác.

## Quyết định và giải quyết bất nhất

1. 28 puzzle P01–P28 là các ID mới theo bản đề xuất. Chính xác: 14 CORE + 7 SUPPORT bắt buộc + 7 SECRET. Như vậy có 21 puzzle trên main route và 7 puzzle tùy chọn; không gọi 14 puzzle hỗ trợ đều optional. Bốn puzzle/chương. P14 và P28 là chuỗi tương tác, không giả coi mỗi thao tác là một puzzle độc lập.
2. 28 puzzle độc lập với 28 journal records. Giữ E01–E14/M01–M07/L01–L07; clues nhỏ có ID riêng và được ghim, không sinh thêm journal record. Hai evidence/chương vẫn là records chính. Nguồn từng E/M được cập nhật trong catalog.
3. M01–M06 thưởng từ P04/P08/P12/P16/P20/P24. M07 từ P25 bắt buộc, không phải phần thưởng sau P27. P27 cần cả bảy M để ghép tuyến; không vòng lặp cần M07 để nhận M07. Cả route là optional cho A/B; không còn mô tả cả bảy M đều được thu ở nhánh optional.
4. P27 chỉ đặt `route_plan_ready`. P28 cho thử kế hoạch khi đủ M + identity + plan. Sau khi ba nhóm an toàn mới đặt `evacuation_route_validated`; sau đó xác nhận C. Không yêu cầu flag validated trước khi được thử sơ tán, không đặt flag này chỉ vì ghép bản đồ. A/B chỉ cần main P25/P26 + reveal, không cần P27 hoặc hoàn tất P28 từ trước.
5. CH01/P01–P04 hoàn chỉnh là mẫu nghiệm thu G2, mục tiêu 35 phút chưa đo. G1 vẫn là fixture kỹ thuật hàng rào P02 với đèn trang bị sẵn trong fixture, không giả chứng minh New Game. G2 phải đi từ New Game qua sửa đèn P01 và encounter optional P04. S25 chỉ audit/polish/revisit CH01, không hoãn các puzzle cốt lõi đến gần cuối sản xuất.
6. Closeup, quest inventory inspect/combine/use, clue pins, hypothesis links và hints được triển khai bằng sáu task T-070205…T-070210 trước authoring P01/P02/P03. Dùng tên WorldController/JournalService hiện có; không thêm WorldStateController/EvidenceJournal thứ hai. Không giữ crafting tổng quát, weight grid hoặc engine optics.
7. Các ý tưởng chưa đủ suy luận được làm rõ: P03 dùng quan hệ địa điểm+mép ghim; P05 kết hợp quan hệ chỗ ngồi; P06 ánh xạ năm/biểu tượng; P11 van liên kết modulo3; P13 quan hệ trước/sau; P15 timeline rồi trích mã472; P17 chứng thực nguồn; P22 tách thứ tự kéo1→3→2 khỏi vị trí bánh0/2/1; P23 người chơi chọn liên kết và quan hệ, không tự solve khi thu đủ evidence.
8. Ngày lịch 2011/2026 trong bản đề xuất được chuẩn hóa về T−15/T0 theo canon để không vô tình khóa năm diễn ra game vào ngày phát triển. Bổ sung giờ hư cấu 01:48 cảnh báo, 02:05 vỡ đập, 02:17 lần kéo chuông đầu; không đồng nhất 02:17 với thời điểm nước tới mọi vị trí. P01 cho thấy giờ nhưng chưa giải nghĩa thảm họa.
9. CH04 giữ dòng tên trống. Bỏ `Nguyễn A…` và tiếng gọi “Anh Minh” ở cảnh trường vì kết hợp chúng tiết lộ quan hệ quá sớm. Không tự thêm họ Nguyễn cho nhân vật. CH01 ảnh chỉ được gọi “hai đứa trẻ” đến CH06. An hiện21 tuổi, hồi ức6 tuổi phân biệt rõ; Minh9 tuổi vẫn là người kéo đầu tiên, mẹ là người duy trì.
10. Ảnh đã neo/E đã commit không bị scare xóa. Bóng người trong ảnh mờ đi là lớp trình bày tạm, journal giữ quan sát trước/sau. Knocker là dấu thu hồi, không thêm loài ma riêng; bóng mẹ/Hạnh là record ký ức, không xác nhận hồi sinh. CH05 không chase, không yêu cầu full voice acting.
11. Nước tăng theo decision beats, không wall-clock. Đọc/journal/pause không phạt. Thử sai tuyến C trở lại checkpoint trước quyết định, giữ M/E; không bị ép B. Việc kiểm tuyến diễn ra trong record trước khi trả thời gian; chỉ final commit mới dẫn tới cơ thể Minh9/An6 và epilogue15 năm sau.
12. Mỗi mảnh là một cạnh của tuyến canonical H07_FRONT→…→HILL, không bảy đường độc lập đều lên đồi. Bản đồ có orientation/socket IDs cụ thể; không tự đổi topology khi xoay hình. Ba nhóm nhập vào các node bến/trường/sân rồi theo tuyến đã nối.

## Tương thích và tiến độ

Các Pxx v3.0 bị tái sử dụng với nghĩa khác; lưu mapping trong `specs/puzzle_id_migration_v3_to_v31.json`. P13 cũ tách main sang P25/P26 và map optional sang P27, không phải ánh xạ solved flag một-một. Không migrate save bằng đổi tên string. Hiện chưa có campaign puzzle/save runtime được sản xuất; các test/bootstrap và evidence đã đóng là lịch sử, không rewrite. Khi có old-save thực, phải xác minh design_version/migration policy và test riêng.

Ledger giữ nguyên mọi task state và gate trước đó, chỉ thêm6 task NOT_STARTED, tăng plan_version3.1/revision và cập nhật định nghĩa công việc tương lai. G0 PASS lịch sử không chứng minh gameplay3.1; G1/G2/G3 chưa được thông qua. Không mở production chapter qua gate chưa đạt.

## Verification bắt buộc

Static design: 28 ID duy nhất, 14/7/7 roles, 21 main-required, dependency DAG, không main phụ thuộc SECRET, reward sources, clue provenance, all chapters four puzzles, định nghĩa route-plan/trial/final không vòng lặp. Các finite fixture phải có đáp án nhất quán. Đây không là playable proof.

Runtime tasks phải kiểm đúng/sai/partial save/load, repeated rewards, recipes không mất vật, input keyboard/pad/mouse, focus/closeup/phase locks, no-audio/large text/reduced effects và end-to-end từ New Game. Playtest cảm nhận vẫn HUMAN_USABILITY_NOT_ASSESSED đến khi có dữ liệu thật. Các tỷ trọng55/25/15/5 và tổng320 phút là mục tiêu đo, không ép pacing bằng đi lại hoặc đợi.
