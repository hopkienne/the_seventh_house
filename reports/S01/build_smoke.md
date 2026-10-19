# S01 clean build và native Windows bootstrap smoke

Kết quả: PASS cho bootstrap, không phải full-game QA. `self_review=true`.

Candidate source commit: `74e110fbf5fd6177364f9ab5629f6df0fa5f6ff2`. Clone local sạch, trước build không có `.godot`, working tree clean. Chỉ cài hai Windows templates đã khóa hash và `version.txt` vào tool-cache ignored; editor được truyền explicit từ cache đã kiểm hash. Không sửa tracked runtime source để build; `git diff --exit-code` sau build bằng 0.

Clean build ID: `20261019T034749875677Z`, source SHA256 `805802baa0dfd4482852453110d90882d558faf2a3b5c18a6b56320f64986108`. Import → bootstrap 21 assertions → scene 57 assertions → release export → PCK inspection đều PASS, không skipped. Runtime product JSON/main scene có trong PCK; tests/tools/reports/planning/host configs/build cũ không có trong các forbidden paths được kiểm.

| Artifact | SHA256 |
| --- | --- |
| TheSeventhHouse.exe | 2160d4ed2cc9b3ef9ef2827dafb826b2b34a2ff34387ff0c706e0f255b590497 |
| TheSeventhHouse.pck | 75c3f57ec6ed4c6ffe9eb885014996e7f1680dd8ee0ccd980032a46f469829f3 |
| Native smoke PNG | de27712f9053c7ffadc102b8b86aa6a2bed01e94a0c19df4c5b0e91979a1be85 |

Copy EXE/PCK sang thư mục mới `.qa/native_smoke/20261019T034749875677Z/`, chạy EXE trực tiếp ngoài editor trên Windows 10. Explicit SwiftShader ICD chỉ trong môi trường subprocess. Actual renderer Forward+, driver Vulkan, adapter SwiftShader Device (Subzero), display Windows. BOOTSTRAP profile chạy 5 assertions, 0 failure/skipped, frame 1280×720, 14 sampled colors, exit 0 và stderr rỗng. PNG trùng SHA256 ảnh scene đã xem ở T-010302 (sàn, cột tham chiếu và bóng có thể thấy), không phải ảnh đen. Negative unknown profile chạy cùng EXE/PCK, exit 2 đúng expectation.

Raw facts ở `reports/tasks/T-010304/`: clean_build.json, clean_manifest.json, native_verification.json, native_smoke.json/png, stdout/stderr và negative profile report. Candidate build có manifest/logs riêng trong clean checkout được ghi bằng đường dẫn chính xác tại clean_build.json.

## Giới hạn

- Đây là geometry/bootstrap scene, chưa có locomotion/campaign/save/final art/audio. Không dùng làm nghiệm thu 7 chương hoặc release game.
- Đây là native Windows executable test bằng **software CPU rendering**, không benchmark/compatibility proof của hardware Forward+. NVS 310 fallback native không đạt Forward+, được giữ ở CAP-001/ADR-001.
- Physical keyboard/gamepad, hotplug, audio listening, GPU performance, toàn bộ game route: NOT_TESTED.
- EXE hash trùng build ban đầu; PCK/source-tree byte hashes khác. Source comparison chỉ tìm thấy newline khác ở lock JSON và GDScript UID do Git checkout normalization; tracked source diff trong clone rỗng. Không tuyên bố PCK bit-for-bit reproducibility. Functional rebuild từ clean commit đã được kiểm bằng suites, package inspection và EXE smoke thực.
- Không upload/publish, không native minimum-spec claim, không chạy nền sau phiên.
