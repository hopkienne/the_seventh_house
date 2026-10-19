# 05 — QA, quality gates và ổn định sản phẩm

## Mức evidence
| Mức | Được xác nhận | Không được suy ra |
|---|---|---|
| Artifact review | Doc/schema/content/license manifest đúng yêu cầu | Game chạy hoặc người chơi thích |
| Headless unit/integration | Logic, data, IDs, serialize, conditions, physics assertions nếu có engine | Camera, audio, GPU performance, Windows executable |
| Rendered replay | Hình/UI/interaction/cinematic/AI và state trong runtime có render | Người thật hiểu/thích; gamepad vật lý nếu chỉ inject |
| Native Windows smoke | Bản .exe cài/chạy ngoài editor trên Windows thật | Mọi cấu hình phổ biến đều tương thích |
| Physical-device check | Pad/hotplug/focus trên thiết bị thực được log | Tất cả model pad hoặc hệ điều hành |
| External platform | Upload/approval/public status từ platform thật | Phê duyệt pháp lý tổng quát/khả năng bán |

Không biến bot scenario thành người dùng; số profile là coverage của scenarios, không sample size nghiên cứu. Human playtest không phải dependency sản xuất bắt buộc trong mô hình agent-only; thiếu dữ liệu đó phải ghi `HUMAN_USABILITY_NOT_ASSESSED`. Agent quality rubric giảm lỗi nhưng không bảo đảm chất lượng cảm xúc/market fit.

## Acceptance suites
Build: clean checkout/import/export, runtime data include, no editor cache/secrets/debug unlocks. Movement: straight/diagonal, wall/slope/depth bounds, FPS delta. Camera: zones/cuts/focus/aspect/large-text occlusion. Switch: body overlap + support, inactive colliders query, reject invariants, spam/pause/load/capture. Interaction: range/LOS/phase/priority/idempotency. Puzzle: đúng/sai/action order/all persistent states/reset/revisit. Save: 3 slots, corrupt main→backup, both corrupt, unknown schema, write failure, migration/rollback, no duplicate rewards. Cinematic: skip từng beat/focus loss/save request; final flags same. AI: perception/phase/hide/search/return/capture safe. UI/LOC: key parity, Unicode Vietnamese, captions, 100/125/150%, keyboard/pad focus. Content: 7/14/7/28/3 inventory và end-to-end. Release: native Windows + RC hashes + real permissions.

P01–P14 mỗi puzzle cần happy-path, wrong-input, replay/reload và exploit test ghi trong spec. Ending unit suite enumerate toàn bộ 128 memory masks: A/B vẫn accessible sau main route, C iff đủ 7 + reveal + route validated; không cho optional lore thay memory. Sau đó ba full rendered runs từ checkpoint hợp lệ và ít nhất một campaign run New Game→credits không set flags giả.

## Test runner và reports
T-010401 triển khai game test runner. RUN-TEST lệnh dự kiến chỉ hợp lệ khi file đó tồn tại; không có runner thì NOT_TESTED. Explicit exit code, discovered/executed/passed/failed/skipped counts; suite không tồn tại/0 tests là FAIL. Timeout/crash logs giữ lại. Screenshots/clip/log có timestamp/build/hash và profile ID. Tool control nội bộ của game chỉ được dùng trong test build, không retail.

Năm profile G1: main route; đi vòng/ngoài Z; Q/E spam; checkpoint/reset; keyboard-only no-audio cues. Tám profile G2: main route, optional explore, no audio, large text, synthetic pad, pause/focus, stealth capture, replay/continue. Physical pad QA ghi riêng. Đừng viết bot đọc trực tiếp answer JSON rồi kết luận hint dễ hiểu; đánh giá hint là review riêng có giới hạn.

## Severity và chặn release
Sev-0: mất/corrupt save nghiêm trọng, security/privacy exposure. Sev-1: crash tái hiện, softlock main route, ending không hoàn tất. Sev-2: lỗi đáng kể có workaround, visual/audio/UX ảnh hưởng. Sev-3: polish nhỏ. G7_TECH không có Sev-0/1. Sev-2 phải nêu cụ thể ảnh hưởng/workaround/retest/risk; không dùng acceptance chung để bỏ lỗi bắt buộc. QA có quyền trả task về rework dù code compile.

## Benchmarks
Tạo routes cố định đo 1080p Medium trên CPU/GPU/RAM/OS/driver ghi thật; record warmup/sample duration/load states, P50/P95/P99 và memory growth. Không dùng FPS khi headless, minimized hoặc capture tool đang throttle mà không ghi điều kiện. Soak lặp load/switch/chapter/ending và kiểm logs/memory trend; chỉ đo phiên đã thực chạy. Không tự lập minimum hardware chưa có dữ liệu.

## Gate close
Đọc `plan/backlog.json:gates`. Evidence cho từng gate phải tham chiếu task artifacts cùng candidate. G4 là đủ nội dung, không phải release ready. G5 text lock; G6 feature lock; G7 RC hash không đổi sau signoff mà không retest delta. G7_PUBLIC cần authorization và platform state; technical reviewer không tự ký thay.

## Hypercare agent-only
Intake theo phiên: đọc report được quyền → deduplicate → reproducer → severity → fix→tests→release candidate→authorize external patch. Không có report thật thì ghi NO_ISSUE_REPORTED, không tạo issue giả. Conditional hotfix tasks NOT_APPLICABLE có report/review nếu không cần; don't bypass main feature. Không theo dõi nền hoặc trực 24/7 trừ hạ tầng scheduler đã thật sự được cấu hình/được cấp quyền. Maintenance backlog tách khỏi Full Game 1.0, giữ source/save compatibility policy.
