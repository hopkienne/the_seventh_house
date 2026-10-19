# Reveal và ba ending — production contract

Nguồn: Story Bible v3, chapter/evidence catalogs, `specs/evacuation_route.json` và P28. Bảng định nghĩa nội dung cần phát; chưa tuyên bố đã tích hợp cinematic runtime.

| Chương | Được reveal | Cấm reveal sớm | Điều kiện/đoạn phát |
| --- | --- | --- | --- |
| CH01 | Nhà/người bị quên, vật chứng còn; Minh nhớ trước đèn; áo vàng xa. M01 là nét route đầu tiên. | Không gọi An là em, không nói cô 21 tuổi hay giải máy chuông. | E01/E02 trong route chính; M01 chỉ khi thật sự thu. |
| CH02 | Tình thân còn trong thói quen; M02 chỉ đường qua sân bà Liên. | Không giải cơ chế chuông hoặc điểm neo. | P05/P06/P07 và quan sát bát/vết chiều cao; M02 optional. |
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

## Ma trận lựa chọn 3.1

`mechanism_ready = p25_solved AND p26_solved`; `main_ready = mechanism_ready AND an_identity_revealed`. Panel P28 không cần P28 solved hoặc credits trước khi mở.

| Điều kiện | A/B | Thử tuyến C | Xác nhận kết thúc C |
| --- | --- | --- | --- |
| Chưa main_ready | Chưa | Chưa | Chưa |
| Main_ready, thiếu M hoặc P27 chưa giải | Có | Chưa; chỉ rõ điều còn thiếu và cho revisit | Chưa |
| Main_ready, đủ7M, P27 tạo route_plan_ready | Có | Có, vào bản ghi trước return-time | Chưa |
| Ba nhóm an toàn, evacuation_route_validated sau P28 trial | Có trước final confirmation | Có thể xem/kiểm lại | Có |

P27 là ghép kế hoạch; không đặt evacuation_route_validated. P28 trial vận dụng M03 chọn HIGH_RAMP, M04 chọn thư viện/cổng sau với chìa record, M02/M05 chọn sân cao và cơ cấu cổng1→3→2. Nước tăng theo quyết định có cue, không khi đọc hoặc pause. Sai trả checkpoint trước quyết định, giữ M/E và không forcedB. Ba nhóm phải tới đồi rồi mới cho finalconfirmC.

| Ending | Resolution phải chơi | Hậu quả | Credits/checkpoint |
| --- | --- | --- | --- |
| A — Điểm neo mới | Minh dùng dấu khởi động thay An | An21tuổi; Minh bị quên; chu kỳ mới, món nợ còn | Checkpoint trước confirmation; credits reachable |
| B — Trả lại thời gian | Giải thể chuông và dùng tuyến mặc định | Minh9/An6 giữ ký ức; có nhóm không thoát; epilogue15năm sau24/21 tưởng niệm | Không tự phát cảnh cứu tất cả của C |
| C — Bình minh thật sự | Lập kế hoạch, kiểm chứng ba nhóm, xác nhận trả thời gian | Minh9/An6 và các nhóm trở về đêm lũ theo tuyến đã chuẩn bị; epilogue24/21; không hứa mẹ bất tử | Trial có retry, credits sau resolution |

Đưa nhóm trong trial là thao tác với record trước khi trả thời gian, không đưa người trưởng thành vào lịch sử thực. Chỉ finalcommit mới đổi lịch sử và cơ thể. Unknown/duplicate memory IDs không bù fragment thiếu. C không phải một nút thưởng khi đủ7mảnh.

## Persist, skip và chống miss vĩnh viễn

- E01–E14 commit từ các puzzle chính theo source_puzzle trong catalog; P23 thu E12 tại entry trước xác nhận, không tự phụ thuộc reward sau solve.
- M01..M06 từ SECRET sáu chương đầu; M07 từ P25 main. Thiếu secret không khóa A/B; trước final confirmation có revisit, không reset puzzle đã giải.
- View/skip chỉ commit presentation và identity flags bắt buộc tương đương xem hết. Không auto-grant M, route plan hoặc route validation.
- Save giữ slots/angles/links, plan, selected ending, group decisions, safe groups và confirmation; reload không duplicate/replay unsafe.
- Kiểm128memory masks cùng identity/mechanism_ready/plan/validated và8group masks, gồm các state không thể tới bằng main để kiểm corrupt/debug guards. Chỉ khi đủ mọi điều kiện mới finalC. Static table không thay ba full rendered ending runs.

## Gameplay3.2 / ADR-003
P28 chấp nhận mọi thứtự ba nhóm khi tuyến phùhợp beat: trường qua thưviện ởbeat0 hoặc gallerycao ởbeat0/1/2, tổngtámplan. Preview trước crossing; reading/pause không tăngnước; sai giữnhómđãsafe. GIỮ/MỞ/TRẢ của lõi khác cần1/3/2 ởcổngsân. P27chỉplan;3nhóm+validationrồimớifinalC. MainreadyvẫnP25/P26+identity; A/Bkhôngcầnsecret. Các lối khác nhau không thêmending/nhà hoặc đổi tuổi/canon.
