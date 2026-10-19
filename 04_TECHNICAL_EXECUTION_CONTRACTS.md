# 04 — Technical execution contracts v3

**Đây là interface/behavior phải implement và test, không phải API game đã tồn tại.** Godot API đối chiếu binary pin + tài liệu chính thức trong 07_SOURCES_AND_DECISIONS.md. Không tạo một framework lớn để mô phỏng engine.

## 1. Cấu trúc repository và chuẩn code
```text
project.godot
export_presets.cfg
config/toolchain.lock.json
scenes/main.tscn
scenes/player/player.tscn
scenes/camera/camera_rig.tscn
scenes/levels/CH01/ ... CH07/
scenes/interactables/
scenes/ui/
scripts/core/            # StoryState, SaveService, InputRouter, LevelRouter
scripts/world/           # WorldController, SwitchSafety, PhaseAware
scripts/player/
scripts/camera/
scripts/interaction/
scripts/puzzles/         # P01..P14 controllers/adapters
scripts/characters/
data/chapters/ data/puzzles/ data/dialogue/ data/clues/ data/localization/
art/source/ art/export/ art/materials/
audio/source/ audio/runtime/
tests/test_runner.gd
tests/unit/ tests/integration/ tests/replays/ tests/fixtures/
build_manifest/ reports/ tools/
```
Các đường dẫn trên là target conventions. `plan/`, `specs/`, `tasks/`, `stories/`, `sprints/` là planning inputs, không import toàn bộ vào retail. Không import reports/raw screenshots/Blender sources vào game package. Export runtime JSON/CSV đúng filters [SRC03].

GDScript typed khi phù hợp, snake_case file/function/property, PascalCase class, stable data IDs, const/enums thay magic strings. Signals nối một lần và ngắt khi cần. Không hardcode scene path xuyên module nếu có registry. Fail với message có context/ID; runtime retail không lộ secret/path máy dev.

## 2. Module ownership và interface
| Module | Input/public contract dự án | Output/invariant |
|---|---|---|
| InputRouter | `acquire_lock(reason)->token`, `release_lock(token)`, context GAMEPLAY/UI/CINEMATIC | Token owner rõ; release một lần; pause không rò lock |
| PlayerController | input vector đã normalize, locomotion settings | CharacterBody3D X/Z; không tự đổi world/story/save |
| CameraDirector | `enter_zone(zone_id)`, `restore(zone_id)` | Theo corridor, không đảo screen-left/right khi chuyển zone |
| WorldController | `request_switch(target_phase)->result`, `current_phase` readonly | Nguồn enum duy nhất; signal `world_changed(from,to,transaction_id)` chỉ sau commit |
| SwitchSafety | `validate_pose(pose, capsule, target_phase)->{ok,reason,support_id}` | Không side effect; fail giữ pose/state |
| InteractionResolver | `resolve(player_pose,phase)->target_id?` | Range + facing + LOS + priority; chỉ một target |
| Interactable | `is_available(context)`, `get_prompt_key()`, `interact(context)->result` | Stable ID, không grant item hai lần |
| StoryState | `get_flag(id)`, `apply_event(event_id)`, `snapshot()` | Event idempotent; validate IDs; UI không trực tiếp set story |
| PuzzleController | `apply_action(action)->result`, `snapshot()`, `restore(state)`, `reset_local()` | Solve flag monotonic; wrong answer không reset chapter |
| SaveService | `save_slot(slot)`, `load_slot(slot)`, `get_slot_info(slot)` | Version/schema/backup; không serialize Node/RID/instance IDs |
| StateRegistry | `register(stable_id,component)`, `snapshot_zone(id)`, `restore_zone(id,data)` | ID unique; unloaded scene không mất persistent state |
| LevelRouter | `travel(level_id,checkpoint_id)` | Transaction khóa input→snapshot→load→restore→spawn→unlock |
| CinematicDirector | `play(cinematic_id)`, `skip()` | Xem hết/skip cùng finalize_once; không giữ input lock |
| KnockerController | perception events, phase, authored route | FSM bounded; không đọc player xuyên tường/phase |
| JournalService | `collect(evidence_id)`, `list_records()` | E01–E14/M01–M07/L01–L07 unique; không duplicate rewards |

Autoload tối thiểu: InputRouter, StoryState, SaveService, LevelRouter, AudioDirector. WorldController thuộc active zone; LevelRouter chuyển scene phải rebind listeners. Khi prototype chưa có autoload đầy đủ, dùng adapter nhỏ nhưng giữ interface, không có hai authoritative states.

## 3. Tọa độ, movement và camera defaults
1 unit = 1 m; Y lên, X ngang, Z sâu. Player feet pivot y=0, capsule height=1.70m/radius=0.28m ban đầu. Walk 2.2m/s, run 3.4m/s, acceleration 12m/s², deceleration 16m/s², gravity từ project settings; là initial tuning, không số đã đo. Hành lang sâu khoảng 3–4m; real physics bounds cả X/Z. Đi chéo không nhanh hơn thẳng >5% trong bài test 5 giây. Không jump.

Camera nhìn từ một phía corridor, initial FOV 38°, offset và look target là Resource per zone. Không băng qua mặt phẳng đảo chiều điều khiển. Interpolate bằng delta; test 30/60/120FPS. Cinematic có safe frame cho 16:9/16:10; ultrawide crop/letterbox được định rõ, không lộ ngoài set. Foreground fade không làm biến mất vật cản gameplay chưa có cue.

Input actions: move_left/right/forward/back, run, interact, toggle_lantern, journal, pause, hint, debug_overlay. Initial keyboard A/D/W/S, Shift, E, Q, J, Esc, H, F3; UI dùng ui_accept/ui_cancel/ui directions. Mapping gamepad theo action, không tên nút bằng text hardcode; gamepad vật lý và synthetic injection là hai evidence mode khác nhau.

## 4. Collision layers — index khác bitmask
| Layer index | Bitmask | Ý nghĩa |
|---|---:|---|
| 1 | 1 | SHARED static world |
| 2 | 2 | REAL-only static world |
| 3 | 4 | ERASED-only static world |
| 4 | 8 | Player |
| 5 | 16 | Shared gameplay props, nếu được cần |
| 6 | 32 | Trigger/switch/zone areas |
| 7 | 64 | Interaction areas |
| 8 | 128 | Enemy bodies |

Player mask REAL = 1|2|16, ERASED = 1|4|16. Không mặc định va cứng với enemy; capture dùng perception/area khi thiết kế yêu cầu. Static phase colliders **giữ queryable**, kể cả phase đang ẩn; mask của active bodies/raycast chọn đúng lớp. Không tắt collider phase đích rồi query một thế giới rỗng. `visible=false` không đổi physics. Không dùng dynamic phase props ở P0; thêm sau chỉ với contract/test rõ.

Các trigger/interactable có `phase_membership` và resolver lọc theo authoritative phase. Physics layer chỉ là một phần lọc, không thay availability. Shared geometry không được nhân đôi trong hai phase. LOS/safety queries dùng target phase mask, exclude player RID và sensors không có nghĩa là vật cản.

## 5. World switching transaction
Trạng thái IDLE → VALIDATING → COMMITTING → PRESENTING → IDLE. Request đang Busy bị reject. Khởi đầu chưa có đèn trả NO_LANTERN. Bị cinematic/story lock trả STORY_BLOCKED; pause/loading trả BUSY. Unsafe trả UNSAFE_OVERLAP hoặc NO_SUPPORT. UI map reason thành key, không tự đổi logic.

Preflight tại physics-safe boundary: giữ pose/velocity/phase/transaction_id cũ; kiểm capsule đúng target mask tại pose hiện tại, dùng clearance epsilon để tiếp xúc sàn hợp lệ không bị xem là xuyên tường; kiểm wall/door overlap; kiểm support bằng center + mẫu chân. Default cần center và ít nhất 3/5 samples có sàn cùng vùng hợp lệ, slope trong floor_max_angle, không drop/step quá mức cấu hình (ban đầu drop 0.10m, step 0.20m). Dốc/biên còn mơ hồ thì fail-safe và đặt switch anchor được thiết kế, không relocate bí mật.

Commit chỉ sau validation thành công: khóa input token → đổi active body masks và phase data → sync visibility/interaction/enemy nav/audio → publish một world_changed → feedback visual/audio → unlock. Với updates cần deferred/physics frame, giữ transition lock tới khi tất cả participant acknowledge; timeout rollback snapshot. Không ghi save half-state. Game paused/focus lost phải resume hoặc rollback có quy tắc, không rò lock.

Tests: 200 switches, 20 fixed poses an toàn/unsafe, thiếu floor, contact sàn, góc tường, cửa đóng, same-phase no-op, Q spam, pause/focus, capture, request trong load, collider inactive vẫn query được. Assert rejected không đổi pose/flags/inventory. Không teleport để chữa switch.

## 6. Scene template / data protocol
```text
ChapterRoot(Node3D)
  Shared(Node3D)
  RealVisuals(Node3D)
  ErasedVisuals(Node3D)
  PhaseCollision(Node3D)   # colliders giữ queryable với layer phù hợp
  Actors(Node3D)
  Interactions(Node3D)
  Checkpoints(Node3D)
  CameraZones(Node3D)
  WorldController(Node)
  ChapterController(Node)
```

Chapter ID canonical **CH01…CH07**, house H01…H07, puzzle P01…P14, evidence E01…E14/M01…M07/L01…L07. V2 `H02_E03` là alias migration, không thêm journal entry mới. Định danh component persistent dạng `CH02.table_layout`; không dùng NodePath làm save key. Validate duplicate keys/IDs và dependency cycles trước import content.

Dùng JSON cho story/puzzle/evidence/dialogue catalogs, Resource cho tuning kỹ thuật. Spec schemas ở `specs/schemas/`. Nếu chọn Resource runtime, tạo converter và semantic equality test; không để JSON doc và Resource thật lệch nhau. Không nạp global flags từ file tùy ý ngoài allowlist. Lời giải/hints theo puzzle specs, không regenerate ngẫu nhiên từng lần load.

## 7. Save contract
3 slots, settings tách profile. Autosave tại safe checkpoints; request save khi switch/cinematic/level load xếp hàng hoặc báo deferred, không snapshot transaction dở. Snapshot schema trong `specs/schemas/save.schema.json`; có schema_version/build_version, slot/chapter/level/checkpoint, player position/rotation_y, phase, story_flags, inventory, journal_ids, puzzle_states, completed_cinematics, zone_states.

Write temp trong cùng thư mục → flush/close → validate parse/schema → tạo backup hợp lệ của bản trước → replace bằng cơ chế target OS kiểm chứng. Không overwrite backup bằng file corrupt. Permission/disk-full báo lỗi UI thực; không display Saved khi fail. Unknown future schema từ chối không reset mất dữ liệu; recovery dùng backup hoặc cho người chơi chọn, log rõ.

Load order: lock → read/validate/migrate → load scene → apply registry/story/puzzles/phase → chọn checkpoint/pose có support → activate player/enemy → restore camera/audio/UI → unlock. Enemy restore về authored safe state để không capture ngay tại spawn, không serialize navigation server handles. Repeated load/skip không duplicate clue/cinematic/reward. Data checksum chỉ phát hiện thay đổi, không được gọi là chống gian lận/bảo mật.

## 8. Cinematic / narrative / enemy
Cinematic definition gồm beat IDs, ordered actions, skip target và finalization event. `finalize_once` chịu trách nhiệm các flags bắt buộc. Optional evidence không grant chỉ vì skip. Chia camera/dialogue/audio thành actions có timeout và cleanup. Nếu lỗi load resource, rollback về checkpoint an toàn, có report.

Knocker ban đầu dùng routes authored và NavigationAgent3D khi geometry cần; không viết planner tổng quát. Chuyển world cập nhật perception/path qua event; không cache player target xuyên phase. Capture return safe checkpoint, giữ journal evidence đã commit. Puzzle fail và enemy capture là hai trạng thái riêng.

## 9. Testability và build
T-010401 tạo `tests/test_runner.gd` kế thừa SceneTree, đọc `--suite`, report count/failed/skipped, exit non-zero khi lỗi hoặc suite không tồn tại. **`godot --test` là engine tests, không phải test runner của game** [SRC08]. Test phải gọi implementation thật, không hardcode đáp án vào fake solver chỉ dùng cho test.

Debug replay được phép spawn fixtures hoặc save stage cho unit/integration. End-to-end phải dùng input actions/interaction thật; không gọi `set_flag('ending_done')` để chứng minh chơi xong. Tách export debug/retail; retail không có debug commands mở khóa ending.

Pin editor/export templates/version/hashes; export binary vào thư mục có build manifest. Import success không thay executable smoke. Include runtime data filters; exclude secrets/.godot caches/source assets/reports. Không thêm Steam SDK/plugin nếu chỉ cần phân phối.

## 10. Performance
Target thiết kế: 1080p Medium 60FPS trên benchmark hardware thực được chốt và ghi ở S02/S10; chưa có minimum spec quảng bá. Đo P50/P95/P99, CPU/GPU/memory/scene load, không lấy FPS headless làm kết quả. Initial G7 target P95≤20ms trên tuyến benchmark; ngưỡng sửa được bằng ADR trước public claims, không hạ sau đo để che regression. Chỉ hai phase của zone đang chơi resident, Shared dùng chung, LOD/lighting/VFX budget theo profiler. P95 chưa đạt thì tối ưu có evidence, không đổi engine tùy tiện.
