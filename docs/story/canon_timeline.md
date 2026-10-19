# Timeline canon — sự kiện gốc và thời gian vay mượn

Nguồn: `11_STORY_BIBLE.md`, reveal CH01–CH07 trong chapter catalog. Các sự thật dưới đây dành cho production; chỉ text được gắn reveal mới đến người chơi. Không phải dữ liệu lịch sử thật.

| Mốc | Sự thật production | Nhận thức/điểm reveal |
| --- | --- | --- |
| T−15 năm, trước lũ | Minh 9 tuổi, An 6 tuổi, là hai anh em. Vỡ đập làm nước tới Hạ Vân. | CH3 có chứng cứ nước; CH4 xác nhận làng bị hủy 15 năm trước. Quan hệ chưa lộ trước CH6. |
| T−15 năm, kích hoạt | Minh kéo cơ cấu chuông khi cố mở cửa cứu An. Minh là người kích hoạt đầu tiên và mang dấu khởi động. | CH1 cho thấy vết tay/phản ứng chuông, không giải nghĩa. CH6 xác nhận người kích hoạt. |
| T−15 năm, ổn định | Mẹ nhận ra hồi thời và chỉnh chốt giữ làng trước khoảnh khắc bị phá. An mắc trong buồng neo khi cửa đóng. | CH5 lộ mẹ duy trì và có người ở lại; CH6 mới xác nhận An và cái giá. Không kể trẻ 6 tuổi tự nguyện ký một giao kèo. |
| T−15…T0 | Đời sống tiếp diễn trong nhánh vay mượn; người được cứu lớn lên. Minh rời làng; An cũng trải qua 15 năm trong buồng neo, nay 21 tuổi. | Người chơi ban đầu không biết An, không dùng mô hình trẻ 6 tuổi để biểu đạt An hiện tại. |
| T−15…T0, mẹ duy trì | Mẹ bảo trì định kỳ. Ký ức trực tiếp về An bị xóa như người khác; bà suy ra người bị giữ từ vật chứng, ghi lại và giữ đồ neo. | CH5 nhật ký không chứng minh mẹ miễn nhiễm. Không đồng thời gọi mẹ là người kích hoạt đầu tiên. |
| Ngay trước game | Mẹ chuẩn bị đèn/bản đồ/thư lịch suy hao rồi qua đời. Lần bảo trì cuối hết hiệu lực khi Minh trở về, ở tuổi 24. | Không thêm ngày tháng hoặc nguyên nhân tử vong chưa được canon xác định. |
| CH1…CH7 | Bảy cụm neo suy hao; An tách từng cụm để tránh bị nuốt đồng thời. H07 của gia đình Minh là lõi cuối. | Thu hồi theo story flags, không wall-clock deadline làm mất nội dung. Áo vàng xa ở CH1 chưa được gọi là em gái. |
| Trước quyết định cuối | Sau CH6, cửa H07 cho truy cập lõi đêm lũ. Người chơi có thể quay lại memory trước final confirmation. | Ba lựa chọn được giải thích ở CH7, không thêm luật cứu tất cả phút cuối. |
| A | Minh dùng dấu khởi động thay An. An về ở tuổi 21, làng ổn định một chu kỳ; Minh bị quên. | Không nói món nợ đã hết. Ảnh trống và đèn sáng tiếp tục trả giá. |
| B/C, trả thời gian | Cơ thể trở về đêm lũ: Minh 9, An 6, giữ ký ức vừa trải qua. B dùng tuyến mặc định, một nhóm không kịp; C nối route từ đủ memory và cứu các nhóm. | Không đặt cơ thể trưởng thành trong quá khứ rồi bỏ qua nghịch lý. |
| Epilogue B/C | Nhảy 15 năm trong lịch sử mới: Minh 24, An 21. B tưởng niệm; C cùng nhìn bình minh. | Không hứa mẹ sống mãi hoặc hồi sinh người chết ngoài trận lũ. |

## Dấu khởi động và đèn

Dấu chống lần xóa **mới**, không khôi phục ký ức đã cắt về An. Vì vậy Minh nhớ H01 vừa biến mất trước pickup đèn nhưng chưa nhớ em gái. Đèn mở ERASED và cố định vật chứng; đèn không trao năng lực nhớ. REAL là đời sống vay mượn hiện tại; ERASED là record bị thu hồi, không phải máy du hành tùy năm.

## Text/trigger contract cho production

Các key dưới đây khóa câu chữ VI ở mức timeline. Chúng chỉ được phát trong chapter/điều kiện đã ghi; localization EN và runtime dialogue được sản xuất ở task tương ứng sau khi engine/trigger system có thật.

| Key | Text VI | Điều kiện tối thiểu | Once flag |
| --- | --- | --- | --- |
| story.timeline.ch01.remember_house | Hôm qua còn có một căn nhà ở đây. | CH01, H01 đã thu hồi; không cần lantern_owned | timeline_ch01_seen |
| story.timeline.ch04.flood_record | Hạ Vân đã bị phá hủy mười lăm năm trước. | CH04, E08 đã commit | timeline_ch04_seen |
| story.timeline.ch05.maintenance | Mẹ đã giữ những chốt này hoạt động suốt từng ấy năm. | CH05, E10 đã commit | timeline_ch05_seen |
| story.timeline.ch06.first_pull | Chính anh đã kéo cơ cấu chuông khi cố mở cửa cứu em. | CH06, an_identity_revealed=true | timeline_ch06_seen |

Skip và xem hết phải commit cùng once flag ở boundary của đoạn; load không phát thưởng evidence/memory lần nữa. Text timeline không tự grant M01–M07. Đây là contract authoring, chưa có runtime cinematic/skip/load để kiểm trong T-010201.

## Kiểm tra continuity

Minh luôn kích hoạt trước, mẹ luôn ổn định/duy trì sau. Minh 9→24, An 6→21 trong nhánh vay mượn và epilogue mới. Không nhầm hai khoảng 15 năm là cộng tuổi thành 39/36. Mẹ không cần nhớ trực tiếp An để duy trì, vì còn vật chứng neo. Rời làng không xóa dấu/nợ; biên gấp vòng khi thu hồi bắt đầu. Capture không được xóa clue đã commit. Canon chưa xác định chi tiết ngày/giờ; không bịa thêm để lấp lịch.
