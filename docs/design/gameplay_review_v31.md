# Phân tích bản đề xuất 28 puzzle — 19/10/2026

Bản đề xuất của chủ dự án đã được đọc đầy đủ và đối chiếu với GDD, Story Bible, catalog và backlog. Đây là đánh giá thiết kế, `self_review=true`, chưa có bằng chứng chơi thử campaign. Hình và đường dẫn trong bản gốc chỉ là tham khảo, không phải asset được cấp phép.

## Nhận định chính

Hướng mới tốt hơn ở chỗ đồ vật có công dụng, các phòng liên quan với nhau, người chơi có thể thử giả thuyết và kiến thức cũ có tác dụng ở finale. Các concept mạnh nhất là P12 loại trừ tuyến theo thời gian, P17 phân biệt nguồn đáng tin, P23 chứng minh danh tính và P27/P28 lập kế hoạch rồi vận dụng để cứu người.

Tuy nhiên, tăng từ14 lên28 chưa tự tạo chiều sâu. Nếu giữ nguyên cách trình bày đáp án, P01/P03/P05/P11/P13/P15/P19/P22/P25 vẫn có thể trở thành đọc mã rồi nhập lại. Bản cập nhật vì thế khóa cả quan sát, quan hệ cần suy ra, thao tác, phản hồi và luật tiến triển. Không cố làm mọi câu khó: P01 dạy giao diện, P02/P10 dạy và kiểm tra luật không gian.

## Phân tích từng puzzle

| ID | Giá trị của concept | Rủi ro cần xử lý | Quyết định đưa vào đặc tả |
| --- | --- | --- | --- |
| P01 | Tìm hiểu nhiều nơi để sửa đèn | Đọc02:17 rồi chép lại chỉ là tutorial; kính nằm sau ERASED sẽ gây kẹt | Cửa hàng mở trước khi có đèn; đọc kim giờ/phút và đối chiếu ghi chú; ghi rõ đây là tutorial |
| P02 | Hai lớp thay đổi đường đi | Chìa cạnh giếng có thể buộc chuyển lớp ở chỗ mất sàn | Hai bệ Shared trên tuyến chính; hố giếng ở nhánh phụ; chuyển sai bị từ chối và giữ pose |
| P03 | Lật và phục hồi ảnh vừa kể chuyện vừa tương tác | Số in sẵn cho nguyên thứ tự; gọi hai trẻ là anh em tiết lộ sớm | Quan hệ sông/cây/chỗ trú kết hợp mép ghim và chiều tile; chỉ gọi hai đứa trẻ |
| P04 | Ghép vật rồi suy ra hành vi nghe âm | Mồi dùng một lần; chỉ cần đứng đợi AI; bị bắt mất đồ | Vị trí mồi xa hộc, cover và cue rõ; đặt sai có phản hồi; mồi có thể nạp/reset |
| P05 | Bữa ăn cho thấy người đã bị quên | Sơ đồ ghi đủ tên biến thành sao chép | Kết hợp quan hệ đối diện, hướng mặt trời mọc và dấu ghế; hướng theo phòng, không theo camera |
| P06 | Dấu chiều cao gắn lịch sử một người | Ba thanh tăng dần quá hiển nhiên | Ánh xạ biểu tượng ngăn sang năm/vạch; thứ tự ngăn cho110/125/95, không tăng dần |
| P07 | So hai bản ảnh để nhận diện Hạnh | Thu đủ mảnh tự mở reveal, không cần nhận diện | Căn dấu đăng ký, rồi dùng chữ viết trong sổ để chứng minh tên; NPC phản ứng theo luật quên |
| P08 | Khăn thêu có bản sắc và công dụng | Chỉ nối điểm theo hình mẫu | Quy tắc mũi thêu kết hợp tránh nền trũng; một cạnh đúng của tuyến tổng, không đường độc lập lên đồi |
| P09 | Repair tạo công cụ quan sát cọc | Kho dây nằm sau cầu sẽ gây dependency vòng | Kho cùng bờ A; mạch có sơ đồ; đèn chỉ làm rõ cọc, không tự sửa cầu |
| P10 | Áp dụng luật phase trên tuyến cầu | Lặp P02, ít phát triển về tư duy | Cọc từ P09 giúp đọc bệ; kết nối với điều tra nước P11/P12; không giả gọi đây là puzzle suy luận sâu |
| P11 | Cơ cấu phản hồi trực tiếp với thao tác | Ba van cùng chọn số2 vẫn là chép mã | Van tác động lên các cặp kim; vòng ba nấc; từ reset, mỗi van quay hai lần là đáp án duy nhất modulo3 |
| P12 | Loại trừ dựa vào thời gian và địa hình | Nhầm vỡ đập với nước tới mọi nơi cùng lúc | Cho giờ nhóm tới, thời gian đi và giờ ngập từng lối; tính đủ hành trình, chọn HIGH_RAMP |
| P13 | Có thể suy ra thứ tự buổi học | Thu ba mảnh có sẵn cả chuỗi thì chỉ là nhặt đồ | Hai quan hệ trước/sau và đồng hồ xác định buổi; suy Đọc→Vẽ→Hát |
| P14 | Chuỗi thao tác qua nhiều phòng | Bấm ba nút lặp lời giải P13; khóa phòng có thể khóa luôn item cần lấy | Các phòng tiếp cận được; sách cho dải tranh, tranh cho đĩa máy; chỉ archive bị khóa |
| P15 | Dòng thời gian trở thành chìa hồ sơ | Xếp giờ quá trực tiếp; nhầm chuông với lũ | Xếp WARNING/DAM_BREAK/FIRST_BELL rồi trích mã472; ba loại sự kiện được tách rõ |
| P16 | Lập tuyến thoát có ứng dụng cuối game | Ghép giấy đẹp nhưng đi xuyên cửa đóng hoặc sân ngập | Kiểm đồ thị cửa/nền cao; tránh SHORT_YARD, đi qua thư viện ra cổng sau; chìa có bản record trong trial |
| P17 | Kiểm độ tin cậy trước khi dùng dữ liệu | Phân biệt bằng màu mực gây bất công | Phải có cả niêm liên tục và mực thấm mặt sau, thể hiện bằng hình/chữ; loại bản sao trước khi xếp thời gian |
| P18 | Hai lớp góp trạng thái cho một cơ cấu | Chỉ hai boolean như cũ; optics vượt phạm vi; kính mất trước P20 | Góc kính theo nấc và tia dàn dựng; cả vị trí lẫn hướng có tác dụng; kính tháo được |
| P19 | Dựng mô hình luật thu hồi | Thiếu dữ liệu xác định trạng thái; không rõ H05 đã bị xóa chưa | Chốt entryCH05 sau năm lần thu hồi; H05 đang là record; H06/H07 còn active |
| P20 | Vận dụng lại kính theo cách khác | Kính bị khóa tại P18; thư tiết lộ An sớm | Chọn ổ và góc để nối lối cao; kính dùng lại được; thư chưa nêu tên An |
| P21 | Học quan hệ cơ khí để dùng ở finale | Đòi nghe cao độ hoặc thử chuông thật làm thay canon | Bộ chuông mẫu cách ly; HOLD trước OPEN trước RETURN; text/icon tương đương âm, không timing |
| P22 | Phối hợp cần và bánh răng | 1–3–2 vừa là thứ tự vừa là giá trị, dễ triển khai sai | Chốt pull_order1/3/2 riêng với gear_detents0/2/1; hình học khía cho phép tìm cấu hình |
| P23 | Suy luận xuyên chương đem lại phần thưởng cảm xúc | Đủ ba record tự reveal; tên đúng chưa chứng minh quan hệ | Người chơi chọn hai liên kết có kiểu và quan hệ em gái; E12 lấy tại entry trước xác nhận |
| P24 | Vận dụng luật cho nhánh bí mật | Mỗi mảnh đều là đường thẳng lên đồi làm topology mâu thuẫn | Cấu hình chốt mở đường bảo trì ứng với cạnh M06; không điều khiển chuông lõi |
| P25 | Ký ức được thao tác trước cao trào | Nếu cần con quay P04 thì nhánh tùy chọn khóa main; không rõ nguồn M07 | Đồ record riêng; quan hệ trước/sau đủ suy ra thứ tự; nhận M07 ở đây |
| P26 | Nhận ra biểu tượng từng gặp, dùng đèn như chìa | Đáp án chưa xác định; đặt đèn rồi mất luôn | MEMORY=TWO_MARKS, TIME=LOOP, ANCHOR=LATCH có nguồn từ chương trước; mở cửa rồi thu hồi đèn |
| P27 | Tổng hợp phát hiện thành kế hoạch | Đủ mảnh tự mở C; vòng lặp nhận M07; đặt validated quá sớm | M07 từ P25; xoay theo dấu Bắc, nối ports và ba nhánh nhóm; chỉ tạo route_plan_ready |
| P28 | Finale yêu cầu vận dụng thay vì chỉ chọn nút | Cần validated trước màn validation; nước đếm giờ; người trưởng thành đứng trong quá khứ | Trial trong record, nước theo quyết định; ba nhóm an toàn mới validated/finalconfirm; tuổi sau return-time theo canon |

## Những bất nhất đã giải quyết

- Cách gọi14 chính+14 hỗ trợ chưa phản ánh luồng chơi: cấu trúc được chốt14CORE+7SUPPORT bắt buộc+7SECRET, tức21 main-required. Mỗi chương có3 bắt buộc và1 bí mật.
- 28 puzzle khác28 journalrecords. Giữ14E+7M+7L; ghi chú nhỏ được ghim riêng. Không phải mỗi puzzle đều phải thưởng mộtE mới.
- M01..M06 đến từ sáu nhánh bí mật; M07 từ P25. P27 lập kế hoạch; P28 kiểm chứng. Thiếu secret không khóa A/B và không có vòng lặp điều kiện.
- Không đưa Nguyễn A… hoặc tiếng gọi Anh Minh vào CH04. Không tự thêm họ nhân vật. CH01 chỉ gọi hai đứa trẻ. Cảnh ảnh mờ không xóa bản chứng cứ đã neo.
- Giữ thời gian tương đối T−15/T0; bổ sung giờ hư cấu01:48/02:05/02:17, không tự chốt năm2011/2026 từ ngày phát triển.
- G2 phải có CH01 P01–P04 hoàn chỉnh trước nhân rộng. S25 chỉ audit/polish, không để ba phần tư thiết kế mới chờ tới cuối dự án.

## Gắn bó, nhịp chơi và phạm vi

Người chơi cần gặp hoặc chia sẻ một hành động đời thường với NPC trước khi bị yêu cầu quan tâm tới mất mát của họ. Sau puzzle, phản ứng nhỏ của bà Liên/ông Phúc/bác Tư giúp khám phá có hậu quả. Thu chứng cứ không khiến họ lập tức nhớ lại tất cả.

Clue đã thấy có snapshot/ghim, shortcut mở sau solve. Không bắt đi lại để chép biểu tượng, thử item lên mọi prop hoặc dựa vào pixel nhỏ. CH05 giữ nhịp nghỉ và đồng cảm với mẹ; không thêm chase chỉ để tăng số sự kiện kinh dị.

Scope tăng thật: thêm closeup, inventory recipes, clue pins và các puzzle/props/audio/UI/VIEN/QA tương ứng. Sáu task nền không đại diện toàn bộ công việc tăng thêm. Chapter tasks được mở rộng thành bốn puzzle; không dùng estimate cũ làm ETA. Tổng320 phút và tỷ trọng55/25/15/5 là mục tiêu, chưa đo.

## Rủi ro còn mở và cách kiểm

Chưa xác nhận độ khó thực của P11/P17/P23/P27, khả năng hiểu phase safety, nhịp gián đoạn do closeup và sức hấp dẫn của CH01. C có thể là lựa chọn hiển nhiên khi mở đủ điều kiện; giữ nó như phần thưởng điều tra, không tự thêm cái giá ngoài canon để ép lựa chọn đạo đức.

Khi có người chơi thật, quan sát lần chơi đầu không giải thích chủ động: họ nhìn gì, giả thuyết nào đã thử, mắc ở đâu, dùng mấy hint và giải thích vì sao đáp án đúng ra sao. Bot biết file đáp án không chứng minh puzzle dễ hiểu. Giữ HUMAN_USABILITY_NOT_ASSESSED khi chưa có dữ liệu. Static validator chỉ kiểm consistency; runtime và cảm nhận cần bằng chứng riêng.
