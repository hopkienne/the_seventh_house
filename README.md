# Ngôi Nhà Thứ Bảy — Agent Execution Pack v3

Bắt đầu tại **START_HERE.md**. Giao nguyên gói cho agent trong repository, dùng **MASTER_AGENT_PROMPT.md**. Phiên sau dùng RESUME_AGENT_PROMPT.md.

36 execution waves / 146 stories / 592 task cards. Agent thực hiện toàn bộ code, story, art, animation, audio, UI, localization, QA và delivery. Không có lịch/nhân sự freelancer làm điều kiện sản xuất. Public/paid/legal actions vẫn có permission boundary.

## Files
AGENTS.md: luật làm việc. 01: master plan. 02: toàn bộ task contract (dài, chỉ tra cứu). 03: content/assets. 04: technical contracts. 05: QA. 06: execution/review/resume. 07: sources/decisions. 08: risks. 09: validation của gói. 10: environment/commands. 11: canon. 12: release/permissions. 13: GDD.

`plan/backlog.json` canonical definitions; `state/task_state.json` runtime state; tasks/stories/sprints là read views. specs chứa 7 chapters/14 puzzles/28 evidence/route/schemas/fixtures. tools chứa plan validator, next-task/state controller và tool tests. templates chứa report/evidence/ADR/handoff. data là CSV snapshots và migration map. HTML/Excel là bản xem, không nguồn trạng thái riêng.

**Chưa có source game hoặc executable game trong gói.** Kết quả validation là của tài liệu/dependency/tools, không phải game QA. Agent phải thực tạo/test outputs theo từng task; tất cả task game bắt đầu NOT_STARTED.

## Làm mới bản xem
Chạy `python tools/render_views.py`: sinh lại Markdown task/story/wave, backlog, HTML và CSV từ JSON, không đổi tiến độ. Excel là snapshot ban đầu (revision 0), không tự đồng bộ.
