# Workflow thực thi và resume

`plan/backlog.json` định nghĩa Sprint → Story → Task. `state/task_state.json` là trạng thái duy nhất. Không cần board/account ngoài. Source game hiện chỉ ở bootstrap; các catalog trong specs là contract, không phải content đã implement.

## Một task WIP

1. Đọc handoff, kiểm Git/disk và test liên quan; không tin một dòng DONE trong tài liệu. Chạy `python tools/validate_plan.py`, `python tools/agentctl.py summary`, `python tools/agentctl.py next`. Trên console Windows dùng `$env:PYTHONIOENCODING='utf-8'`.
2. Đọc đúng task card, story cha, read_before và dependency evidence. `python tools/agentctl.py start <ID> --executor codex-primary` claim sau khi đủ dependency/capability/gate.
3. Tạo test/fixture phù hợp, implement thật trong allowed scope, integrate, chạy verification. Runtime suite gọi implementation thật; PCK test mount trong project rỗng; exported smoke dùng EXE riêng.
4. Pass review riêng: so code/artifact/AC/log, tìm failure mode. Một agent thì khai `self_review=true`; không mô tả là reviewer độc lập.
5. Viết `reports/tasks/<ID>/review.md` và evidence.json: actual timestamp, revision/build/source hash, outputs có SHA256, expected/observed/result, commands/raw logs/capture đúng loại và limitations. Artifact review không thay engine/render/Windows/audio.
6. `python tools/agentctl.py review <ID>` rồi `python tools/agentctl.py finish <ID> --evidence reports/tasks/<ID>/evidence.json`. Chỉ finish khi mọi required check PASS. Không sửa validator để qua một task fail.
7. Lưu handoff/task progress rồi chọn Ready tiếp theo. Không đánh DONE việc dở hoặc đổi scope để mở gate.

Block bằng agentctl với `--type BLOCKED_CAPABILITY|BLOCKED_EXTERNAL|BLOCKED_DEPENDENCY --reason ... --attempted ... --needed ...`. Ghi queue ở state/external_requests.json. Một nhánh blocked không cho phép vượt hard gate; nhánh Ready độc lập vẫn tiếp tục. Recheck rồi `start` khi blocker được gỡ. Rework từ lỗi production thật phải có reproducer/regression, không tạo bug giả để đủ sprint.

## Verification hiện có

`tests/test_runner.gd` kế thừa SceneTree; registry `bootstrap`, `scene`, `utilities`, `asset_import`. `--list-suites` xuất registry JSON cho build script chạy tất cả suite đã có, không gọi suite tương lai. Dùng pinned binary trong config/toolchain.lock.json:

```text
<pinned-console.exe> --headless --path . --script res://tests/test_runner.gd -- --suite bootstrap
<pinned-console.exe> --headless --path . --script res://tests/test_runner.gd -- --suite scene
<pinned-console.exe> --headless --path . --script res://tests/test_runner.gd -- --suite utilities
python tools/verify_bootstrap.py --report-dir reports/verification/<run-id>
python tools/test_agentctl.py
python tests/test_build_windows.py
python tests/test_validate_game_data.py
python tools/validate_game_data.py
python tools/validate_game_data.py --require-complete
python scripts/build_windows.py
```

Runner in JSON report có suite, registered_suites, executed/tests, assertions, failed, skipped, failures và result; explicit nonzero exit cho unknown suite, zero tests/assertions, bad arguments/fixtures và assertion failure. Negative fixture không vào default suite. Utility suite đọc runtime product JSON qua JSON reader thật, thử malformed/array/missing inputs. Không gọi world/ending suites chưa có.

Game data validator dùng jsonschema 4.25.1 đang probe được (`requirements-dev.txt`), Draft202012 schemas local, không fetch schema URL tùy ý. Kiểm runtime product; canonical chapter/puzzle/journal/ending IDs và duplicate; dialogue schema/line IDs/inline VI/EN; Godot CSV key/vi/en và text references khi catalog đã có; save/asset schemas khi có data tương ứng.

`PARTIAL` + exit 0 nghĩa là **các file đã sản xuất hợp lệ nhưng content còn thiếu**. Hiện chỉ có runtime/product.json: 0/7 chapter, 0/14 puzzle, 0/28 records, 0/3 ending. `--require-complete` trả FAIL/exit 1 khi coverage thiếu. Zero files là FAIL. Schema/IDs không chứng minh puzzle chơi được, art đẹp hay campaign hoàn chỉnh. Flag/event allowlists và script localization references chưa kiểm, ghi rõ trong report; mở rộng khi các registries được sản xuất, không bịa coverage.

## Evidence, Git và handoff

Evidence task đóng giữ nguyên. Task sau được sửa source hợp lệ và phải có evidence mới; đừng rewrite report cũ để hash source luôn khớp hiện tại. Khi replay dùng report-dir mới, tránh ghi đè raw logs đã đóng. Snapshot/commit giúp khôi phục phiên bản; exported EXE/PCK và manifest gắn cùng build ID. Không stage .tools/.godot/builds/secrets; không tạo LFS pointers khi chưa kiểm host thật. Không publish/push hoặc mua dịch vụ từ workflow này.

Cuối phiên ghi state/session_handoff.md: current task, Git commit/tree, working tree, changed files, commands/exit/count, validated vs NOT_TESTED, blockers/decisions và next concrete command. Commit local được phép trong phạm vi nhiệm vụ; không reset/force-push/xóa source cũ. Trước context limit giữ progress thật cả khi task chưa hoàn tất.

Gates chỉ cập nhật với evidence và required tasks terminal. G0 không phải full game; G7_TECH/G7_PUBLIC tách; không gọi PUBLISHED trước G8 và public smoke thật. Hiện rendered QA dùng SwiftShader CPU Vulkan theo ADR-001: functional render đúng Forward+ nhưng không benchmark GPU/physical input/audio listening.
