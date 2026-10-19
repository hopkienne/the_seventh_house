#!/usr/bin/env python3
"""Validate the document/backlog package, NOT the Godot game. Standard library only."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

def validate(root:Path)->dict:
    errors=[]
    def read(rel):
        try:return json.loads((root/rel).read_text(encoding='utf-8'))
        except (OSError,ValueError) as e:errors.append(f'{rel}: {e}');return {}
    plan=read('plan/backlog.json');state=read('state/task_state.json')
    tasks=plan.get('tasks',[]);stories=plan.get('stories',[]);sprints=plan.get('sprints',[])
    def unique(items,key,label):
        vals=[x.get(key) for x in items]
        if len(vals)!=len(set(vals)):errors.append(f'Duplicate {label} IDs')
    for items,label in [(tasks,'task'),(stories,'story'),(sprints,'sprint'),(plan.get('requirements',[]),'requirement')]:unique(items,'id',label)
    td={t['id']:t for t in tasks};sd={s['id']:s for s in stories};sp={s['id']:s for s in sprints};req={r['id'] for r in plan.get('requirements',[])}
    for key,items in [('task_count',tasks),('story_count',stories),('sprint_count',sprints)]:
        if plan.get('meta',{}).get(key)!=len(items):errors.append(f'Meta count mismatch: {key}')
    if set(state.get('tasks',{}))!=set(td):errors.append('State/definition task ID sets differ')
    for t in tasks:
        if t['story'] not in sd or t['sprint'] not in sp:errors.append(f'{t["id"]}: parent missing')
        elif t['id'] not in sd[t['story']]['tasks'] or sd[t['story']]['sprint']!=t['sprint']:errors.append(f'{t["id"]}: parent mismatch')
        for field in ['goal','outputs','acceptance_criteria','implementation_steps','verification','read_before','required_verification','mode','evidence_path','review_path']:
            if not t.get(field):errors.append(f'{t["id"]}: empty {field}')
        if 'hours' in t or 'actual_hours' in t:errors.append(f'{t["id"]}: legacy staffing hours remain active')
        for d in t.get('depends_on_tasks',[]):
            if d not in td:errors.append(f'{t["id"]}: unknown dependency {d}')
            elif int(td[d]['sprint'][1:])>int(t['sprint'][1:]):errors.append(f'{t["id"]}: future-wave dependency {d}')
        for r in t.get('requirement_refs',[]):
            if r not in req:errors.append(f'{t["id"]}: unknown requirement {r}')
        for p in t['read_before']+[f'tasks/{t["id"]}.md']:
            if not (root/p).is_file():errors.append(f'{t["id"]}: missing context/card {p}')
        if state['tasks'].get(t['id'],{}).get('status') not in {'NOT_STARTED','IN_PROGRESS','IN_REVIEW','DONE','NOT_APPLICABLE','BLOCKED_DEPENDENCY','BLOCKED_CAPABILITY','BLOCKED_EXTERNAL'}:errors.append(f'{t["id"]}: invalid state')
        if state['tasks'].get(t['id'],{}).get('status')=='NOT_APPLICABLE' and not t['conditional']:errors.append(f'{t["id"]}: mandatory task skipped')
    color={};order=[]
    def visit(x):
        if color.get(x)==1:errors.append(f'Dependency cycle near {x}');return
        if color.get(x)==2:return
        color[x]=1
        for y in td[x].get('depends_on_tasks',[]):
            if y in td:visit(y)
        color[x]=2;order.append(x)
    for x in td:visit(x)
    for s in stories:
        if not (root/f'stories/{s["id"]}.md').is_file():errors.append(f'Missing story card {s["id"]}')
        if any(t not in td for t in s['tasks']):errors.append(f'Unknown task in {s["id"]}')
    for s in sprints:
        if not (root/f'sprints/{s["id"]}.md').is_file():errors.append(f'Missing sprint card {s["id"]}')
    chapter=read('specs/chapter_catalog.json');puzzles=read('specs/puzzle_catalog.json');evidence=read('specs/evidence_catalog.json');route=read('specs/evacuation_route.json')
    if len(chapter)!=7:errors.append('Expected seven chapter contracts')
    if len(puzzles)!=14:errors.append('Expected fourteen puzzle contracts')
    if len(evidence)!=28:errors.append('Expected twenty-eight evidence records')
    if isinstance(evidence,list):
        unique(evidence,'id','evidence');valid={f'E{i:02}' for i in range(1,15)}|{f'M{i:02}' for i in range(1,8)}|{f'L{i:02}' for i in range(1,8)}
        if {e['id'] for e in evidence}!=valid:errors.append('Evidence namespace mismatch')
    if isinstance(puzzles,list):
        for p in puzzles:
            if not p.get('solution') or not p.get('actions') or len(p.get('hints',[]))!=3:errors.append(f'Incomplete puzzle contract {p.get("id")}')
            if not (root/f'specs/puzzles/{p["id"]}.md').is_file():errors.append('Missing puzzle card '+p['id'])
    edges=route.get('segments',[])
    if len(edges)!=7 or [e.get('memory_id') for e in edges]!=[f'M{i:02}' for i in range(1,8)]:errors.append('Route segment IDs/count wrong')
    if edges and (edges[0]['from']!=route['start'] or edges[-1]['to']!=route['end'] or any(a['to']!=b['from'] for a,b in zip(edges,edges[1:]))):errors.append('Route is disconnected')
    if len({e.get('from') for e in edges})!=len(edges):errors.append('Route repeats source node')
    for f in root.rglob('*.json'):
        try:json.loads(f.read_text(encoding='utf-8'))
        except (OSError,ValueError) as e:errors.append(f'Invalid JSON {f.relative_to(root)}: {e}')
    return {'result':'PASS' if not errors else 'FAIL','scope':'DOCUMENT_PACKAGE_ONLY_NOT_GAME_QA','counts':{'sprints':len(sprints),'stories':len(stories),'tasks':len(tasks),'chapters':len(chapter),'puzzles':len(puzzles),'journal_records':len(evidence)},'checks':['unique_ids','parent_references','task_fields','no_active_staffing_hours','dependency_exists','dependency_acyclic','no_future_wave_dependency','read_before_paths','task_story_sprint_cards','state_id_sets','content_counts','puzzle_solutions_hints','route_connectivity','json_parse'],'errors':errors,'topological_first_tasks':order[:8]}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));ap.add_argument('--output');a=ap.parse_args()
    try:result=validate(Path(a.root).resolve())
    except (KeyError,TypeError,ValueError) as e:result={'result':'FAIL','scope':'DOCUMENT_PACKAGE_ONLY_NOT_GAME_QA','errors':[str(e)]}
    text=json.dumps(result,ensure_ascii=False,indent=2);print(text)
    if a.output:
        p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text+'\n',encoding='utf-8')
    return 0 if result['result']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
