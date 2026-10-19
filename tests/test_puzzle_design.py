"""Regression for design migration checks; these do not run the Godot puzzles."""
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_puzzle_design import validate


class DesignContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        for rel in ['puzzle_catalog.json','chapter_catalog.json','evidence_catalog.json','evacuation_route.json','item_catalog.json']:
            p=self.root/'specs'/rel;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes((ROOT/'specs'/rel).read_bytes())
        (self.root/'specs/puzzles').mkdir()
        for n in range(1,29):(self.root/f'specs/puzzles/P{n:02}.md').write_text('Fixture card',encoding='utf-8')

    def tearDown(self):self.temp.cleanup()

    def edit(self,filename,action):
        p=self.root/'specs'/filename
        value=json.loads(p.read_text(encoding='utf-8'));action(value)
        p.write_text(json.dumps(value),encoding='utf-8')

    def test_canonical_contracts(self):
        result=validate(self.root)
        self.assertEqual(result['result'],'PASS',result['errors'])
        self.assertIn('NOT_RUNTIME',result['scope'])

    def test_old_fourteen_puzzle_package_rejected(self):
        self.edit('puzzle_catalog.json',lambda p:p.__delitem__(slice(14,None)))
        self.assertTrue(any('28 unique' in e for e in validate(self.root)['errors']))

    def test_duplicate_id_rejected(self):
        self.edit('puzzle_catalog.json',lambda p:p.append(copy.deepcopy(p[0])))
        self.assertTrue(any('28 unique' in e for e in validate(self.root)['errors']))

    def test_main_cannot_depend_on_secret(self):
        self.edit('puzzle_catalog.json',lambda p:p[27]['depends_on'].append('P27'))
        self.assertTrue(any('main depends' in e for e in validate(self.root)['errors']))

    def test_cycle_rejected(self):
        self.edit('puzzle_catalog.json',lambda p:p[0]['depends_on'].append('P03'))
        self.assertTrue(any('dependency cycle' in e for e in validate(self.root)['errors']))

    def test_m07_circular_reward_rejected(self):
        self.edit('evidence_catalog.json',lambda records:next(r for r in records if r['id']=='M07').update(source_puzzle='P27'))
        self.assertTrue(any('M07' in e for e in validate(self.root)['errors']))

    def test_plan_does_not_validate_evacuation(self):
        self.edit('evacuation_route.json',lambda r:r.update(validation_condition='P27_SOLVED'))
        self.assertTrue(any('separated' in e for e in validate(self.root)['errors']))

    def test_incorrect_valve_answer_rejected(self):
        self.edit('puzzle_catalog.json',lambda p:p[10]['solution'].update(turns_mod3=[1,1,1]))
        self.assertTrue(any('linked-valve' in e for e in validate(self.root)['errors']))

    def test_arbitrary_map_angle_rejected(self):
        self.edit('puzzle_catalog.json',lambda p:p[26]['solution']['rotations_degrees'].__setitem__(1,0))
        self.assertTrue(any('rotations' in e for e in validate(self.root)['errors']))


if __name__=='__main__':unittest.main(verbosity=2)
