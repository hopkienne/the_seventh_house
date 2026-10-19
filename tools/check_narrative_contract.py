#!/usr/bin/env python3
"""Static production-data checks; explicitly not a cinematic runtime test."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check():
    checks = []

    def require(label, condition):
        checks.append({'id': label, 'result': 'PASS' if condition else 'FAIL'})

    keys, flags, hints = [], [], []
    files = ['canon_timeline.md', 'world_rules.md', 'reveal_ending_matrix.md']
    for name in files:
        text = (ROOT / 'docs/story' / name).read_text(encoding='utf-8')
        require(name + ':utf8', '\ufffd' not in text)
        for line in text.splitlines():
            if not re.match(r'\| story\.', line):
                continue
            cells = [c.strip() for c in line.strip('|').split('|')]
            require(cells[0] + ':fields', len(cells) == 4 and all(cells))
            if len(cells) != 4:
                continue
            key, vi, condition, flag = cells
            keys.append(key)
            flags.append(flag)
            require(key + ':key', bool(re.fullmatch(r'story\.[a-z0-9_.]+', key)))
            require(key + ':once', bool(re.fullmatch(r'[a-z0-9_]+_seen', flag)))
            chapter = re.search(r'\.ch(\d{2})\.', key)
            require(key + ':chapter', chapter is not None and 1 <= int(chapter[1]) <= 7)
            if chapter and int(chapter[1]) < 6:
                require(key + ':no_identity_spoiler', not re.search(r'\bAn\b|em gái|điểm neo là', vi))
            if key.startswith('story.route.ch0') and chapter and int(chapter[1]) <= 3:
                hints.append(key)
                require(key + ':earned', 'collected' in condition)
    require('translation_keys_unique', len(keys) == len(set(keys)) and len(keys) > 0)
    require('once_flags_unique', len(flags) == len(set(flags)))
    require('at_least_two_early_route_foreshadows', len(hints) >= 2)
    chapters = json.loads((ROOT / 'specs/chapter_catalog.json').read_text(encoding='utf-8'))
    records = json.loads((ROOT / 'specs/evidence_catalog.json').read_text(encoding='utf-8'))
    route = json.loads((ROOT / 'specs/evacuation_route.json').read_text(encoding='utf-8'))
    require('seven_unique_houses', {c['house_id'] for c in chapters} == {f'H{i:02}' for i in range(1, 8)})
    require('memory_route_bijection', {r['id'] for r in records if r['kind'] == 'MEMORY'} ==
            {s['memory_id'] for s in route['segments']} == {f'M{i:02}' for i in range(1, 8)})
    require('no_permanently_missable_records', all(not r['missable'] for r in records))
    require('only_essential_records_gate_main', all(r['gates_main'] == (r['kind'] == 'ESSENTIAL') for r in records))
    cursor = route['start']
    for segment in route['segments']:
        require(segment['memory_id'] + ':connected', segment['from'] == cursor)
        record = next(r for r in records if r['id'] == segment['memory_id'])
        require(segment['memory_id'] + ':catalog_edge', (record['route_from'], record['route_to']) ==
                (segment['from'], segment['to']))
        cursor = segment['to']
    require('route_reaches_hill', cursor == route['end'] == 'HILL')
    result = {'result': 'PASS' if all(c['result'] == 'PASS' for c in checks) else 'FAIL',
              'scope': 'STATIC_AUTHORING_CONTRACT_NOT_GAMEPLAY', 'checks_count': len(checks),
              'translation_keys': keys, 'early_foreshadows': hints, 'checks': checks}
    return result


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['result'] == 'PASS' else 1)
