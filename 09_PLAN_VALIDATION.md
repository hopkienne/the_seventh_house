# 09 — Kiểm tra Agent Execution Pack v3

## Phạm vi
Báo cáo này kiểm tra **tài liệu, manifest, dependency graph và helper tools**. Không có source game đã triển khai trong gói. Không có tuyên bố import Godot, chạy Windows game, render gameplay, nghe mix hoặc hoàn thành một chương game.

## Kết quả thực đã chạy
| Kiểm tra | Kết quả | Evidence |
|---|---|---|
| Parse JSON; ID duy nhất; parent/story/sprint; trường bắt buộc | PASS | data/plan_validation.json |
| Dependency tồn tại, không vòng lặp, không phụ thuộc wave tương lai | PASS | data/plan_validation.json |
| 36 wave / 146 story / 592 task card; read_before paths | PASS | data/plan_validation.json |
| 7 chapter / 14 puzzle / 28 journal records; đáp án và hints | PASS | data/plan_validation.json |
| Tuyến sơ tán bảy đoạn nối đúng | PASS | data/plan_validation.json |
| 22 unit tests của agentctl | PASS | data/agentctl_tests.log |
| HTML: tìm kiếm, chọn task, lọc wave, mobile và JavaScript | PASS | data/handbook_ui_validation.json |
| Excel: 12 sheet, công thức tổng hợp và render Dashboard | PASS | data/spreadsheet_validation.json |
| Bootstrap harness trước các task yêu cầu ENGINE_TEST | Đã sửa contract: tạo ở T-010301, mở rộng T-010401 | tasks/T-010301.md; 10_ENVIRONMENT_AND_COMMANDS.md |

Các unit test helper chạy trên temporary fixture repositories. Fixture capture trong unit test chỉ là dữ liệu thử parser, **không phải ảnh game hay evidence nghiệm thu game**. Evidence validator kiểm cấu trúc/hash/đường dẫn/loại kiểm thử; không thể tự xác thực nội dung lời báo cáo có đúng với gameplay. Reviewer phải kiểm tra artifact và log thật.

## Cách tái kiểm tra
```bash
python tools/validate_plan.py --output data/plan_validation.json
python -m unittest discover -s tools -p test_agentctl.py -v
python tools/render_views.py
python tools/agentctl.py summary
python tools/agentctl.py next
```
`render_views.py` tái tạo task/story/wave Markdown, backlog, HTML và CSV từ manifest/state. Không reset state, không thực thi game task, không cập nhật XLSX. XLSX là snapshot revision 0; khi state đổi, dùng HTML/CSV/JSON mới để quyết định công việc.

## Trạng thái bàn giao
592 task: **NOT_STARTED**. 10 gate: **NOT_EVALUATED**. Chưa có artifact game `DONE`. Dùng lệnh next để xác định task Ready đầu tiên, không chuyển trạng thái chỉ vì gói tài liệu đã hoàn tất.

Kiểm ZIP/manifest cuối gói nằm trong PACKAGE_CHECK.json. File đó chỉ chứng minh tính toàn vẹn tài liệu đóng gói, không chứng minh game hoàn chỉnh hoặc kiểm chứng môi trường máy agent.
