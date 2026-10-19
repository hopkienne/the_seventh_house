# ADR-003 — Suy luận, liên kết và kịch tính / gameplay 3.2

Ngày 19/10/2026. ACCEPTED cho cập nhật thiết kế local theo yêu cầu chủ dự án. Kế thừa ADR-002, giữ 28 puzzle,7 chương,28 journalrecords,3 ending, engine/canon và các ranh giới quyền. Không phải cập nhật game runtime đã hoàn thành.

## Quyết định

1. Mỗi chương có câu hỏi điều tra, điểm gắn bó với nhân vật, nhánh quan sát có mục tiêu và một kết luận làm đổi cách hiểu tình huống. Các ID P01–P28 giữ nguyên; mỗi card có hypotheses, thought_path, observation_routes, feedback, knowledge links, tension và payoff cụ thể.
2. Giả thuyết chủ yếu là công cụ authoring. P07/P15/P17/P19/P23 dùng proof board có liên kết giới hạn; các puzzle khác cho người chơi chứng minh bằng hành động world. Không thêm 28 bảng điền đáp án hoặc parser văn bản tự do. Đọc clue không là khóa vô hình; đáp án hợp lệ được chấp nhận nếu đủ điều kiện vật lý/evidence cần thiết.
3. Quan hệ tri thức khác dependency vật lý. Kxx mô tả luật được học, không là currency/collectible hoặc điều kiện phải bấm xác nhận đã hiểu. Clue mới không được grant tri thức về chương tương lai. Callback chỉ phát khi có provenance và chapter guard.
4. Đồ thị puzzle được nới: CH02 P05/P06 độc lập rồi hội tụ P07; CH03 P09/P11 cùng bờ trước P10; CH05 P17/P19 trước P18; CH07 P25/P26 có thể giải theo hai thứ tự nhưng P28 cần cả hai. P04/P08/P16/P24 có thể bắt đầu sớm hơn ở nhánh đã mở. Cập nhật vị trí, key use, actions và dependencies tương ứng, không chỉ sửa sơ đồ trên giấy.
5. P06 vào phòng qua ERASED/Shared khi chưa có chìa P05; chìa mở shortcut REAL. P11 console và vết bùn ở cùng bờ A để không bị khóa bởi cầu P10. P19 mô hình/nhật ký thường tiếp cận từ entry CH05; P17 kiểm thư dẫn phòng kín, P18 dùng kết quả của cả hai. Mọi nhánh có đường về/checkpoint an toàn.
6. Một số tình huống có nhiều lời giải được kiểm chứng: P04 hai vị trí mồi khả dụng, P16 hai tuyến cửa sau, P28 tám kế hoạch sơ tán hợp lệ theo thứ tự nhóm và tình trạng thư viện. Không buộc lặp lại đúng thứ tự walkthrough duy nhất. Các mã/cơ cấu cần đáp án xác định vẫn có thể giữ một cấu hình đúng.
7. Kịch tính theo anticipation→commitment→aftermath, có khoảng nghỉ. Closeup chỉ mở ở safe boundary và dừng danger advancement; Warn/Chase chặn mở mới. Không có timer trừng phạt việc đọc. Tại P28, crossing committed tăng water beat; preview báo thư viện sẽ mất an toàn sau lần chuyển nhóm đầu. Lối gallery cao luôn còn; sai có retry trước quyết định, giữ nhóm đã an toàn và clue.
8. P27 chỉ plan; P28 thử plan, đưa 3 nhóm an toàn, rồi mới validated/final C. HOLD và OPEN trước chuyển nhóm, RETURN sau tất cả. A/B có hậu quả canon và vẫn là kết thúc hợp lệ; không coi chúng là lỗi logic hoặc thêm cái giá C mới.
9. Source research chỉ là desk research có nguồn sơ cấp/đối thoại tác giả. Không tuyên bố đã chơi game tham chiếu, sao chép asset hoặc bảo đảm market fit. Playtest người thật vẫn NOT_ASSESSED nếu chưa có dữ liệu.

## Production và tương thích

Thêm 4 task NOT_STARTED: T-070211/212 cho proof/provenance và lộ trình quan sát; T-080405 cho tension/encounter thực; T-250205 cho decision model sơ tán. T-070210 chờ hai task hệ mới; các task phụ thuộc story nhận thêm task mới. G2 vẫn chặn nhân rộng; kiểm cả thứ tự khám phá hợp lệ và retry dưới áp lực, không nâng gate từ static PASS.

Plan/save design_version sang 3.2; giữ mọi trạng thái task/gate trước đó. Save 3.1 chưa có campaign runtime được sản xuất ở thời điểm đổi thiết kế; không tự diễn giải solved flags khi dependency/layout/valid solution đã đổi. Giữ bản gốc, từ chối import không hỗ trợ và kiểm migration riêng trước khi hỗ trợ. Không xóa hoặc sửa evidence đã đóng.

## Kiểm chứng

Static checks phải kiểm nguồn/refutation tồn tại, route không dùng clue chưa mở, teacher main cho luật dùng ở main, callback không spoil, DAG và không main→secret; finite models kiểm seating, thứ tự, routes, letters và tám kế hoạch C. Fixtures chỉ kiểm consistency thiết kế. Runtime phải kiểm UI không tự solve, phản hồi không làm lộ từng ô, phase/LOS an toàn, cả đường quan sát và cách giải được chấp nhận, save partial, once effects và action preview đúng trạng thái. Độ khó/cảm xúc chỉ kết luận từ bằng chứng phù hợp.

Điều kiện vật lý và thông tin: P10 nhận thông tin từ P09/P11 nhưng không kiểm hai solved flags để cho qua cầu; giải sớm hợp lệ vẫn được nhận, chapterexit cần cả ba. P18 thực sự cần cửa phòng từ P17 và kính từ hộc mô hình P19; nguồn REFLECTOR được chuyển sang P19. Đây không là yêu cầu phải click đọc đủ clue.
