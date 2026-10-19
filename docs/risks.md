# Rủi ro thực thi đang mở — S01

Nguồn baseline: 08_RISK_REGISTER.md. Bảng là đánh giá hiện tại từ probes/evidence, không thay task_state.json hoặc đóng risk chỉ vì có mitigation.

| Risk | Quan sát thật | Trạng thái / bước xử lý |
| --- | --- | --- |
| RK01 prototype trở thành điểm dừng | Mới có bootstrap; runtime validator PARTIAL,0/7 chapters,0/14 puzzles,0/28 records,0/3 endings | OPEN: tiếp tục Ready theo gates. Không gọi mẫu hình học là game hoàn chỉnh |
| RK02/RK12 native Forward+ GPU | NVS 310 không khởi tạo Vulkan/D3D12; auto fallback vẫn exit0. SwiftShader CPU Vulkan đã tạo render thật | CAP-001 OPEN cho hardware benchmark; functional tests dùng software có metadata/renderer guard; không lấy CPU FPS làm retail spec |
| RK03 art procedural chưa đủ | Chỉ static stool BLOCKOUT đã export/import/render; chưa rig/animation/golden sample | OPEN: agent làm kit và base rig ở task art, REVIEWED/FINAL chỉ sau rubric in-game |
| RK04 audio chưa nghe | Chưa tạo cue/mix hoặc probe playback/loopback | NOT_TESTED: agent sản xuất source/cue tự tổng hợp, metrics rồi playback/capture thật khi tới task; thiếu capability thì chặn phần audio acceptance, không dùng silence |
| RK05 canon thay đổi | Timeline/rules/reveal matrix đã đối chiếu,81 static checks; chưa runtime story | OPEN regression: giữ source Bible/puzzle specs và stable IDs, test skip/load/ending khi modules có thật |
| RK06 false PASS | Đã bắt zero-data complete, exit0 renderer fallback, package leak và runner provider lifetime | MITIGATED cho checks hiện có, vẫn OPEN toàn sản phẩm: hashes/raw logs/counts, self-review, strict coverage và hard gates |
| RK07/RK14 resume/views | Ledger là nguồn duy nhất; handoff checkpoint ban đầu cần cập nhật trước kết thúc phiên | OPEN routine: kiểm Git/disk rồi test trước resume; Excel/HTML không nhập trạng thái độc lập |
| RK08 shared writer | Một agent thực thi tuần tự, agentctl WIP/lock có22 tests | CONTROLLED: tiếp tục một writer, không giả reviewer độc lập |
| RK09 save/world | Chưa có WorldController/SaveService/gameplay; runtime content chưa tạo | OPEN: không nhân rộng puzzle trước G1/G3; giữ transaction/safe support/persistent clues và golden saves |
| RK10/RK11 quyền/chi phí | Asset spike là recipe toán học tự viết; chưa có nguồn third-party/paid trong game. Spend0,publishfalse,không remote | OPEN cho final audit: lưu license/provenance/hash từng nguồn; không suy quyền public/legal từ task tổng quát |
| RK13 feedback giả | Chưa có human playtest | HUMAN_USABILITY_NOT_ASSESSED; scenario bots chỉ là coverage |
| RK15 public blocker làm dừng local | Chưa có store account/quyền upload/public, nhưng local build/test đã chạy | External release giữ riêng; không yêu cầu owner tạo assets, tiếp tục local Ready |
| Rebuild byte identity | Clean source chạy được và EXE hash trùng, PCK khác; source diff chỉ newline | Functional rebuild VERIFIED; bit-for-bit PCK NOT_ESTABLISHED. Không ghi deterministic binary claim; giữ hashes từng candidate |
| Physical device coverage | Keyboard/pad test bằng event mapping, chưa pad/hotplug thật | NOT_TESTED: khi tới gate thiết bị phải dùng hardware và raw record thực; không đổi nhãn synthetic thành physical |

Không có request chi phí, publish hoặc đổi phạm vi. CAP-001 ở state/external_requests.json là queue capability; chưa chặn task baseline đang có đường software/headless hợp lệ. Nếu task tương lai yêu cầu GPU/pad/audio thật mà không có môi trường, claim task rồi block đúng loại, tiếp tục nhánh Ready độc lập nếu gate cho phép.
