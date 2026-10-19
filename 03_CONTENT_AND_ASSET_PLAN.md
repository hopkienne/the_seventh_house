# 03 — Content & asset pipeline dành cho agent

## Trách nhiệm
Agent tạo **file nội dung thực dùng trong game**: model/rig/animation/material, cue/soundscape/music, dialogue/translation, UI, cinematic. Không giao đầu ra cho freelancer, không đánh DONE với brief/prompt/render mockup. Công cụ sinh tài nguyên có thể hỗ trợ nhưng không được giả định sẵn; kiểm capability trước. Không cần tạo tất cả assets trước prototype; sản xuất theo chapter và golden sample.

## Inventory đã khóa
7 chapter specs `specs/chapters/CH01.md`…`CH07.md`; 14 puzzle specs; 28 journal records trong `specs/evidence_catalog.json`. Main characters: Minh, An, Knocker; NPC phụ dùng chung base rig và biến thể silhouette/outfit. Một street kit + 7 layout nhà + bến/trường/tháp/đồi, không 7 kit hoàn toàn riêng. Mẹ chủ yếu qua ảnh/nhật ký/âm thanh; flashback trẻ dùng silhouette có chủ đích, không bỏ cảnh cần thiết.

## Art direction và recipe bắt buộc
| Loại | Cách agent thực hiện | Kiểm chứng |
|---|---|---|
| Environment modular | Blender Python tạo wall/roof/window/door/fence/ground, UV/material, deterministic seed; ghép layout bằng config | GLB trong Godot; scale/pivot/LOS/collision; screenshot camera |
| Minh/An/Knocker | Stylized silhouette distinct, mesh topology đủ cho rig, source + skeleton + reusable animation clips | Walk/run/idle/interact/hide/capture/lantern poses trong engine |
| NPC | Base rig và biến thể trang phục/tỷ lệ hợp lý, không đổi nhận dạng ở hai phase | Dialogue camera và shared animation |
| Materials | PBR đơn giản hoặc custom shader nhỏ, texture tự tạo/provenance rõ; REAL/ERASED overrides | Không z-fighting, không chữ clue bị che, màu không là cue duy nhất |
| VFX | Fog/rain/dust/dissolve/water beat có budget; reduced effects switch | Capture trước/sau; pipeline render thật không black frame |
| UI | Godot Control-based; icons vector/tự tạo theo glyph set | Keyboard/pad focus, large text, VI/EN |

Blender CLI/script là một đường sản xuất; chính agent phải tạo `tools/art/build_*.py`, input config và output manifest rồi chạy. Source `.blend` và scripts lưu riêng, game nhập GLB [SRC02]. Nếu Blender không sẵn, ưu tiên cài binary theo quyền local hoặc tạo geometry bằng Godot tool script và export khi phù hợp. Model procedural vẫn phải qua cùng art rubric; không gọi capsule đơn giản là nhân vật final.

## Asset definition và trạng thái
Record: asset_id, category, chapter_ids, phase, source_path, runtime_path, generator_path/config/seed, tool_version, source_url/license_id/license_text_path, provenance_kind, content_hash, measurements, quality_state, captures, dependencies. `quality_state`: BLOCKOUT → INTEGRATED → REVIEWED → FINAL. FINAL chỉ khi hiện trong gameplay, source tái tạo được, license rõ và visual review pass. Mọi alias/import rule ghi một chỗ, không hand-edit mesh runtime mà quên source.

Initial budgets là guardrail để bắt đầu profiling, không tiêu chuẩn Godot: main character ~5–15k triangles, common prop 100–2k, textures 512–2048 theo screen size; đo draw calls và memory thực, không coi đủ polygon là đẹp. World phase duplicate geometry chỉ nơi cần khác topology; ánh sáng/ambient khác không cần nhân đôi kit.

## Visual rubric cho agent reviewer
Kiểm ít nhất front/gameplay/wide frames và hai phase. Pass khi silhouette Minh đọc được nền, lối đi/interactive clues thấy rõ, scale nhất quán, chất liệu không ngẫu nhiên, normals/UV/rig/feet/hand-lantern không lỗi nghiêm trọng, UI không che clue, art style nhất quán golden sample. Lưu cả lỗi và vòng sửa; không tự cho 10/10 vô chứng cứ. Thẩm mỹ/hấp dẫn người thật chưa được xác nhận nếu chỉ agent đánh giá.

## Audio production
Agent tạo cue map từ sự kiện gameplay trước. Shared cues: bước chân theo bề mặt, door/key/inspect/UI, switch success/reject, bell triplet, Knocker warning/chase/capture. Mỗi CH có ambience REAL/ERASED và tension layers; CH5 yên hơn, ending motif khác nhưng cùng chủ đề.

Dùng synthesis/foley/library có quyền. Tự tạo `tools/audio/build_*.py` hoặc project nguồn; record seeds/sample provenance. WAV master 48kHz/24bit định hướng; runtime OGG/WAV theo use-case. Đo peak/clipping/silence/loop seam, sau đó kiểm **mix trong game**. Synthesis test không thay nghe/capture audio thực. Không có voice acting toàn bộ là scope đã chốt; không tự clone giọng người thật. Motif nhạc tự sáng tác hoặc dùng nguồn được phép, không bắt chước melody nhận diện của tác phẩm khác.

AudioDirector buses Master/Music/Ambience/SFX/UI; sliders persist; pause/cinematic ducking hồi phục; cue nguy hiểm có captions/symbol. Không có capability nghe/loopback thì phần kiểm âm giữ NOT_TESTED, không dùng số peak đơn lẻ để chứng minh đúng cảm xúc.

## Dialogue và VI/EN
NARRATIVE_AGENT viết VI theo canon, scene beat, entry/exit conditions; LOCALIZATION_AGENT tạo EN và glossary, REVIEWER_AGENT đối chiếu. Chuỗi text có key ngay từ S06; không đợi S29 mới gỡ hardcode. Catalog gồm key, vi, en, context, speaker, spoiler_chapter, placeholders. Hints/captions/tutorial/settings/credits cùng pipeline. Pseudo-localize + large text trước text freeze; final EN ở S29–S30 có rendered LQA [SRC05].

Nguồn font: agent chọn license phù hợp và glyph Việt/Anh, ghi URL/giấy phép; gói kế hoạch hiện tại không kèm font binary. Không bàn giao font có hạn chế phân phối. Việc được dùng trong game khác quyền gửi riêng file nguồn font cho người nhận.

## Rights và dịch vụ sinh nội dung
Manifest không được ghi “free” như một license. Lưu license text/URL/checked_at, quyền sửa/phân phối/attribution, source hash, dịch vụ/model/điều khoản tại lúc tạo khi dùng AI. Không suy quyền thương mại chỉ từ output được tải. Cần paid API thì lập permission request với ngân sách tối đa; default 0. Asset quyền chưa rõ phải thay hoặc block release. Không gọi thủ tục của chủ tài khoản là task coding đã hoàn thành.

## Chapter pipeline
Đọc CH spec + hai P specs → greybox main/optional route → puzzle state graph/tests → narrative/journal → camera/enemy/checkpoints → final model/material/lighting → audio/cinematic → save/revisit/capture regression → rendered walkthrough → reviewer acceptance → manifest FINAL. Mỗi cặp sprint chapter phải hoàn tất cả art/audio/QA, không để toàn bộ “polish” dồn vào S31.
