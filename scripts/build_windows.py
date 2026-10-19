#!/usr/bin/env python3
"""Fail-closed local Windows build. No downloads, deletion, upload or publishing."""
import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BuildFailure(RuntimeError):
    pass


def sha(path):
    with Path(path).open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def test_report(stdout):
    lines = re.findall(r'^TEST_REPORT (.+)$', stdout, re.MULTILINE)
    if len(lines) != 1:
        raise BuildFailure('Expected exactly one test report')
    report = json.loads(lines[0])
    if (report.get('result') != 'PASS' or report.get('tests', 0) < 1 or
            report.get('assertions', 0) < 1 or report.get('failed') != 0 or report.get('skipped') != 0):
        raise BuildFailure('Tests failed, skipped or executed zero assertions')
    return report


def run_step(name, command, log_dir, timeout):
    started = time.monotonic()
    try:
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=timeout)
        stdout, stderr, code = process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode('utf-8', 'replace') if isinstance(value, bytes) else value or ''
        stdout, stderr, code = decode(error.stdout), decode(error.stderr) + '\nTIMEOUT', None
    for stream, content in [('stdout', stdout), ('stderr', stderr)]:
        (log_dir / f'{name}.{stream}.log').write_text(content or '(empty stream)\n', encoding='utf-8')
    record = dict(id=name, command=command, exit_code=code, elapsed_seconds=time.monotonic()-started,
                  stdout=(log_dir / f'{name}.stdout.log').as_posix(), stderr=(log_dir / f'{name}.stderr.log').as_posix())
    if code != 0 or re.search(r'SCRIPT ERROR:|^ERROR:', stdout + stderr, re.MULTILINE):
        raise BuildFailure(f'{name} failed (exit={code}); see {log_dir}')
    return record, stdout


def source_hash():
    files = [ROOT / 'project.godot', ROOT / 'export_presets.cfg', ROOT / 'config/toolchain.lock.json']
    for directory in ['scenes', 'scripts', 'data/runtime', 'data/chapters', 'data/puzzles', 'data/dialogue', 'data/clues', 'data/localization']:
        files += [p for p in (ROOT / directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    return hashlib.sha256('\n'.join(f'{p.relative_to(ROOT).as_posix()} {sha(p)}' for p in sorted(files)).encode()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot')
    parser.add_argument('--preset', default='Windows Desktop')
    parser.add_argument('--output-dir', default='builds/windows')
    parser.add_argument('--timeout', type=float, default=180)
    args = parser.parse_args(argv)
    output_root = (ROOT / args.output_dir).resolve()
    output_root.relative_to((ROOT / 'builds').resolve())
    build_id = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = output_root / build_id
    output.mkdir(parents=True, exist_ok=False)
    logs = ROOT / 'reports/builds' / build_id
    logs.mkdir(parents=True, exist_ok=False)
    manifest = dict(build_id=build_id, result='FAIL', stage='BOOTSTRAP', steps=[], artifacts=[],
                    created_at=dt.datetime.now(dt.timezone.utc).isoformat(), source_sha256=source_hash())
    try:
        lock = json.loads((ROOT / 'config/toolchain.lock.json').read_text(encoding='utf-8'))
        engine = Path(args.godot).resolve() if args.godot else (ROOT / lock['console_path']).resolve()
        if sha(engine) not in {lock['console_sha256'], lock['editor_sha256']}:
            raise BuildFailure('Godot binary hash differs from lock')
        editor = engine.parent / Path(lock['editor_path']).name
        if sha(editor) != lock['editor_sha256']:
            raise BuildFailure('Godot editor sibling hash differs from lock')
        for name, expected in lock['template_binaries'].items():
            if sha(ROOT / lock['templates_root'] / name) != expected:
                raise BuildFailure('Export template checksum mismatch: ' + name)
        if (ROOT / lock['templates_root'] / 'version.txt').read_text().strip() != lock['export_templates_version']:
            raise BuildFailure('Export templates version mismatch')
        record, version = run_step('version', [str(engine), '--version'], logs, args.timeout)
        manifest['steps'].append(record)
        if not version.strip().startswith(lock['godot_version'] + '.stable.'):
            raise BuildFailure('Godot version differs from pin')
        manifest.update(engine_version=version.strip(), engine_sha256=sha(editor), template_hashes=lock['template_binaries'])
        base = [str(engine), '--headless', '--path', str(ROOT)]
        record, _ = run_step('import', base + ['--import'], logs, args.timeout)
        manifest['steps'].append(record)
        for suite in ['bootstrap', 'scene']:
            if not (ROOT / 'tests/test_runner.gd').is_file():
                raise BuildFailure('Test runner absent: NOT_TESTED')
            record, stdout = run_step(suite, base + ['--script', 'res://tests/test_runner.gd', '--', '--suite', suite], logs, args.timeout)
            record['test_report'] = test_report(stdout)
            manifest['steps'].append(record)
        binary = output / 'TheSeventhHouse.exe'
        record, _ = run_step('export', base + ['--export-release', args.preset, str(binary)], logs, args.timeout)
        manifest['steps'].append(record)
        for path in [binary, binary.with_suffix('.pck')]:
            if not path.is_file() or path.stat().st_size == 0:
                raise BuildFailure('Expected export artifact missing/empty: ' + str(path))
        scratch = ROOT / '.qa/build_checks' / build_id
        scratch.mkdir(parents=True, exist_ok=False)
        (scratch / 'project.godot').write_text('config_version=5\n[application]\nconfig/name="Pack inspection fixture"\n')
        record, stdout = run_step('pack_contents', [str(engine), '--headless', '--path', str(scratch),
                                   '--script', str(ROOT / 'tests/fixtures/inspect_pack.gd'), '--',
                                   str(binary.with_suffix('.pck'))], logs, args.timeout)
        records = re.findall(r'^PACK_REPORT (.+)$', stdout, re.MULTILINE)
        if len(records) != 1 or json.loads(records[0]).get('result') != 'PASS':
            raise BuildFailure('Export package inspection did not pass')
        record['pack_report'] = json.loads(records[0])
        manifest['steps'].append(record)
        manifest['artifacts'] = [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha(p), bytes=p.stat().st_size)
                                 for p in output.iterdir() if p.is_file()]
        manifest.update(result='PASS', limitations=['Export build only; Windows rendered executable smoke is a separate check.',
                                                   'Bootstrap content, not a finished campaign or retail release.'])
    except (OSError, ValueError, KeyError, BuildFailure) as error:
        manifest['error'] = str(error)
        print('BUILD FAILED:', error, file=sys.stderr)
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    (logs / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'result':manifest['result'], 'manifest':str(output/'manifest.json'), 'logs':str(logs)}))
    return 0 if manifest['result'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
