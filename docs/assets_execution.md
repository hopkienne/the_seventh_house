# Pipeline art/audio do agent thực thi

## Portable Blender pipeline verified — T-020301

The earlier PATH audit is historical. Blender 4.5.3 LTS now runs locally from the SHA256-pinned portable binary in `config/blender.lock.json`; the archive matches two independently retrieved public mirror checksum lists. Tool license files stay under `.tools/blender/`; the tool is not shipped with the game.

`python -X utf8 tools/art/rebuild_street.py --output-root .qa/street_NEW_ID` creates genuine `.blend`, GLB and semantic metrics in a new directory. Optional `--install` copies the three canonical outputs and regenerates prefab collision IDs; rerun import, tests, captures and manifest hashes after installation. Never reuse an evidence directory. Run the pinned Blender with `--background art/source/blockout_street.blend --disable-autoexec --python-exit-code 1 --python tools/art/verify_street_blend.py` to reopen and independently measure the source.

Street asset `ENV_STREET_BLOCKOUT_01` is BLOCKOUT, static/no rig, metre scale and shared geometry. Provenance, hashes and measurements are in `art/manifest/blockout_street.asset.json`; evidence is under `reports/tasks/T-020301/`. `.gdignore` excludes authoring sources; Godot imports the explicit GLB only. `scenes/environment/street_scale_scene.tscn` integrates the actual player and gameplay camera. REAL/ERASED material previews do not implement phase switching. The opaque exterior roof/walls hide the player once inside from this camera; chapter interior cameras/cutaway remain later integration work. No character rig, final art, GPU performance or whole-chapter acceptance follows from this static pipeline.

Giữ toàn bộ scope v3; không giao sản xuất cho freelancer/owner. Công cụ trả phí mặc định0. Gói hiện có static GLB pipeline spike và bootstrap scene, chưa có final campaign assets/audio. Đây là quyết định workflow của T-010403; sản xuất từng asset/cue ở task backlog tương ứng, không coi tài liệu này là asset hoàn thành.

## Art

Đường mặc định đã probe: Godot 4.7.2 stable → recipe JSON + generator GDScript → GLTFDocument xuất GLB → Godot importer → tests dimensions/normals/UV/material → scene integration/captures → review/rubric → manifest. Spike thật tại tools/art/build_stool_spike.gd và reports/S01/skill_spike.md chứng minh static geometry. Không có random parameters; nếu generator sau dùng random thì seed/config/version phải ghi và rebuild kiểm hash hoặc semantic measurements rõ.

Agent sẽ tạo một street kit, bảy house layouts và khu phụ theo chapter specs; Shared không nhân đôi, phase-specific geometry/query masks theo contract. Source recipe/config/material nằm art/source hoặc tools/art; GLB/material runtime ở art/export và art/materials. Stable IDs, meter scale/feet pivot và collision authored tách visual khi cần. Không hand-edit output rồi bỏ nguồn rebuild.

Minh/An/Knocker và NPC dùng base rig/weights/animation clips do agent tạo; cần idle/walk/run/interact/hide/capture/lantern cùng blend/feet/hand tests trong Godot. Hiện rig chưa probe. Nếu Godot procedural rig không đạt workflow/rubric, agent tự tải portable Blender miễn phí trong .tools, kiểm version/help/hash rồi tạo scripts/source .blend và import GLB. Không yêu cầu owner đi thuê người hoặc tự dựng nhân vật. Không gọi capsule hoặc stool là final character.

Mỗi asset có asset_id/category/chapter_ids/phase/source/runtime paths, generator/config/seed, tool pin/hash, provenance/license, measurements, dependencies và captures. State BLOCKOUT → INTEGRATED → REVIEWED → FINAL; FINAL phải có gameplay/wide/front review và hai phase khi áp dụng. Rubric 03_CONTENT_AND_ASSET_PLAN.md giữ nguyên: silhouette/readability, scale, normals/UV/rig, vật liệu, lối đi/clue, UI occlusion và style nhất quán golden sample. Triangle/texture budgets là guardrail, không chứng minh đẹp. Agent self-review khai rõ, human appeal chưa đánh giá nếu không có dữ liệu.

## Render và profiling

Functional render hiện dùng SwiftShader CPU Vulkan, actual Forward+ có capture, theo ADR-001. ICD chỉ truyền vào subprocess test; không copy browser DLL vào game. Report phải có actual adapter/driver/method/software flag, bỏ false PASS khi auto fallback. Giữ project Forward+ và release Windows x64. Render software có thể kiểm shape/UI/material logic nhưng không dùng FPS/memory trace của nó làm benchmark GPU, minimum spec hoặc final hardware compatibility.

Hardware Forward+ performance đang CAP-001; rig/custom shader/navigation/VFX chưa được thử thì giữ NOT_TESTED/NOT_IMPLEMENTED. Khi task/gate đòi môi trường vật lý mà không có, block đúng loại; không hạ gate hoặc giả metrics. Các task logic/generator/content độc lập vẫn tiếp tục khi dependency cho phép.

## Audio

Đường chọn: Python standard-library deterministic synthesis và foley do agent tạo, thêm library có quyền rõ chỉ khi cần và đã kiểm license. Agent viết tools/audio/build_*.py, recipe/seed và WAV master thực; không tạo cue JSON trỏ vào file không có, không dùng silence để giả ambience. Bell/footstep/wood/cloth/rain/wind/UI/danger và motif ending phải bám cue map gameplay, captions cho thông tin cần thiết.

Master mục tiêu48kHz/24bit, runtime WAV/OGG theo use case và converter đã probe. Generator xuất metrics duration/channels/sample-rate/peak/clipping/silence/loop seam, provenance/source hash và rebuild log. Metrics chỉ là kiểm kỹ thuật. AudioDirector cần Master/Music/Ambience/SFX/UI, volume persistence, ducking/pause cleanup và phase/stealth cues đúng lúc. Agent nghe và capture mix thật khi playback/loopback đã probe; hiện phần nghe/mix NOT_TESTED. Nếu không có capability, giữ task/audio acceptance blocked thay vì ký PASS từ waveform.

Motif tự sáng tác, không clone giọng người thật hoặc sao melody nhận diện. Không full voice acting là scope đã chốt. Nếu bất kỳ nguồn/API cần tiền hoặc quyền tài khoản chưa có thì dùng nguồn tự tạo hợp lệ hoặc ghi permission request cụ thể; không tự chi tiền.

## Quyền và delivery

Lưu source URL/license text/checked_at/attribution/quyền phân phối cho nguồn ngoài; không ghi “free” thay giấy phép. Font phải có glyph VI/EN và quyền phân phối phù hợp. AI/tool output nếu sử dụng cần record tool/model/terms tại thời điểm tạo, không mặc định thương mại. Nguồn quyền chưa rõ phải thay hoặc block release. Local recipe spike không tạo quyền public/publish cho game.

Chapter pipeline: spec + hai puzzle → greybox logic → journal/dialogue → camera/enemy/checkpoint → final model/material/animation → audio/cinematic → save/revisit/capture → rendered walkthrough + rubric → FINAL manifest. Không dồn art/audio toàn bộ sang cuối. Các thiếu hụt và next verification gắn task ID trong ledger/evidence; state và permission queue vẫn do orchestrator một writer cập nhật.
