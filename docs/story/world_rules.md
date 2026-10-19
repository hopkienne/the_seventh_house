# Luật thế giới — tám câu hỏi canon

Nguồn chuẩn: `11_STORY_BIBLE.md`; timeline cụ thể tại `canon_timeline.md`. Đây là tài liệu production. “Minh tin” không tự trở thành sự thật, và biết ở production không cho NPC nói sớm.

## 1. Ai khởi động chuông, mẹ làm gì?

**Sự thật:** Minh 9 tuổi kéo cơ cấu khi cố mở cửa cứu An; mẹ chỉnh chốt ổn định rồi duy trì 15 năm. **Minh ban đầu:** chưa hiểu vết tay hoặc lịch bảo trì. **Người chơi:** CH1 thấy foreshadow, CH5 biết mẹ duy trì, CH6 mới biết Minh kích hoạt. Không gọi mẹ là người kích hoạt đầu tiên.

## 2. Vì sao Minh nhớ nhà trước khi nhặt đèn nhưng quên An?

**Sự thật:** dấu khởi động chống lần xóa mới, không phục hồi ký ức cũ đã bị cắt. Đèn mở ERASED và cố định vật chứng. **Minh CH1:** biết có nhà biến mất, chưa có lời giải hoặc nhớ em. **Người chơi:** chứng kiến sự bất nhất trước pickup; không nhận text “đèn cho tôi nhớ”. Giải nghĩa dấu ở CH6.

## 3. An có lớn lên và tự nguyện chịu giá không?

**Sự thật:** An mắc trong buồng neo lúc 6 tuổi, trải qua 15 năm, nay 21. Trẻ 6 tuổi không hiểu và ký giao kèo tự nguyện. **Minh:** không nhận ra em từ đầu. **Người chơi:** áo vàng xa chưa xác nhận tuổi/khuôn mặt; CH6 thấy người trưởng thành mệt nhưng bình tĩnh. Không mô tả cô là phản diện đòi hiến tế.

## 4. REAL và ERASED là hai nơi nào?

**Sự thật:** REAL là nhánh vay mượn hiện tại; ERASED là record của cụm thu hồi bị kéo về thảm họa, không phải chọn năm du hành tự do. Bệ chung là chỗ hai record còn đồng thuận. **Minh:** học chuyển lớp cùng tọa độ khi có đèn. **Người chơi:** biết luật an toàn qua gameplay, chưa cần biết toàn bộ máy chuông. Không có sàn đích thì từ chối; không teleport, không battery gây kẹt. H07 truy cập lõi sau CH6.

## 5. Xóa nhà có giết mọi người và xóa mọi vật chứng không?

**Sự thật:** xóa hình/ghi nhớ xã hội; một số cư dân mắc trong ERASED, không đồng nghĩa chết ngay. Bát thừa, ảnh, vết chiều cao, vải thêu còn nhờ neo sang người/vật/cụm chưa xóa. Mẹ đã mất ký ức trực tiếp An nhưng suy ra người bị giữ từ vật chứng và ghi chép. **Minh:** ban đầu nghi lời NPC, chưa kết luận mọi người đã chết. **Người chơi:** CH1 thấy record còn; CH2 thói quen gia đình; CH3/4 mới hiểu hậu quả lũ. Không giữ/xóa tùy tiện để tiện puzzle; capture giữ essential clue đã commit.

## 6. Vì sao bây giờ chuông thu hồi từng nhà; An có thể dừng không?

**Sự thật:** mẹ qua đời, lần duy trì cuối hết hiệu lực khi Minh trở về. Có bảy cụm neo/bảy nhà; An tách từng cụm để tránh sụp đồng thời, H07 là lõi cuối. Ngăn cô mà chưa xử lý neo làm cả bảy sụp. **Minh:** có thể nghi áo vàng gây hại; đây là hiểu lầm có bằng chứng sửa ở CH6. **Người chơi:** thu hồi theo progression, không deadline wall-clock; không bỏ nội dung vì chậm thao tác. Không thêm boss fight hoặc luật chuông thứ hai.

## 7. Vì sao không rời làng để trốn nợ?

**Sự thật:** nợ gắn với người được cứu và record; Minh từng rời làng mà dấu vẫn còn. Khi thu hồi bắt đầu, đường biên gấp vòng. **Minh:** thử ra biên và trở lại, thấy đường quen dẫn về. **Người chơi:** cảnh ngắn đầu game xác nhận giới hạn; không cần bản đồ thế giới ngoài làng. Đó không phải invisible wall được giải thích bằng lore mới.

## 8. Ba ending trả giá và tuổi như thế nào?

**Sự thật:** A: Minh thay neo hợp lệ nhờ dấu; An trở về 21, Minh bị quên, nợ được trì hoãn. B: giải thể, cơ thể Minh/An về 9/6 với ký ức trải qua, tuyến mặc định làm một nhóm không kịp; epilogue 15 năm mới ở 24/21. C: đủ bảy memory, identity revealed và route validated; nối route, đưa ba nhóm qua trước trả thời gian, epilogue 24/21 bình minh. Không hứa mẹ bất tử hoặc hồi sinh người chết ngoài lũ. **Minh/người chơi:** CH7 hiểu giá trước confirmation, có thể quay lại memory. A/B luôn mở sau main; lỗi thử C về checkpoint, không tự ép sang B.

## Text và điều kiện phát

| Key | Text VI | Điều kiện | Once flag |
| --- | --- | --- | --- |
| story.rules.ch01.edge | Con đường này… lại đưa mình về đây. | CH01, trigger biên đã xảy ra | rule_edge_seen |
| story.rules.ch02.habit | Bà vẫn đặt thêm một chiếc bát. | CH02, quan sát bàn ăn | rule_habit_seen |
| story.rules.ch05.records | Mẹ không còn nhớ người ấy. Nhưng những trang ghi chép vẫn còn. | CH05, E10 committed | rule_records_seen |
| story.rules.ch06.age | Em đã ở đây suốt mười lăm năm. | CH06, an_identity_revealed=true | rule_age_seen |

Các once flags chỉ xác nhận đoạn đã kết thúc, không dùng thay reward/evidence/ending eligibility. Re-enter/load không grant lại. Xem hết và skip commit cùng flags, không cấp memory chưa thu. Đây là ràng buộc dữ liệu cho task dialogue/cinematic sau; chưa có runtime để test.

## Ràng buộc production

H01–H07 là bảy nhà duy nhất. Trường gắn H04; tháp gắn H06, bến và đồi là khu phụ. Knocker là dấu thu hồi, không thêm tộc quái/tôn giáo thật. Không thêm ngày tháng, nguyên nhân chết của mẹ hoặc luật cứu tất cả ngoài canon. Asset nhân vật hiện tại cần An trưởng thành; silhouettes/camera được dùng cho đoạn cơ thể trẻ ở B/C theo Bible.

## Gameplay3.2 / ADR-003
P28 chấp nhận mọi thứtự ba nhóm khi tuyến phùhợp beat: trường qua thưviện ởbeat0 hoặc gallerycao ởbeat0/1/2, tổngtámplan. Preview trước crossing; reading/pause không tăngnước; sai giữnhómđãsafe. GIỮ/MỞ/TRẢ của lõi khác cần1/3/2 ởcổngsân. P27chỉplan;3nhóm+validationrồimớifinalC. MainreadyvẫnP25/P26+identity; A/Bkhôngcầnsecret. Các lối khác nhau không thêmending/nhà hoặc đổi tuổi/canon.
