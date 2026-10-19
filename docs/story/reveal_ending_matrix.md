# Reveal và ba ending — production contract

Nguồn: Story Bible v3, chapter/evidence catalogs, `specs/evacuation_route.json` và P14. Bảng định nghĩa nội dung cần phát; chưa tuyên bố đã tích hợp cinematic runtime.

| Chương | Được reveal | Cấm reveal sớm | Điều kiện/đoạn phát |
| --- | --- | --- | --- |
| CH01 | Nhà/người bị quên, vật chứng còn; Minh nhớ trước đèn; áo vàng xa. M01 là nét route đầu tiên. | Không gọi An là em, không nói cô 21 tuổi hay giải máy chuông. | E01/E02 trong route chính; M01 chỉ khi thật sự thu. |
| CH02 | Tình thân còn trong thói quen; M02 chỉ đường qua sân bà Liên. | Không giải cơ chế chuông hoặc điểm neo. | P03/P04 và quan sát bát/vết chiều cao; M02 optional. |
| CH03 | Nước từng tới làng; M03 có điểm tập kết lên đồi. | Không xác nhận ai là điểm neo. | E05/E06 và M03 khi thu; không bắt thu M03 để qua chương. |
| CH04 | Làng bị hủy 15 năm trước, danh sách lớp có chỗ trống; nghi chuông. | Không giải hết vai trò mẹ/Minh/An. | E07/E08; trường là khu phụ H04. |
| CH05 | Mẹ duy trì thời gian vay; có một người ở lại. | Chưa xác nhận khuôn mặt/tuổi An. | E09/E10 và nhật ký đã đọc; mẹ suy ra từ records, không miễn nhiễm. |
| CH06 | An là em Minh, tuổi 21; Minh kích hoạt trước, mẹ duy trì; giá của neo. | Không tự giải route C thay người chơi hoặc grant memory còn thiếu. | E11/E12 và identity reveal transaction. |
| CH07 | Cơ chế/giá A/B/C; chơi route sơ tán, quay lại fragment trước xác nhận. | Không thêm luật cứu tất cả ngoài đủ memory và route đúng. | Main route xong; confirmation riêng, checkpoint trước lựa chọn. |

## Dấu báo trước tuyến C ở ba chương đầu

| Key | Text VI | Quan sát/điều kiện | Once flag |
| --- | --- | --- | --- |
| story.route.ch01.sketch | Nét vẽ này bắt đầu từ lối trước nhà, rồi rẽ sang con ngõ đối diện. | M01 collected; cạnh H07_FRONT → H01_LANE | route_hint_m01_seen |
| story.route.ch02.stitch | Đường chỉ đi qua sân bà Liên. Nó nối tiếp nét vẽ trong trí nhớ. | M02 collected và M01 collected | route_hint_m02_link_seen |
| story.route.ch03.assembly | Điểm tập kết nằm trên đường lên đồi. Những dấu này có thể nối lại. | M03 collected và ít nhất M01 hoặc M02 collected | route_hint_m03_link_seen |

Nếu M02/M03 thu trước M01, journal vẫn giữ từng đoạn; khi revisit/thu đoạn còn lại, điều kiện nối được đánh giá lại để phát gợi ý còn thiếu đúng một lần. Không chặn main nếu thiếu gợi ý. M01 tự báo một phần tuyến, M02/M03 cho ít nhất hai dấu cụ thể về đường nối/sơ tán; không tiết lộ người neo hoặc toàn bộ lời giải. Text mô tả cạnh đã có trong catalog, không tạo cơ chế mới.

## Ma trận lựa chọn

Trong bảng này, “main xong” nghĩa là `main_p13_solved=true` và reveal CH6 đã được commit, đủ mở panel P14; không yêu cầu `p14_solved` hoặc credits trước khi được chọn ending. Đây là boundary trước resolution, tránh dependency vòng.

| Điều kiện tại final decision | A | B | C |
| --- | --- | --- | --- |
| Main route chưa xong | Chưa chọn | Chưa chọn | Chưa chọn |
| Main xong; thiếu bất kỳ M01–M07 | Có | Có | Chưa; chỉ rõ fragment còn thiếu, cho quay lại |
| Đủ M; chưa identity reveal hoặc chưa validate route | Có | Có | Chưa; hoàn thành điều kiện còn thiếu |
| Main xong; đủ M; an_identity_revealed=true; evacuation_route_validated=true | Có | Có | Có |

Main route đã bao gồm reveal CH6; hàng identity=false vẫn là negative case cần bảo vệ khi load/debug. C không chỉ kiểm memory count: phải đúng tập ID và route validated. Unknown IDs hoặc duplicate không được bù memory thiếu. Route lưu đúng cạnh/trình tự theo `specs/evacuation_route.json`, không dùng teleport. P14 phải đưa ba nhóm đại diện qua route, có checkpoint/retry. Lỗi thao tác route C không tự chọn B, không xóa memory.

| Ending | Resolution phải chơi | Hậu quả | Credits/checkpoint |
| --- | --- | --- | --- |
| A — Điểm neo mới | Minh thay An bằng dấu khởi động | An 21, Minh bị quên, chu kỳ mới; ảnh trống/đèn sáng, nợ chưa hết | Checkpoint trước confirmation; credits reachable |
| B — Trả lại thời gian | Giải thể chuông, quay về đêm lũ | Cơ thể Minh 9/An 6 giữ ký ức; tuyến mặc định làm một nhóm không kịp; epilogue 15 năm mới ở 24/21, tưởng niệm | Cùng boundary lựa chọn; không hiện cứu tất cả của C |
| C — Bình minh thật sự | Đóng chốt đúng trình tự, đưa ba nhóm qua tuyến từ 7 memory rồi trả thời gian | Cứu các nhóm của làng; epilogue 24/21 nhìn bình minh; không hứa mẹ bất tử | Route failure retry checkpoint; credits sau resolution |

## Persist, skip và chống miss vĩnh viễn

- E01–E14 là essential, commit theo puzzle route chính, idempotent. Capture không xóa records; checkpoint không rollback kiến thức đã commit.
- M01–M07 optional cho A/B, không permanently missable; trước final confirmation phải có đường trở lại các fragment đã mở. L01–L07 không bị tính nhầm thành memory eligibility.
- View/skip cinematic phải đặt cùng final flags; không tự đánh M collected hoặc route validated. Once flags là presentation, không thay gameplay eligibility.
- Save/load trước/sau choice, identity reveal và từng group checkpoint phải giữ cùng trạng thái. Cần test runtime ở task hệ thống tương ứng; document review hiện tại chỉ kiểm contract.
- 128 tập con memory × identity false/true × route false/true × main false/true là 1.024 tổ hợp eligibility phải kiểm: A/B chỉ theo main; C theo conjunction đủ điều kiện. Final QA còn cần run/capture từng ending thật.
