import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import validate_game_data as validator


class DataValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.data = Path(self.temp.name)

    def tearDown(self):
        # Only test-owned temporary files; no repository data is removed.
        import time
        for attempt in range(5):
            try:
                self.temp.cleanup()
                return
            except OSError as error:
                if getattr(error, 'winerror', None) not in {32,145} or attempt == 4: raise
                time.sleep(0.05*(attempt+1))

    def write(self, path, value):
        destination = self.data/path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(value), encoding='utf-8')

    def product(self):
        self.write('runtime/product.json', {'product_id':'the_seventh_house','build_version':'0.1.0','release_target':'windows_x86_64','content_stage':'BOOTSTRAP'})

    def test_no_runtime_is_not_pass(self):
        result = validator.validate(self.data)
        self.assertEqual(result['result'], 'FAIL')
        self.assertEqual(result['files_checked'], 0)

    def test_bootstrap_is_partial_not_complete(self):
        self.product()
        self.assertEqual(validator.validate(self.data)['result'], 'PARTIAL')
        self.assertEqual(validator.validate(self.data, True)['result'], 'FAIL')

    def test_unknown_and_duplicate_ids_rejected(self):
        self.product()
        self.write('puzzles/catalog.json',[{'id':'P01'},{'id':'P01'},{'id':'P99'}])
        messages = [e['message'] for e in validator.validate(self.data)['errors']]
        self.assertTrue(any('Duplicate' in m for m in messages))
        self.assertTrue(any('Unknown' in m for m in messages))

    def test_dialogue_schema_and_translation_reference(self):
        self.product()
        line = {'id':'CH01_TEST','speaker':'MINH','text_key':'dialogue.test','vi':'Nhà ở đây.','en':'The house was here.','conditions':{},'events':[],'once':True}
        self.write('dialogue/CH01.json',{'chapter_id':'CH01','lines':[line]})
        self.write('localization/unused.json', {})
        path=self.data/'localization/strings.csv'
        path.write_text('keys,vi,en\nwrong.key,Sai,Wrong\n',encoding='utf-8')
        self.assertTrue(any('text reference' in e['message'] for e in validator.validate(self.data)['errors']))
        path.write_text('keys,vi,en\ndialogue.test,Nhà ở đây.,The house was here.\n',encoding='utf-8')
        self.assertFalse(validator.validate(self.data)['errors'])

    def test_invalid_save_schema_rejected(self):
        self.product()
        save=validator.read(validator.ROOT/'specs/fixtures/save_empty_CH01.json')
        save['slot_id']=4
        self.write('save_fixtures/slot.json', save)
        self.assertTrue(any('slot_id' in e['message'] for e in validator.validate(self.data)['errors']))

    def test_bad_csv_and_reference_types_report_errors(self):
        self.product()
        self.write('chapters/CH01.json', {'id':'CH01','chapter_id':[]})
        path=self.data/'localization/strings.csv'
        path.parent.mkdir(parents=True)
        path.write_text('keys,vi,en\nmissing_columns\n',encoding='utf-8')
        messages=[e['message'] for e in validator.validate(self.data)['errors']]
        self.assertIn('Unknown chapter reference', messages)
        self.assertIn('Empty translation key/VI/EN', messages)


if __name__ == '__main__':
    unittest.main(verbosity=2)
