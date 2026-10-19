#!/usr/bin/env python3
"""Local task ledger controller. Does not implement the game or run in the background.
Only the orchestrator should mutate the shared ledger. Python 3 standard library.
Evidence validation is structural; the reviewer must verify its factual accuracy.
"""
from __future__ import annotations
import argparse, contextlib, datetime as dt, glob, hashlib, json, os, sys
from pathlib import Path
from typing import Any

TERMINAL = {'DONE', 'NOT_APPLICABLE'}
BLOCKED = {'BLOCKED_DEPENDENCY', 'BLOCKED_CAPABILITY', 'BLOCKED_EXTERNAL'}
HARD_GATES = [('G0',2),('G1',5),('G2',11),('G3',13),('G4',27),('G5',29),('G6',31),('G7',35)]

class LedgerError(Exception): pass

def load_json(path: Path) -> dict:
    try:
        data=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data,dict): raise LedgerError(f'Expected JSON object: {path}')
        return data
    except (OSError,ValueError) as e: raise LedgerError(f'Cannot read {path}: {e}') from e

def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('w',encoding='utf-8') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

def inside(root: Path, rel: str) -> Path:
    if not isinstance(rel,str) or not rel.strip(): raise LedgerError('Missing relative path')
    p=(root/rel).resolve()
    try: p.relative_to(root.resolve())
    except ValueError: raise LedgerError(f'Path outside repository: {rel}')
    return p

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def now()->str:return dt.datetime.now(dt.timezone.utc).isoformat()

@contextlib.contextmanager
def lock(root: Path):
    p=root/'state/.agentctl.lock';p.parent.mkdir(parents=True,exist_ok=True)
    try: fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError: raise LedgerError('Ledger locked. Check live writer; do not delete an active lock. For stale lock verify no writer, then remove this file explicitly.')
    try:
        os.write(fd,f'pid={os.getpid()}\nstarted={now()}\n'.encode());os.close(fd)
        yield
    finally:
        p.unlink(missing_ok=True)

def prerequisites(t:dict,state:dict)->list[str]:
    missing=[d for d in t['depends_on_tasks'] if state['tasks'].get(d,{}).get('status') not in TERMINAL]
    sn=int(t['sprint'][1:])
    for gid,threshold in HARD_GATES:
        if sn>=threshold:
            g=state.get('gates',{}).get(gid,{})
            if gid=='G7':
                if g.get('technical_status')!='PASS':missing.append('G7_TECH')
                if g.get('public_status')!='PASS':missing.append('G7_PUBLIC')
            elif g.get('status')!='PASS':missing.append(gid)
    return sorted(set(missing))

def ready_tasks(plan:dict,state:dict)->list[dict]:
    result=[]
    for t in plan['tasks']:
        st=state['tasks'][t['id']]['status']
        if st in TERMINAL or st in BLOCKED:continue
        if not prerequisites(t,state):result.append(t)
    return sorted(result,key=lambda t:(0 if state['tasks'][t['id']]['status'] in {'IN_PROGRESS','IN_REVIEW'} else 1,int(t['sprint'][1:]),t['id']))

def _real_text(value:Any,field:str)->None:
    if not isinstance(value,str) or not value.strip() or 'REPLACE' in value or value in {'NOT_RUN','UNKNOWN'}:
        raise LedgerError(f'Unfilled evidence field: {field}')

def evidence_artifacts(root:Path,data:dict)->set[Path]:
    records=data.get('artifacts',[])
    if not records:raise LedgerError('Evidence needs real artifact files')
    found=set()
    for a in records:
        p=inside(root,a.get('path',''))
        if not p.is_file() or p.stat().st_size==0:raise LedgerError(f'Missing/empty artifact: {p}')
        if a.get('sha256')!=sha(p):raise LedgerError(f'Artifact SHA256 mismatch: {a.get("path")}')
        found.add(p)
    return found

def authorization(root:Path,ref:Any)->dict:
    if not isinstance(ref,str):raise LedgerError('External action needs authorization_ref')
    a=load_json(inside(root,ref))
    if a.get('approved') is not True:raise LedgerError('Authorization not approved')
    for k in ['authorization_id','approved_by','record_path']:_real_text(a.get(k),k)
    record=inside(root,a['record_path'])
    if not record.is_file() or not record.stat().st_size:raise LedgerError('Missing real owner authorization record')
    if not a.get('allowed_operations'):raise LedgerError('Authorization operation scope missing')
    if a.get('expires_at'):
        try: exp=dt.datetime.fromisoformat(a['expires_at'].replace('Z','+00:00'))
        except ValueError as e:raise LedgerError('Invalid authorization expiry') from e
        if exp.tzinfo is None or exp<dt.datetime.now(dt.timezone.utc):raise LedgerError('Expired or timezone-free authorization')
    return a

def validate_evidence(root:Path,t:dict,rel:str,skip:bool=False)->dict:
    data=load_json(inside(root,rel))
    if data.get('task_id')!=t['id']:raise LedgerError('Evidence task_id mismatch')
    expected='NOT_APPLICABLE' if skip else 'PASS'
    if data.get('result')!=expected:raise LedgerError(f'Evidence result must be {expected}')
    for field in ['executor_id','revision','created_at']:_real_text(data.get(field),field)
    try:
        stamp=dt.datetime.fromisoformat(data['created_at'].replace('Z','+00:00'))
        if stamp.tzinfo is None:raise ValueError('timezone missing')
    except ValueError as e:raise LedgerError('created_at must be ISO datetime with timezone') from e
    review=data.get('review',{})
    if review.get('result')!=expected:raise LedgerError('Reviewer result missing/not accepted')
    _real_text(review.get('reviewer_id'),'reviewer_id')
    if not isinstance(review.get('self_review'),bool):raise LedgerError('Declare self_review true/false')
    rp=inside(root,review.get('path',''))
    if not rp.is_file() or not rp.stat().st_size:raise LedgerError('Review file missing/empty')
    files=evidence_artifacts(root,data)
    checks=data.get('checks',[])
    if not checks:raise LedgerError('Evidence has zero checks')
    kinds=set()
    for ch in checks:
        if ch.get('result')!='PASS':raise LedgerError('Required check FAIL/NOT_TESTED cannot close task')
        for field in ['id','kind','expected','observed']:_real_text(ch.get(field),field)
        kinds.add(ch['kind'])
        if ch['kind'] in {'ENGINE_TEST','RENDERED_RUNTIME','WINDOWS_RUNTIME','AUDIO_REVIEW','EXTERNAL_RESULT'}:
            lp=inside(root,ch.get('log_path',''))
            if not lp.is_file() or not lp.stat().st_size:raise LedgerError('Runtime/external check needs actual log')
        if ch['kind']=='ENGINE_TEST' and (not isinstance(ch.get('assertions'),int) or ch['assertions']<1):
            raise LedgerError('Zero assertions is not a passing engine test')
        if ch['kind'] in {'RENDERED_RUNTIME','WINDOWS_RUNTIME'}:
            caps=ch.get('capture_paths',[])
            if not caps or any(not inside(root,p).is_file() for p in caps):raise LedgerError('Rendered/native check needs capture files')
        if ch['kind']=='WINDOWS_RUNTIME' and ch.get('native_os')!='Windows':raise LedgerError('Native Windows verification not provided')
    if skip:
        if not t.get('conditional'):raise LedgerError('Cannot skip a non-conditional task')
        _real_text(data.get('not_applicable_reason'),'not_applicable_reason')
    else:
        for k in t['required_verification']:
            if k not in kinds:raise LedgerError(f'Missing verification kind: {k}')
        for pattern in t['outputs']:
            # Planned directories/globs must be resolved to real, hashed output files.
            match=[]
            for name in glob.glob(str(inside(root,pattern)),recursive=True):
                p=Path(name)
                if p.is_dir():match.extend(x.resolve() for x in p.rglob('*') if x.is_file())
                elif p.is_file():match.append(p.resolve())
            if not match or not any(p in files for p in match):raise LedgerError(f'Output absent or not hashed: {pattern}')
        if t.get('external_action'):
            auth=authorization(root,data.get('authorization_ref'))
            act=data.get('external_action',{})
            if act.get('operation') not in auth['allowed_operations']:raise LedgerError('Operation outside authorization scope')
            for field in ['app_id','build_sha256','channel']:
                if auth.get(field) is not None and act.get(field)!=auth[field]:raise LedgerError(f'External action mismatches authorized {field}')
    return data

def main(argv:list[str]|None=None)->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1]))
    sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('summary');sub.add_parser('next')
    p=sub.add_parser('show');p.add_argument('task')
    p=sub.add_parser('start');p.add_argument('task');p.add_argument('--executor',required=True)
    p=sub.add_parser('review');p.add_argument('task')
    for cmd in ['finish','skip']:
        p=sub.add_parser(cmd);p.add_argument('task');p.add_argument('--evidence',required=True)
    p=sub.add_parser('block');p.add_argument('task');p.add_argument('--type',choices=sorted(BLOCKED),required=True);p.add_argument('--reason',required=True);p.add_argument('--needed',required=True);p.add_argument('--attempted',required=True)
    p=sub.add_parser('gate');p.add_argument('gate');p.add_argument('--evidence',required=True)
    args=ap.parse_args(argv);root=Path(args.root).resolve()
    try:
        plan=load_json(root/'plan/backlog.json');state_path=root/'state/task_state.json';state=load_json(state_path)
        tasks={t['id']:t for t in plan['tasks']}
        if args.cmd=='summary':
            counts={}
            for v in state['tasks'].values():counts[v['status']]=counts.get(v['status'],0)+1
            print(json.dumps({'plan_version':plan['meta']['version'],'counts':counts,'gates':state['gates'],'project_status':state.get('project_status'),'note':'Task status is not proof of game quality.'},ensure_ascii=False,indent=2));return 0
        if args.cmd=='next':
            ready=ready_tasks(plan,state)
            if not ready:
                print(json.dumps({'next':None,'message':'No eligible task. Inspect unfinished gates, dependencies and blockers; do not auto-skip.'},ensure_ascii=False));return 0
            t=ready[0]
            print(json.dumps({'task_id':t['id'],'status':state['tasks'][t['id']]['status'],'mode':t['mode'],'title':t['title'],'card':f'tasks/{t["id"]}.md','read_before':t['read_before'],'alternatives':[x['id'] for x in ready[1:6]]},ensure_ascii=False,indent=2));return 0
        if args.cmd=='show':
            if args.task not in tasks:raise LedgerError('Unknown task ID')
            print(json.dumps(tasks[args.task],ensure_ascii=False,indent=2));return 0
        with lock(root):
            state=load_json(state_path)
            if args.cmd=='gate':
                g=next((g for g in plan['gates'] if g['id']==args.gate),None)
                if not g:raise LedgerError('Unknown gate')
                ev=load_json(inside(root,args.evidence))
                if ev.get('gate_id')!=args.gate or ev.get('result') not in {'PASS','FAIL','BLOCKED'}:raise LedgerError('Invalid gate result/id')
                rp=inside(root,ev.get('review_file',''))
                if not rp.is_file() or not rp.stat().st_size:raise LedgerError('Gate review file missing')
                evidence_artifacts(root,ev)
                if ev['result']=='PASS':
                    if not ev.get('checks') or any(x.get('result')!='PASS' for x in ev['checks']):raise LedgerError('Gate missing passing checks')
                    limit=int(g['sprint'][1:])
                    # G0-G7 technical gates do not wait for account-dependent release work.
                    required=[t for t in plan['tasks'] if int(t['sprint'][1:])<=limit and (args.gate in {'G8','G9'} or t['task_type']!='release')]
                    incomplete=[t['id'] for t in required if state['tasks'][t['id']]['status'] not in TERMINAL]
                    if incomplete:raise LedgerError('Gate tasks incomplete: '+', '.join(incomplete[:12]))
                rec={'status':ev['result'],'evidence':args.evidence,'updated_at':now()}
                if args.gate=='G7':
                    rec['technical_status']=ev.get('technical_status','NOT_EVALUATED');rec['public_status']=ev.get('public_status','NOT_EVALUATED')
                    if rec['public_status']=='PASS':authorization(root,ev.get('authorization_ref'))
                    if rec['technical_status']=='PASS' and ev['result']!='PASS':raise LedgerError('Technical PASS requires accepted gate evidence')
                state['gates'][args.gate]=rec
            else:
                if args.task not in tasks:raise LedgerError('Unknown task ID')
                t=tasks[args.task];row=state['tasks'][args.task]
                if row['status'] in TERMINAL:raise LedgerError('Terminal task immutable. Open regression/ADR instead of overwriting evidence.')
                if args.cmd=='block':
                    row.update(status=args.type,blocker={'reason':args.reason,'needed':args.needed,'attempted':args.attempted})
                else:
                    missing=prerequisites(t,state)
                    if missing:raise LedgerError('Unmet prerequisites: '+', '.join(missing))
                    if args.cmd=='start':
                        active=[k for k,v in state['tasks'].items() if k!=args.task and v['status'] in {'IN_PROGRESS','IN_REVIEW'}]
                        if active:raise LedgerError('Sequential WIP limit; finish/block active task: '+','.join(active))
                        row.update(status='IN_PROGRESS',executor_id=args.executor,blocker=None)
                    elif args.cmd=='review':
                        if row['status']!='IN_PROGRESS':raise LedgerError('Review requires IN_PROGRESS')
                        row['status']='IN_REVIEW'
                    elif args.cmd in {'finish','skip'}:
                        if row['status']!='IN_REVIEW':raise LedgerError('Finish/skip requires a review pass (IN_REVIEW)')
                        data=validate_evidence(root,t,args.evidence,skip=args.cmd=='skip')
                        row.update(status='NOT_APPLICABLE' if args.cmd=='skip' else 'DONE',evidence=args.evidence,blocker=None)
                        row.setdefault('notes',[]).append({'closed_at':now(),'revision':data['revision'],'evidence_sha256':sha(inside(root,args.evidence))})
                row['updated_at']=now()
            state['revision']=int(state.get('revision',0))+1
            if state.get('gates',{}).get('G8',{}).get('status')=='PASS':state['project_status']='PUBLISHED'
            elif state.get('gates',{}).get('G7',{}).get('technical_status')=='PASS':state['project_status']='READY_FOR_RELEASE'
            elif any(v['status']!='NOT_STARTED' for v in state['tasks'].values()):state['project_status']='IN_PROGRESS'
            write_json(state_path,state)
        print(json.dumps({'operation':args.cmd,'id':getattr(args,'task',getattr(args,'gate',None)),'state_revision':state['revision']},ensure_ascii=False));return 0
    except (LedgerError,OSError,KeyError,TypeError) as e:
        print(f'ERROR: {e}',file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
