# Nghiên cứu gameplay phục vụ baseline 3.2

Ngày kiểm nguồn:19/10/2026. Phương pháp: đọc trang nhà phát triển, devlog và lời trả lời trực tiếp trong phỏng vấn. Đây là desk research, không phải đã chơi hết các game, xem toàn bộ video hoặc thực hiện playtest. Không dùng điểm đánh giá, doanh thu hay độ nổi tiếng làm bằng chứng thiết kế sẽ hiệu quả cho dự án này. Phần áp dụng là suy luận thiết kế riêng của Ngôi Nhà Thứ Bảy; không sao chép puzzle, lời thoại, hình hoặc nghi thức.

## Nguồn đã đọc và giới hạn kết luận

| ID | Game / nguồn sơ cấp | Điều được nguồn hỗ trợ | Áp dụng có chọn lọc |
| --- | --- | --- | --- |
| RS01 | [Paper Bride2 — mô tả của HeartBeat Plus](https://store.steampowered.com/app/1879380/Paper_Bride_2_Zangling_Village/) | Khám phá bí ẩn làng, tăng chi tiết manh mối và suspense được nhóm phát triển nêu rõ | Vật sinh hoạt và dấu vết địa phương dẫn suy luận. Trang giới thiệu không chứng minh cấu trúc dependency cụ thể hoặc mọi câu đố đều sâu. Không lấy văn hóa Trung Quốc làm quy luật ngầm của làng Việt |
| RS02 | [The Room — Fireproof Games](https://www.fireproofgames.com/games/the-room) | Cơ cấu biến đổi từng lớp, công cụ nhìn thông tin ẩn, thao tác trực quan | Vật thể có affordance và phản hồi cơ khí; inspect có mục đích. Các ô xoay chỉ tồn tại khi có lý do trong đồ vật, không thêm hộp khóa ở mọi nhà |
| RS03 | [Rusty Lake / The Past Within — Devlog3](https://blog.rustylake.com/the-past-within-devlog-3/) | Không gian dễ hiểu, lựa chọn vừa đủ; puzzle theo chủ đề nơi chốn; playtest làm lộ cách hiểu ngoài dự kiến | Giới hạn vật khả dụng theo ngữ cảnh, thao tác quen thuộc trước thử thách; information split giữa hai thực tại. Không đưa co-op hay nội dung ngoài game vào1.0 |
| RS04 | [Outer Wilds — Alex Beachum nói về pathing](https://www.mobiusdigitalgames.com/news/the-intentionality-of-wandering) | Cần cho người chơi đủ dấu hiệu để chọn hướng vì tò mò; đường đi không nên là tung đồng xu | Nhánh hồ sơ/nhánh khảo sát có mục tiêu quan sát được, hội tụ tại một giả thuyết. Giữ phạm vi phòng nhỏ, không nhập hệ mặt trời, vòng lặp thời gian hoặc open world |
| RS05 | [The Case of the Golden Idol — Andrejs Klavins trả lời phỏng vấn](https://www.gamedeveloper.com/design/case-of-the-golden-idol) | Khó khăn ở việc người chơi diễn đạt suy luận; phản hồi toàn bộ đúng/sai và phản hồi từng ô đều có đánh đổi; cần người chưa biết đáp án để đánh giá | Nhận xét theo nhóm quan hệ và dạng mâu thuẫn; không lộ từng ô đúng; cho nhiều đường quan sát. Không lấy mô tả của tác giả làm bằng chứng tự động rằng puzzle của ta dễ hiểu |
| RS06 | [Return of the Obra Dinn — Lucas Pope trả lời GDC](https://www.gamedeveloper.com/design/for-lucas-pope-i-return-of-the-obra-dinn-i-was-a-bunch-of-appealing-design-problems) và [trang chính thức](https://obradinn.com/) | Người chơi mang vai điều tra, tìm hiểu số phận con người; thiết kế phải giải quyết ràng buộc cụ thể | Ghép danh tính bằng các nguồn có provenance và ngữ cảnh. Không sao chép60nhân vật hoặc tự khẳng định cơ chế xác nhận theo lô từ các đoạn nguồn không mô tả nó |
| RS07 | [Frictional — Thomas Grip,9Years9Lessons](https://frictionalgames.com/2019-10-9-years-9-lessons-on-horror/) | Anticipation, câu chuyện, vai trò và agency quan trọng; dày scare hoặc hệ thống hút hết chú ý có thể giảm kinh dị | Tách lúc suy luận với lúc thực hiện dưới áp lực; dấu hiệu nguy cơ rõ nhưng danh tính/ý nghĩa còn bí ẩn. Không nhập sanity/battery hoặc làm mơ hồ luật an toàn để ép sợ |

## Kết quả tổng hợp của dự án

Các nguồn không thống nhất rằng tăng độ phức tạp luôn tốt. Điểm cần dung hòa: cho đủ thông tin để lập kế hoạch nhưng vẫn giữ bất định về ý nghĩa; cho tương tác có phản hồi mà không biến toàn game thành thao tác máy; bảo vệ lúc đọc nhưng giữ trách nhiệm khi quyết định đi ra vùng nguy hiểm. Đây là diễn giải của dự án dựa trên RS02/RS05/RS07.

Do đó, baseline3.2 giữ28 puzzle và thêm chiều sâu theo bốn hướng: đồ thị câu hỏi xuyên chương, các lộ trình quan sát hội tụ, mô hình giả thuyết có phản chứng, và tình huống thực hiện có hệ quả nhìn thấy được. P01/P02/P10 vẫn được phép dễ. Chỉ các bàn điều tra cần liên kết có kiểu; các puzzle vật lý biểu đạt suy luận bằng hành động trong world. Không bắt người chơi điền thêm một bảng kết luận sau mọi lần mở tủ.

## Bằng chứng cần thu khi triển khai

Với từng puzzle: người chơi đang cố trả lời câu nào; đã có đủ thông tin nào; thử giả thuyết bằng hành động gì; phản hồi giúp loại khả năng nào; kết quả làm thay đổi mục tiêu/chuyện gì. Theo dõi route đã đi, hint tự yêu cầu, thử sai khác nhau và lý do mắc kẹt. Việc nhìn đúng vật hoặc nhập đúng đáp án không tự chứng minh đã hiểu.

Khi có người chơi thật chưa biết đáp án, quan sát yên lặng rồi hỏi họ giải thích luật; không tuyển người bằng công cụ nhắn tin nếu chưa được yêu cầu. Thiếu người thật ghi HUMAN_USABILITY_NOT_ASSESSED, tiếp tục kiểm bằng agent và runtime với giới hạn đúng. Không chuyển số lần playtest của studio khác thành quota hoặc kết quả cho dự án.

Trace từ nghiên cứu tới yêu cầu có trong `specs/gameplay_reasoning.json`; từng puzzle ghi research_refs. Các trường này là nguồn gợi ý thiết kế, không tự tạo dependency runtime hoặc xác nhận quyền sử dụng asset.
