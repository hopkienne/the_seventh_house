# 10 — Environment bootstrap và lệnh cho agent

## Capability audit trước khi nhận task kỹ thuật
Đọc permissions thật của môi trường. Dùng shell/filesystem/Python/Git đã có, không giả định Blender, Godot, GPU, gamepad, GUI automation, image/audio tools, subagents hoặc Windows máy test đều sẵn. Kiểm phiên bản thực bằng argument list + timeout. Không tự cài dịch vụ trả phí hoặc dùng tài khoản cá nhân chưa được cho phép.

`config/agent_capabilities.json` do T-010103 tạo: tool/name/path/version, probe command/exit code, available, CLI/render/GPU/native Windows/physical pad/network/asset tool/subagent status, limitations, fallback, probe_timestamp. Giá trị unknown để null; `available=true` cần probe thực. `config/toolchain.expected.json` là baseline mong muốn, không chứng minh installed.

Godot pin 4.7.2 stable theo archive official đã kiểm 18/10/2026 [SRC01]. Binary và export templates phải cùng phiên bản. Nếu không lấy được đúng pin, ghi blocker và kiểm nguồn, không tự dùng beta. Thay patch qua ADR với import/save/export regression. Blender/Python phiên bản được record từ môi trường, không bịa số “mới nhất”.

## Capability → phương án
| Thiếu | Tiếp tục được | Chưa được xác nhận |
|---|---|---|
| Godot CLI | Viết/validate plan, canon, data và scripts theo docs | Import/runtime/gameplay tests |
| GPU/render | Headless logic/data tests, xuất build nếu tools đủ | Art/camera/UI/rendered replay/performance |
| Blender | Dùng Godot procedural mesh/tool script cho asset phù hợp hoặc xin cài binary local | Blender source/rig import chưa tạo không DONE |
| Audio playback/capture | Synthesis và phân tích waveform/metadata | Đánh giá mix/cue nghe thực |
| Windows runtime | Cross-export .exe nếu templates đủ; native host testing | Native Windows smoke/compatibility |
| Physical pad | Synthetic action replay và focus logic | Hotplug/driver/mapping thiết bị thật |
| Steam account | Local package/store drafts/rights audit/runbook | Platform state/upload/approval/public |
| Paid generation | Procedural art/audio hoặc nguồn có license được kiểm | Dịch vụ trả phí chưa có authorization |

Không cần hỏi người dùng đi làm asset. Chỉ báo capability thực cần cấp nếu không có đường thay thế đạt tiêu chí. Điểm cuối không được che thiếu môi trường test.

## Lệnh CÓ SẴN trong gói
```bash
python tools/validate_plan.py
python tools/agentctl.py summary
python tools/agentctl.py next
python tools/agentctl.py show T-030201
python tools/test_agentctl.py
```
Các script này quản lý **tài liệu/task ledger**, không test Godot/game. `test_agentctl.py` chạy trên temporary copies, không đánh DONE task game trong ledger gốc.

## Lệnh Godot sau khi T-010301 tạo project/toolchain
Dưới đây dùng tên `godot`; thay bằng đường dẫn binary đã xác minh. Trên PowerShell dùng call operator `&` trước đường dẫn có dấu cách. Các ví dụ là templates có điều kiện tiên quyết, không report đã chạy.

**RUN-VERSION**
```bash
godot --version
```
**RUN-IMPORT** — cần `project.godot`.
```bash
godot --headless --path . --import
```
**RUN-BOOTSTRAP** — harness do T-010301 tạo ngay trong bootstrap, không phụ thuộc T-010401.
```bash
godot --headless --path . --script res://tests/test_runner.gd -- --suite bootstrap
```
T-010301..T-010304 dùng bootstrap suite có assertions thật; T-010401 mở rộng registry/report. Không yêu cầu suite world trước khi WorldController đã được tạo. Unknown suite và zero tests phải fail.

**RUN-TEST** — cần `tests/test_runner.gd` bootstrap do T-010301 tạo và T-010401 mở rộng.
```bash
godot --headless --path . --script res://tests/test_runner.gd -- --suite world
```
**RUN-RENDER** — cần test replay scene/entrypoint do task gameplay/QA tạo.
```bash
godot --path . -- --qa-profile P0_MAIN --qa-report reports/runtime/p0_main.json
```
Các custom options sau `--` phải được agent implement đọc bằng project code; Godot không tự hiểu `--qa-profile`, `--qa-report`, `--suite`. Không gọi chúng rồi bỏ qua vì engine không lỗi. RUN-RENDER test build phải thực tạo capture/report/exit code, không dùng headless để thay render.

**RUN-EXPORT** — cần templates và `export_presets.cfg` có preset chính xác; tạo folder trước.
```bash
python -c "from pathlib import Path; Path('builds/windows').mkdir(parents=True,exist_ok=True)"
godot --headless --path . --export-release "Windows Desktop" builds/windows/TheSeventhHouse.exe
```
Godot command-line và export semantics dựa official docs [SRC08]. Không dùng `--test` để giả chạy game tests: đó là engine unit tests với build phù hợp. Import checker exit 0 chưa chứng minh mọi runtime branch.

**RUN-WINDOWS** — chỉ chạy trên Windows runtime được kiểm. Cài/copy artifact sang thư mục sạch, mở `.exe`, New Game/save/continue/replay. Dùng automation công cụ thực của agent nếu có; ghi native OS và capture. Wine/cross-export không tự tương đương native Windows QA.

## Script build agent phải tạo
`scripts/build_windows.py` nhận `--godot`, `--preset`, `--output-dir`, ghi version/hash/manifest, gọi import/test/export trong thứ tự đúng, timeout từng subprocess, dừng khi exit code/test count/error log fail. Không dựa executable tên chung trong PATH khi lock chỉ binary khác. Ghi stdout/stderr riêng, không nuốt lỗi. Working directory rõ; không delete folder ngoài outputs của chính build. Test runner chưa tạo thì báo NOT_TESTED, không tạo report PASS mặc định.

## Asset commands
T-ART tạo generator/config. Khi binary Blender sẵn, kiểm `blender --help` của bản local rồi chạy background Python theo help; không copy API chưa đối chiếu. Generator có version, seed, outputs paths, validation, không network upload ngầm. Equivalent Godot tool scripts cũng phải có entrypoint/config/rebuild proof. `audio` generator xuất file thực kèm metrics/source, không chỉ JSON cue names.

## Nguồn kiểm chứng và bảo mật
Source URLs trong 07_SOURCES_AND_DECISIONS.md. Ghi checksum của file tải thực; không gán một hash tự nghĩ. Chỉ đọc credentials qua secret store/env nếu task cần, redact logs. Không kiểm toàn bộ máy hoặc tài khoản ngoài phạm vi task. Không tự dùng tài nguyên khác repo mà chưa biết quyền.
