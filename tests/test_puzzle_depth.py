"""Semantic regression of authored design rules; not Godot/puzzle player tests."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_puzzle_depth import validate,evacuation_plan_valid


class PuzzleDepthTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        (self.root/'specs').mkdir()
        for name in ['puzzle_catalog.json','gameplay_reasoning.json','deduction_models.json','ending_c_decisions.json']:
            p=ROOT/'specs'/name
            if p.exists():(self.root/'specs'/name).write_bytes(p.read_bytes())

    def tearDown(self):self.temp.cleanup()

    def edit(self,filename,action):
        p=self.root/'specs'/filename;data=json.loads(p.read_text(encoding='utf-8'));action(data)
        p.write_text(json.dumps(data),encoding='utf-8')

    def test_all_twenty_eight_have_consistent_reasoning(self):
        r=validate(self.root);self.assertEqual(r['result'],'PASS',r['errors'])
        self.assertEqual(r['valid_evacuation_plans'],8)

    def test_nonexistent_refutation_is_rejected(self):
        self.edit('puzzle_catalog.json',lambda ps:ps[6]['reasoning']['hypotheses'][0].update(refuted_by=['P99_C0']))
        self.assertTrue(any('provenance' in e for e in validate(self.root)['errors']))

    def test_reading_timer_is_rejected(self):
        self.edit('puzzle_catalog.json',lambda ps:ps[27]['reasoning']['tension'].update(advances_while_reading=True))
        self.assertTrue(any('reading timer' in e for e in validate(self.root)['errors']))

    def test_main_rule_cannot_require_only_secret_teacher(self):
        self.edit('gameplay_reasoning.json',lambda r:r['knowledge'][0].update(mandatory_teachers=['P04']))
        self.assertTrue(any('main knowledge reachable' in e for e in validate(self.root)['errors']))

    def test_copying_clue_route_is_not_a_second_route(self):
        self.edit('puzzle_catalog.json',lambda ps:ps[0]['reasoning']['observation_routes'].__setitem__(1,ps[0]['reasoning']['observation_routes'][0].copy()))
        self.assertTrue(any('distinct information' in e for e in validate(self.root)['errors']))

    def test_undefined_interaction_is_rejected(self):
        self.edit('puzzle_catalog.json',lambda ps:ps[5]['reasoning']['thought_path'][0].update(canonical_actions=['invented_action']))
        self.assertTrue(any('canonical interactions' in e for e in validate(self.root)['errors']))

    def test_bridge_must_accept_early_valid_crossing(self):
        self.edit('puzzle_catalog.json',lambda ps:ps[9].update(depends_on=['P09','P11']))
        self.assertTrue(any('hidden solved gate' in e for e in validate(self.root)['errors']))

    def model(self):return json.loads((self.root/'specs/ending_c_decisions.json').read_text(encoding='utf-8'))

    def test_library_safe_if_school_first(self):
        plan=dict(prefix=['HOLD','OPEN'],order=['GROUP_SCHOOL','GROUP_FAMILIES','GROUP_RIVERSIDE'],school_route='LIBRARY',finish='RETURN')
        self.assertTrue(evacuation_plan_valid(plan,self.model()))

    def test_library_unsafe_after_another_crossing(self):
        plan=dict(prefix=['HOLD','OPEN'],order=['GROUP_FAMILIES','GROUP_SCHOOL','GROUP_RIVERSIDE'],school_route='LIBRARY',finish='RETURN')
        self.assertFalse(evacuation_plan_valid(plan,self.model()))
        plan['school_route']='UPPER_GALLERY'
        self.assertTrue(evacuation_plan_valid(plan,self.model()))

    def test_duplicate_group_or_early_return_rejected(self):
        plan=dict(prefix=['HOLD','OPEN'],order=['GROUP_SCHOOL']*3,school_route='UPPER_GALLERY',finish='RETURN')
        self.assertFalse(evacuation_plan_valid(plan,self.model()))
        plan['order']=['GROUP_SCHOOL','GROUP_FAMILIES']
        self.assertFalse(evacuation_plan_valid(plan,self.model()))

    def test_wrong_gate_preparation_rejected(self):
        plan=dict(prefix=['OPEN','HOLD'],order=['GROUP_SCHOOL','GROUP_FAMILIES','GROUP_RIVERSIDE'],school_route='UPPER_GALLERY',finish='RETURN')
        self.assertFalse(evacuation_plan_valid(plan,self.model()))


if __name__=='__main__':unittest.main(verbosity=2)
