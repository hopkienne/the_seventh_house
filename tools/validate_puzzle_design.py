"""Check authoring contracts and finite design fixtures, NOT playable game quality."""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    root = Path(root)
    errors, checks = [], []

    def require(label, condition):
        checks.append(label)
        if not condition: errors.append(label)

    def read(rel):
        return json.loads((root / rel).read_text(encoding='utf-8'))

    puzzles = read('specs/puzzle_catalog.json')
    chapters = read('specs/chapter_catalog.json')
    records = read('specs/evidence_catalog.json')
    route = read('specs/evacuation_route.json')
    by_id = {p['id']: p for p in puzzles}
    require('28 unique puzzle IDs P01..P28', len(puzzles)==len(by_id)==28 and set(by_id)=={f'P{i:02}' for i in range(1,29)})
    if set(by_id)!={f'P{i:02}' for i in range(1,29)}:
        return dict(result='FAIL', scope='STATIC_DESIGN_CONSISTENCY_NOT_RUNTIME_OR_HUMAN_PLAYTEST',
                    checks_count=len(checks),checks=checks,errors=errors,puzzles=len(puzzles),
                    main_required=sum(p.get('required_for_main',False) for p in puzzles),
                    human_usability='HUMAN_USABILITY_NOT_ASSESSED')
    require('roles 14 CORE / 7 SUPPORT / 7 SECRET', Counter(p.get('role') for p in puzzles)=={'CORE':14,'SUPPORT':7,'SECRET':7})
    require('21 main-required and secret not required', sum(p.get('required_for_main',False) for p in puzzles)==21 and all(p.get('required_for_main')==(p['role']!='SECRET') for p in puzzles))
    fields=['scene','clues','inference','actions','solution','items','negative_case','hints','horror','persistent_fields']
    for p in puzzles:
        pid=p['id']
        require(pid+': complete playable-design fields', all(p.get(f) for f in fields))
        require(pid+': at least two located clues', len(p.get('clues',[]))>=2 and all(c.get('id') and c.get('location') and c.get('observation') for c in p['clues']))
        require(pid+': exactly three nonempty hints', len(p['hints'])==3 and all(p['hints']))
        require(pid+': dependencies known', all(d in by_id for d in p['depends_on']))
        require(pid+': no main depends directly on secret', not p['required_for_main'] or all(by_id[d]['role']!='SECRET' for d in p['depends_on'] if d in by_id))
        require(pid+': rewards reference known records', set(p['rewards']) <= {r['id'] for r in records})
        require(pid+': card exists', (root/f'specs/puzzles/{pid}.md').is_file())
    color={}

    def visit(pid, stack):
        if color.get(pid)==1:
            errors.append('dependency cycle: '+' -> '.join(stack+[pid]));return
        if color.get(pid)==2:return
        color[pid]=1
        for d in by_id[pid]['depends_on']:
            if d in by_id:visit(d,stack+[pid])
        color[pid]=2
    for pid in by_id:visit(pid,[])
    checks.append('puzzle dependency DAG')
    for c in chapters:
        own={p['id'] for p in puzzles if p['chapter']==c['id']}
        required={pid for pid in own if by_id[pid]['required_for_main']}
        require(c['id']+': four own puzzles / three required / one secret', len(own)==4 and own==set(c['all_puzzles']) and len(required)==3 and required==set(c['required_puzzles']) and len(c['secret_puzzles'])==1)
        require(c['id']+': roles listed correctly', set(c['main_puzzles'])=={pid for pid in own if by_id[pid]['role']=='CORE'} and set(c['support_puzzles'])=={pid for pid in own if by_id[pid]['role']=='SUPPORT'} and set(c['secret_puzzles'])=={pid for pid in own if by_id[pid]['role']=='SECRET'})
    sources=Counter(r for p in puzzles for r in p['rewards'])
    require('each E/M reward exactly once; lore is separate inspect', sources==Counter({r['id']:1 for r in records if r['kind']!='LORE'}))
    for r in records:
        if r['kind'] in {'ESSENTIAL','MEMORY'}:
            require(r['id']+': reward source matches catalog', r.get('source_puzzle') in by_id and r['id'] in by_id[r['source_puzzle']]['rewards'])
    require('M07 from P25, not circular P27', next(r for r in records if r['id']=='M07')['source_puzzle']=='P25' and 'P27' not in by_id['P25']['depends_on'])
    require('P28 main requires P25/P26 without optional P27', set(by_id['P28']['depends_on'])=={'P25','P26'})
    require('plan and validation separated', route.get('plan_flag')=='route_plan_ready' and route.get('validation_flag')=='evacuation_route_validated' and route.get('plan_puzzle')=='P27' and route.get('execution_puzzle')=='P28' and route.get('validation_condition')=='P28_THREE_GROUPS_SAFE')
    require('water is decision-based', route.get('water_progress')=='DECISION_BEATS_ONLY')
    angles=by_id['P27']['solution']['rotations_degrees']
    require('P27 rotations derived from printed north marks', len(angles)==7 and all((a+s['printed_north_degrees'])%360==0 for a,s in zip(angles,route['segments'])))
    require('P27 group joins are actual route nodes', set(by_id['P27']['solution']['group_join_nodes'].values()) <= {s['from'] for s in route['segments']}|{route['end']})
    # Finite model verifies the documented valve answer is possible and unique modulo3.
    model=by_id['P11']['solution']
    solutions=[]
    for turns in itertools.product(range(3),repeat=3):
        observed=[(model['initial'][j]-1+sum(turns[k]*model['coupling'][k][j] for k in range(3)))%3+1 for j in range(3)]
        if observed==model['target']:solutions.append(list(turns))
    require('P11 linked-valve answer unique modulo3', solutions==[model['turns_mod3']])
    require('P13 ordering constraints have one answer', [list(v) for v in itertools.permutations(['READING','DRAWING','MUSIC']) if v.index('READING')<v.index('DRAWING')<v.index('MUSIC')]==[by_id['P13']['solution']['sequence']])
    require('P22 pull order distinct from gear settings', by_id['P22']['solution']['pull_order']==[1,3,2] and by_id['P22']['solution']['gear_detents']==[0,2,1])
    require('P23 required evidence matches earlier source puzzles or entry photo', by_id['P23']['solution']['required_evidence']==['E08','E10','E12'] and by_id['P23']['solution']['relation']=='YOUNGER_SISTER')
    items=read('specs/item_catalog.json')
    valid_items={i['id'] for i in items['items']}
    valid_recipes={r['id'] for r in items['recipes']}
    require('item IDs unique', len(valid_items)==len(items['items']))
    for p in puzzles:
        require(p['id']+': known item and recipe IDs', set(p['items']['inputs']+p['items']['outputs'])<=valid_items and set(p['items']['recipes'])<=valid_recipes)
    for recipe in items['recipes']:
        require(recipe['id']+': valid consume/produce references', set(recipe['inputs']+recipe['outputs'])<=valid_items)
    return dict(result='FAIL' if errors else 'PASS',scope='STATIC_DESIGN_CONSISTENCY_NOT_RUNTIME_OR_HUMAN_PLAYTEST',
                checks_count=len(checks),checks=checks,errors=errors,puzzles=len(puzzles),main_required=21,
                human_usability='HUMAN_USABILITY_NOT_ASSESSED')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',default=str(ROOT));parser.add_argument('--output')
    args=parser.parse_args()
    result=validate(Path(args.root))
    output=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(output,encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['result']=='PASS' else 1)
