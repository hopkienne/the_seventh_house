"""Process/error handling tests, not fake gameplay tests."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('build_windows', Path(__file__).resolve().parents[1] / 'scripts/build_windows.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class BuildTests(unittest.TestCase):
    def test_valid_report(self):
        report = dict(result='PASS', tests=2, assertions=3, failed=0, skipped=0)
        self.assertEqual(build.test_report('TEST_REPORT '+json.dumps(report)), report)

    def test_zero_and_skipped_cannot_pass(self):
        for field, value in [('tests', 0), ('assertions', 0), ('skipped', 1), ('failed', 1)]:
            report = dict(result='PASS', tests=2, assertions=3, failed=0, skipped=0)
            report[field] = value
            with self.subTest(field=field), self.assertRaises(build.BuildFailure):
                build.test_report('TEST_REPORT '+json.dumps(report))

    def test_missing_report_cannot_pass(self):
        with self.assertRaises(build.BuildFailure):
            build.test_report('Engine exited 0 but ran no game tests')

    def test_exit_zero_engine_error_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(build.BuildFailure):
                build.run_step('fixture_error', [sys.executable, '-c', "print('ERROR: fixture engine failure')"], Path(temp), 5)
            self.assertIn('ERROR:', (Path(temp)/'fixture_error.stdout.log').read_text())

    def test_timeout_fails_and_logs(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(build.BuildFailure):
                build.run_step('fixture_timeout', [sys.executable, '-c', 'import time; time.sleep(2)'], Path(temp), 0.05)
            self.assertIn('TIMEOUT', (Path(temp)/'fixture_timeout.stderr.log').read_text())


if __name__ == '__main__':
    unittest.main(verbosity=2)
