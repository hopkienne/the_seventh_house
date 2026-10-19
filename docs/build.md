# Build Windows local — bootstrap

Đây là pipeline của project ở giai đoạn BOOTSTRAP, chưa có campaign/locomotion/final assets. Build PASS xác nhận import, suites và export/package; native rendered EXE smoke là phép kiểm riêng. Không có upload hoặc publish trong pipeline.

## Rebuild

1. `python tools/fetch_godot.py` tải portable editor đúng 4.7.2 stable và kiểm SHA256 từ official release API.
2. `python tools/fetch_godot.py --templates` tải matching templates; nếu bị ngắt, kiểm partial rồi dùng `--templates --resume`. Dữ liệu tải nằm trong `.tools/`, không đưa vào Git.
3. `python scripts/build_windows.py` kiểm hash editor/templates và version, chạy headless import → bootstrap → scene → export-release preset `Windows Desktop` → inspect PCK trong project rỗng.
4. Kết quả mới ở `builds/windows/<build_id>/`, log riêng từng step và manifest ở `reports/builds/<build_id>/`. Có EXE/PCK, hashes, source hash, assertions và limitations. Mỗi build tạo thư mục mới, không xóa/ghi đè build trước.

Có thể truyền `--godot <verified-console-or-editor.exe> --preset "Windows Desktop" --output-dir builds/<name> --timeout 180`. Binary phải đúng hash trong lock, cùng thư mục với editor chính; không dùng tên PATH để vượt pin. Output chỉ trong `builds/`. Không gọi suite world chưa được implement. Runner thiếu, zero tests/assertions, skipped, timeout, engine ERROR dù exit 0, export thiếu EXE/PCK hoặc pack inspection fail đều dừng build và giữ failure manifest/log.

`python tests/test_build_windows.py` kiểm process error handling bằng subprocess fixture (không phải gameplay test). `python tools/verify_bootstrap.py --report-dir reports/verification/bootstrap` kiểm cả runner negative paths, không ghi đè evidence task đã đóng.

## Package và source control

Preset giữ runtime JSON/CSV trong các folder runtime được chỉ định. Test/script tools, planning inputs, reports, source assets, host capabilities, lock/permissions, secrets và build cũ không được đóng vào PCK. Inspection mount PCK trong project rỗng để source tree không che file bị thiếu. `data/runtime/product.json` phải còn và main scene phải loadable.

Git local nhánh `main`. `.tools/`, `.godot/`, `.qa/`, `builds/`, Python cache và secret patterns được ignore. LFS CLI đã probe được, nhưng chưa có remote/host LFS được xác minh nên chưa bật filter=lfs hoặc tạo pointers. Binary source dùng ordinary Git binary files hiện tại; khi có assets lớn/remote phải chọn LFS host thực hoặc artifact manifest với hash theo contract. Không có remote/push mặc định.

## Runtime smoke trên host hiện tại

Main hỗ trợ `-- --qa-profile BOOTSTRAP --qa-report <res://reports/...json hoặc user://...json>`, ghi report và PNG sau frame_post_draw rồi thoát theo kết quả. Unknown profile/headless render/out-of-scope report path bị từ chối.

NVS 310 không chạy native Forward+. Functional rendered tests hiện dùng explicit process-scoped SwiftShader Vulkan theo ADR-001 và `config/test_environment.json`; không thay project renderer. Không phân phối SwiftShader/browser binaries cùng game, không đổi machine environment. Native EXE render bằng software vẫn phải ghi software=true, không được dùng làm GPU performance/minimum-spec evidence. Pad vật lý/audio listening chưa được kiểm.
