#!/usr/bin/env python3
"""Render requirement traceability from the canonical manifest; no ledger writes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render():
    plan = json.loads((ROOT / 'plan/backlog.json').read_text(encoding='utf-8'))
    story_ids = {story['id'] for story in plan['stories']}
    assert {r['id'] for r in plan['requirements']} == {f'R{i:02}' for i in range(1, 19)}
    lines = [
        '# Yêu cầu và ma trận nghiệm thu 1.0', '',
        'Nguồn chuẩn: `plan/backlog.json`. Tái tạo bằng `python tools/write_requirements.py`.',
        'Tất cả R01–R18 là Must của Full Game 1.0; bảng này là định nghĩa nghiệm thu, không phải bằng chứng tính năng đã PASS.',
        'Trạng thái task/gate chỉ lấy từ `state/task_state.json`; không duy trì trạng thái thứ hai trong tài liệu này.', '',
        '| ID | Yêu cầu Must | Nghiệm thu | Gate | Stories |',
        '| --- | --- | --- | --- | --- |',
    ]
    for req in plan['requirements']:
        assert req['stories'] and set(req['stories']) <= story_ids
        links = ', '.join(f'[{sid}](../stories/{sid}.md)' for sid in req['stories'])
        values = [req['id'], req['title'], req['acceptance'], req['gates'], links]
        lines.append('| ' + ' | '.join(v.replace('|', '\\|') for v in values) + ' |')
    lines += ['', '## Các gate', '', '| Gate | Wave | Tiêu chí |', '| --- | --- | --- |']
    for gate in plan['gates']:
        lines.append(f"| {gate['id']} | {gate['sprint']} | {gate['criteria']} |")
    lines += [
        '', '## Quy tắc xác nhận', '',
        '- R02 gồm cả ba ending A/B/C, playable resolution, credits và checkpoint trước lựa chọn; cả 128 tổ hợp memory không khóa A/B. C cần đầy đủ memory cùng tuyến sơ tán đúng. Không thay bằng cinematic mô tả hoặc một ending duy nhất.',
        '- R06/R07 có 14 puzzle + 7 memory và 28 journal IDs (14 E + 7 L + 7 M). Save/load, negative input và revisit là phần nghiệm thu.',
        '- R14 cần số đo trên benchmark đã khóa và exported Windows runtime. Headless logic PASS không xác nhận GPU, art, audio hay gamepad vật lý.',
        '- Evidence task gồm outputs có hash, raw logs/captures đúng loại, expected/observed/result và reviewer. Single-agent review khai self_review=true; document review không xác nhận game chạy.',
        '- G7_TECH và G7_PUBLIC tách biệt. Public release cần quyền theo đúng build/channel; chưa có quyền giữ BLOCKED_EXTERNAL. G8 chỉ PASS sau tải/cài/smoke public build thật.',
        '- Requirement chỉ được xác nhận từ acceptance cùng evidence hợp lệ của các story/gate liên quan. Tỷ lệ task DONE không thay nghiệm thu sản phẩm.', '',
    ]
    return '\n'.join(lines)


if __name__ == '__main__':
    destination = ROOT / 'docs/requirements.md'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render(), encoding='utf-8')
    print('Rendered 18 Must requirements with canonical story/gate links.')
