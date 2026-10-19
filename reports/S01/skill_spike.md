# S01 model import / Godot skill spike

Kết quả: PASS cho GLB static-prop pipeline; self_review=true. Không phải nhân vật/rig/final art acceptance.

Agent tạo recipe ghế gỗ meter-scale `tools/art/stool_spike.json`, generator Godot `tools/art/build_stool_spike.gd`, xuất GLB thật bằng GLTFDocument. Không có Blender hoặc mesh/texture bên ngoài. Năm BoxMesh có material PBR chung, seat 0.48×0.06×0.40m ở y=0.45m; bốn chân 0.045×0.42×0.045m chạm mặt sàn y=0. Không random parameters.

GLB 4.468 bytes tại tests/fixtures/art/stool_spike.glb. Hai lần rebuild cùng SHA256 `a2ac9541d19a1b862638b5a67f00568b462a7a5eddf56e56fe94369399735014`. Godot --import thực thành PackedScene. Suite asset_import: 2 cases/29 assertions PASS, kiểm đủ 5 mesh, material, vertices/normals/UV và vị trí seat; missing GLB không được coi available.

Fixture ghép GLB vào main scene, ẩn cột scale reference và đổi camera cho prop; non-headless Forward+ Vulkan qua SwiftShader, capture 1280×720 đã xem: ghế gỗ có mặt ngồi/chân/bóng rõ, không black frame. Source recipe + generator + engine pin + asset manifest + raw import/test/rebuild/render logs tại reports/tasks/T-010402/; mẫu giữ quality_state=BLOCKOUT và bị loại khỏi retail pack bằng tests/*.

## Lỗi thực được sửa trong spike

Suite ban đầu timeout 90s. Bounded reproducer 5s lưu SCRIPT ERROR gọi null::_import_glb: Callable không giữ provider RefCounted sống sau block registry. Runner nay giữ providers tới hết execution và từ chối invalid Callable bằng structured FAIL/nonzero. Ca âm invalid_callable thoát1 ngay với0 assertions/FAIL, không được gọi là game PASS. Regression bootstrap/scene/utilities và asset_import đều chạy thật. Build entrypoint nay discover --list-suites để chạy cả utilities/asset_import trước export thay vì bỏ sót các suite mới.

## Gap thực và đường xử lý

| Vùng | Đã kiểm | Gap / cách tiếp tục |
| --- | --- | --- |
| Static model/material | GLB export/import, normals/UV primitive, scale, PBR và capture | Chưa có bevel/texture/golden sample, collider authored, module kit hay hai phase; sản xuất ở task art, cùng rubric in-game |
| Rig/animation | NOT_TESTED | Chưa có Skeleton3D/weights/clips; cần agent làm base rig/animation recipe và test imported clips; không gọi primitive prop là final character |
| Shader | StandardMaterial3D hiển thị qua Forward+ | Custom phase shader/VFX/reduced-effects chưa implement/test; đối chiếu API pin và kiểm captures khi task tới |
| Navigation | NOT_IMPLEMENTED | Chưa bake NavigationMesh hoặc test Agent/path/perception; triển khai ở gameplay/stealth với phase/LOS contracts, không suy từ import mesh |
| Profiling | Functional software render, không lấy FPS làm benchmark | NVS 310 native Forward+ fail; hardware GPU performance BLOCKED_CAPABILITY khi gate benchmark cần. Có thể đo logic/headless riêng, không thay GPU số liệu |
| Blender | CLI absent trong audit | Godot procedural pipeline đã hoạt động cho prop phù hợp; nếu workflow rig cần Blender, agent tự bootstrap portable miễn phí và probe trước khi dùng |

Chưa có kỹ năng/tài nguyên nào được giao cho freelancer hoặc yêu cầu owner tự làm. Physical pad và audible audio mix vẫn NOT_TESTED. G0 chỉ dựa mức bootstrap phù hợp; các gap final quality không biến thành fake PASS.
