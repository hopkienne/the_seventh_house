# 07 — Sources, assumptions và decisions

Tài liệu bên ngoài chỉ hỗ trợ thông tin công cụ/nền tảng, không xác nhận game đã chạy. `/stable/` có thể đổi theo thời gian; agent đối chiếu binary pin. Quyết định narrative/gameplay/quality thresholds trong v3 là thiết kế của dự án, không được gán cho Godot.

| ID | Nguồn | URL | Áp dụng |
| --- | --- | --- | --- |
| SRC01 | Godot archive | https://godotengine.org/download/archive/ | Pin 4.7.2 stable đã đối chiếu; không khẳng định binary đã có trong máy agent. |
| SRC02 | Available 3D formats | https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html | GLB/glTF pipeline và source format. |
| SRC03 | Exporting projects | https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html | Export presets/templates/filters; agent kiểm lại theo pin. |
| SRC04 | Saving games | https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html | File/serialization cơ sở; atomic recovery/schema là contract dự án, phải tự test. |
| SRC05 | Internationalizing games | https://docs.godotengine.org/en/stable/tutorials/i18n/internationalizing_games.html | Localization keys/catalog; LQA là công việc dự án. |
| SRC06 | Steam release process | https://partner.steamgames.com/doc/store/releasing | Store/build review, Coming Soon và quyền release; recheck current account. |
| SRC07 | PhysicsDirectSpaceState3D | https://docs.godotengine.org/en/stable/classes/class_physicsdirectspacestate3d.html | Target-world physics query APIs; không chứng minh SwitchSafety implementation. |
| SRC08 | Godot command line tutorial | https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html | --import, --script, --export-release; --test không phải game test suite. |

## Quyết định khác v2
D-001: đổi executor từ người/freelancer sang agent modes, một agent tuần tự là đủ về mô hình tổ chức. D-002: sprint là wave, bỏ ETA/capacity/giờ người/chi phí suy diễn khỏi bản đang thực thi. D-003: task definitions và task state tách làm hai file; Excel/HTML chỉ là views. D-004: mọi task có card/input/output/tests/evidence/blocker/resume. D-005: human playtest targets đổi thành explicit agent scenario reviews; không tuyên bố feedback người thật. D-006: public/legal/paid actions giữ permission boundaries, không giả quyền. D-007: canon giải rõ người kích hoạt, mẹ duy trì, An aging và reset ending. D-008: 14 puzzle có đáp án/graph/test và 28 evidence IDs canonical. D-009: giữ 592 task IDs, không xóa Must; conditional bug allowance chỉ N/A khi có evidence. D-010: không mang source v1/v2 đang có hiệu lực trong gói, tránh agent đọc nhầm.

## Những gì chưa được kiểm chứng khi bàn giao gói
Repo game, Godot runtime, build Windows, art/audio final, public account, human playtest, benchmark hardware/cost/ETA. Chúng là kết quả tương lai của task execution, không trạng thái được kế thừa từ kế hoạch. Script validation chỉ kiểm bộ tài liệu/task graph/tool workflow; báo cáo khác phải ghi NOT_TESTED.
