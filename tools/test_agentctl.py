#!/usr/bin/env python3
"""Regression tests for the ledger helper, not for Godot gameplay. No real task state writes."""
from __future__ import annotations
import contextlib,copy,io,json,tempfile,time,unittest
from pathlib import Path
import agentctl as a

class AgentCtlTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.task={'id':'T-TEST01','sprint':'S01','story':'ST-TEST','title':'Test artifact','mode':'ORCHESTRATOR','read_before':[],'depends_on_tasks':[],'outputs':['out.txt'],'conditional':False,'required_verification':['ARTIFACT_REVIEW'],'external_action':False,'task_type':'governance'}
        self.next=copy.deepcopy(self.task);self.next.update(id='T-TEST02',depends_on_tasks=['T-TEST01'])
        self.plan={'meta':{'version':'3.0'},'tasks':[self.task,self.next],'gates':[{'id':'G0','sprint':'S01'}]}
        self.state={'revision':0,'tasks':{t['id']:{'status':'NOT_STARTED','executor_id':None,'notes':[]} for t in self.plan['tasks']},'gates':{'G0':{'status':'NOT_EVALUATED'}},'project_status':'NOT_STARTED'}
        a.write_json(self.root/'plan/backlog.json',self.plan);a.write_json(self.root/'state/task_state.json',self.state)
        for f,v in [('out.txt','actual test artifact'),('review.md','Reviewer test pass'),('check.log','One real fixture assertion passed'),('capture.png','test capture placeholder only used by ledger test, not game evidence')]:
            (self.root/f).write_text(v)
        self.ev={'task_id':'T-TEST01','result':'PASS','executor_id':'test-executor','revision':'fixture-revision-for-tool-unit-test','created_at':a.now(),'review':{'result':'PASS','reviewer_id':'test-reviewer','self_review':True,'path':'review.md'},'artifacts':[{'path':'out.txt','sha256':a.sha(self.root/'out.txt')}],'checks':[{'id':'AC1','kind':'ARTIFACT_REVIEW','expected':'fixture exists','observed':'fixture reviewed in unit test','result':'PASS'}]}
        self.save_ev()
    def tearDown(self):
        # Windows filesystem observers can briefly retain a just-closed fixture directory.
        # Retry cleanup only; never retry or suppress a failed test assertion.
        for attempt in range(5):
            try:
                self.tmp.cleanup()
                return
            except OSError as error:
                if error.winerror not in {32,145} or attempt==4:
                    raise
                time.sleep(0.05*(attempt+1))
    def save_ev(self):a.write_json(self.root/'evidence.json',self.ev)
    def call(self,*args):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):return a.main(['--root',str(self.root),*args])
    def test_01_next_respects_dependency(self):self.assertEqual([t['id'] for t in a.ready_tasks(self.plan,self.state)],['T-TEST01'])
    def test_02_full_lifecycle(self):
        self.assertEqual(self.call('start','T-TEST01','--executor','e'),0)
        self.assertEqual(self.call('review','T-TEST01'),0)
        self.assertEqual(self.call('finish','T-TEST01','--evidence','evidence.json'),0)
        st=a.load_json(self.root/'state/task_state.json');self.assertEqual(st['tasks']['T-TEST01']['status'],'DONE');self.assertEqual(a.ready_tasks(self.plan,st)[0]['id'],'T-TEST02')
    def test_03_cannot_start_missing_dependency(self):self.assertEqual(self.call('start','T-TEST02','--executor','e'),2)
    def test_04_finish_needs_review(self):self.assertEqual(self.call('finish','T-TEST01','--evidence','evidence.json'),2)
    def test_05_hash_mismatch(self):
        self.ev['artifacts'][0]['sha256']='0'*64;self.save_ev()
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_06_missing_output(self):
        self.task['outputs']=['absent.txt']
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_07_not_tested_not_pass(self):
        self.ev['checks'][0]['result']='NOT_TESTED';self.save_ev()
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_08_mandatory_cannot_skip(self):
        self.ev['result']='NOT_APPLICABLE';self.ev['review']['result']='NOT_APPLICABLE';self.ev['not_applicable_reason']='No issue in tool fixture';self.save_ev()
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json',skip=True)
    def test_09_conditional_can_skip_with_evidence(self):
        self.task['conditional']=True;self.ev['result']='NOT_APPLICABLE';self.ev['review']['result']='NOT_APPLICABLE';self.ev['not_applicable_reason']='No issue in tool fixture';self.save_ev();a.validate_evidence(self.root,self.task,'evidence.json',skip=True)
    def test_10_zero_assertions_fail(self):
        self.ev['checks'][0].update(kind='ENGINE_TEST',assertions=0,log_path='check.log');self.save_ev()
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_11_native_windows_not_emulated(self):
        self.ev['checks'][0].update(kind='WINDOWS_RUNTIME',native_os='Linux',capture_paths=['capture.png'],log_path='check.log');self.save_ev()
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_12_path_escape(self):
        with self.assertRaises(a.LedgerError):a.inside(self.root,'../outside')
    def test_13_required_kind_missing(self):
        self.task['required_verification'].append('RENDERED_RUNTIME')
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_14_external_requires_auth(self):
        self.task['external_action']=True
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_15_block_and_resume(self):
        self.assertEqual(self.call('block','T-TEST01','--type','BLOCKED_CAPABILITY','--reason','no renderer','--needed','GPU runtime','--attempted','probe'),0)
        st=a.load_json(self.root/'state/task_state.json');self.assertFalse(a.ready_tasks(self.plan,st))
        self.assertEqual(self.call('start','T-TEST01','--executor','e'),0)
    def test_16_wip_limit(self):
        self.next['depends_on_tasks']=[];a.write_json(self.root/'plan/backlog.json',self.plan)
        self.assertEqual(self.call('start','T-TEST01','--executor','e'),0)
        self.assertEqual(self.call('start','T-TEST02','--executor','e'),2)
    def test_17_hard_gate(self):
        self.task['sprint']='S02';self.assertIn('G0',a.prerequisites(self.task,self.state))
    def test_18_active_task_first(self):
        self.next['depends_on_tasks']=[];self.state['tasks']['T-TEST02']['status']='IN_PROGRESS'
        self.assertEqual(a.ready_tasks(self.plan,self.state)[0]['id'],'T-TEST02')
    def test_19_lock_exclusion(self):
        with a.lock(self.root):
            with self.assertRaises(a.LedgerError):
                with a.lock(self.root):pass
        self.assertFalse((self.root/'state/.agentctl.lock').exists())
    def test_20_placeholder_evidence_rejected(self):
        self.ev['revision']='REPLACE_WITH_HASH';self.save_ev()
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_21_external_scope_checked(self):
        self.task['external_action']=True;(self.root/'permission-record.txt').write_text('Explicit test-only owner authorization fixture')
        a.write_json(self.root/'auth.json',{'approved':True,'authorization_id':'TEST-ONLY','approved_by':'fixture-owner','record_path':'permission-record.txt','allowed_operations':['upload_private'],'app_id':'123','build_sha256':'abc','channel':'private'})
        self.ev.update(authorization_ref='auth.json',external_action={'operation':'publish_public','app_id':'123','build_sha256':'abc','channel':'public'});self.save_ev()
        with self.assertRaises(a.LedgerError):a.validate_evidence(self.root,self.task,'evidence.json')
    def test_22_terminal_immutable(self):
        self.state['tasks']['T-TEST01']['status']='DONE';a.write_json(self.root/'state/task_state.json',self.state)
        self.assertEqual(self.call('start','T-TEST01','--executor','e'),2)

if __name__=='__main__':unittest.main(verbosity=2)
