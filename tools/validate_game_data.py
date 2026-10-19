#!/usr/bin/env python3
"""Validate produced runtime data. Missing campaign content is PARTIAL, never a game PASS."""
import argparse
import csv
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate(data_root=None, require_complete=False):
    data_root = Path(data_root) if data_root else ROOT / 'data'
    errors, checked, missing = [], [], []
    coverage = {}
    ids = {
        'chapters': {c['id'] for c in read(ROOT/'specs/chapter_catalog.json')},
        'puzzles': {p['id'] for p in read(ROOT/'specs/puzzle_catalog.json')},
        'clues': {r['id'] for r in read(ROOT/'specs/evidence_catalog.json')},
        'endings': {'A', 'B', 'C'},
    }

    def error(path, message):
        errors.append({'path': str(path), 'message': message})

    def document(path):
        try:
            value = read(path)
            checked.append(str(path))
            return value
        except (OSError, ValueError) as exception:
            error(path, str(exception))
            return None

    def schema(path, value, name):
        definition = read(ROOT / f'specs/schemas/{name}.schema.json')
        # Contract schemas are self-contained. Never fetch arbitrary schema URLs.
        def refs(node):
            if isinstance(node, dict):
                if '$ref' in node and not node['$ref'].startswith('#'):
                    raise ValueError('External schema references forbidden')
                for child in node.values(): refs(child)
            elif isinstance(node, list):
                for child in node: refs(child)
        refs(definition)
        Draft202012Validator.check_schema(definition)
        problems = list(Draft202012Validator(definition).iter_errors(value))
        for problem in sorted(problems, key=lambda p: p.json_path):
            error(path, problem.json_path + ': ' + problem.message)
        return not problems

    product = data_root / 'runtime/product.json'
    if product.exists():
        value = document(product)
        if value is not None: schema(product, value, 'product')
    else:
        missing.append('runtime/product.json')

    for kind, canonical in ids.items():
        found = set()
        for path in sorted((data_root / kind).glob('*.json')):
            value = document(path)
            if value is None: continue
            records = value if isinstance(value, list) else [value]
            for record in records:
                if not isinstance(record, dict) or not record:
                    error(path, 'Runtime record must be a nonempty object')
                    continue
                identity = record.get('id', record.get({'chapters':'chapter_id','puzzles':'puzzle_id','clues':'evidence_id','endings':'ending_id'}[kind], path.stem))
                if not isinstance(identity, str) or identity not in canonical:
                    error(path, f'Unknown {kind} ID: {identity}')
                    continue
                if identity in found: error(path, 'Duplicate ID: ' + identity)
                found.add(identity)
                if 'chapter_id' in record and (not isinstance(record['chapter_id'], str) or record['chapter_id'] not in ids['chapters']):
                    error(path, 'Unknown chapter reference')
        absent = sorted(canonical - found)
        coverage[kind] = dict(expected=len(canonical), present=len(found), missing_ids=absent)
        if absent: missing.append(kind)

    line_ids, text_values = set(), {}
    dialogue_files = sorted((data_root/'dialogue').glob('*.json'))
    if not dialogue_files: missing.append('dialogue')
    for path in dialogue_files:
        value = document(path)
        if value is None or not schema(path, value, 'dialogue'): continue
        for line in value['lines']:
            if line['id'] in line_ids: error(path, 'Duplicate dialogue line ID: ' + line['id'])
            line_ids.add(line['id'])
            translation = (line['vi'], line['en'])
            if line['text_key'] in text_values and text_values[line['text_key']] != translation:
                error(path, 'Conflicting translation key: ' + line['text_key'])
            text_values[line['text_key']] = translation

    translations = {}
    localization_files = sorted((data_root/'localization').glob('*.csv'))
    if not localization_files: missing.append('localization')
    for path in localization_files:
        checked.append(str(path))
        with path.open(encoding='utf-8-sig', newline='') as source:
            rows = csv.DictReader(source)
            fields = rows.fieldnames or []
            if not fields or not {'vi','en'} <= set(fields):
                error(path, 'Godot CSV must contain a key column and vi/en columns')
                continue
            key_column = fields[0]
            for row in rows:
                key = row.get(key_column)
                if not key or not (row.get('vi') or '').strip() or not (row.get('en') or '').strip():
                    error(path, 'Empty translation key/VI/EN')
                elif key in translations:
                    error(path, 'Duplicate translation key: ' + key)
                else: translations[key] = (row['vi'], row['en'])
    if localization_files:
        for key, value in text_values.items():
            if translations.get(key) != value: error('localization', 'Missing/mismatched dialogue text reference: ' + key)

    for path in sorted((data_root/'save_fixtures').glob('*.json')):
        value = document(path)
        if value is not None: schema(path, value, 'save')
    asset_files = sorted((data_root/'assets').glob('*.json'))
    if not asset_files: missing.append('asset_manifests')
    for path in asset_files:
        value = document(path)
        if value is not None: schema(path, value, 'asset')
    if not checked: errors.append({'path':str(data_root),'message':'Zero produced runtime files checked'})
    result = 'FAIL' if errors or require_complete and missing else 'PARTIAL' if missing else 'PASS'
    return dict(result=result, scope='PRODUCED_RUNTIME_DATA_ONLY_NOT_GAMEPLAY_OR_CONTENT_QUALITY',
                files_checked=len(checked), checked_files=checked, coverage=coverage,
                incomplete_categories=missing, errors=errors, dialogue_lines=len(line_ids),
                translation_keys=len(translations), references_scope='Canonical IDs; inline dialogue VI/EN; CSV references when present. Runtime flag/event registries and script string references are not yet checked.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    result = validate(require_complete=args.require_complete)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['result'] == 'FAIL' else 0


if __name__ == '__main__':
    raise SystemExit(main())
