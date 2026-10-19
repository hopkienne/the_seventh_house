#!/usr/bin/env python3
"""Run the pinned engine and verify positive/negative runner exit/report contracts."""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', default='reports/verification/bootstrap')
    args = parser.parse_args()
    report_dir = (ROOT / args.report_dir).resolve()
    report_dir.relative_to((ROOT / 'reports').resolve())
    lock = json.loads((ROOT / 'config/toolchain.lock.json').read_text(encoding='utf-8'))
    engine = str((ROOT / lock['console_path']).resolve())
    runner = [engine, '--headless', '--path', str(ROOT), '--script', 'res://tests/test_runner.gd', '--']
    cases = [
        ('import', [engine, '--headless', '--path', str(ROOT), '--import'], 0, None),
        ('bootstrap', runner + ['--suite', 'bootstrap'], 0, True),
        ('negative_assertion', runner + ['--suite', 'bootstrap', '--fixture', 'res://tests/fixtures/bootstrap_failure.gd'], 1, False),
        ('unknown_suite', runner + ['--suite', 'not_registered'], 2, False),
        ('zero_tests', runner + ['--suite', 'bootstrap', '--filter', 'not_registered'], 1, False),
        ('missing_argument', runner + ['--suite'], 2, False),
        ('unknown_argument', runner + ['--no-such-option'], 2, False),
        ('fixture_outside_allowlist', runner + ['--suite', 'bootstrap', '--fixture', 'res://project.godot'], 2, False),
    ]
    report_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for name, command, expected_exit, positive in cases:
        try:
            process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                     encoding='utf-8', errors='replace', timeout=90)
            stdout, stderr, code = process.stdout, process.stderr, process.returncode
        except subprocess.TimeoutExpired as error:
            stdout, stderr, code = str(error.stdout), str(error.stderr) + '\nTIMEOUT', None
        (report_dir / f'{name}.stdout.log').write_text(stdout or '(empty stdout)\n', encoding='utf-8')
        (report_dir / f'{name}.stderr.log').write_text(stderr or '(empty stderr)\n', encoding='utf-8')
        reports = re.findall(r'^TEST_REPORT (.+)$', stdout, re.MULTILINE)
        report = json.loads(reports[-1]) if reports else None
        passed = code == expected_exit and not re.search(r'SCRIPT ERROR:|^ERROR:', stdout + stderr, re.MULTILINE)
        if positive is not None:
            passed = passed and report is not None
            if report:
                passed = passed and report['skipped'] == 0 and (report['result'] == 'PASS') == positive
                if positive:
                    passed = passed and report['tests'] > 0 and report['assertions'] > 0 and report['failed'] == 0
                else:
                    passed = passed and report['failed'] > 0
                if name == 'negative_assertion':
                    passed = passed and report['tests'] == 1 and report['assertions'] == 1
        record = dict(id=name, command=command, expected_exit=expected_exit, observed_exit=code,
                      result='PASS' if passed else 'FAIL', report=report,
                      stdout=(report_dir / f'{name}.stdout.log').relative_to(ROOT).as_posix(),
                      stderr=(report_dir / f'{name}.stderr.log').relative_to(ROOT).as_posix())
        results.append(record)
        print(name, record['result'], 'exit=', code, flush=True)
    summary = dict(result='PASS' if all(r['result'] == 'PASS' for r in results) else 'FAIL', cases=results)
    (report_dir / 'verification.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    return 0 if summary['result'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
