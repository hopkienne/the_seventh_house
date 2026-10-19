"""Validate 3.2 reasoning authoring and finite models; never claims runtime usability."""
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def evacuation_plan_valid(plan, model):
    """Pure authored-rule fixture, NOT the game's evacuation implementation."""
    order=plan.get('order',[])
    if len(order)!=3 or set(order)!=set(model['groups']):return False
    if plan.get('prefix')!=['HOLD','OPEN'] or plan.get('finish')!='RETURN':return False
    route=model['school_routes'].get(plan.get('school_route'))
    return route is not None and order.index('GROUP_SCHOOL') in route['safe_at_beats']


def validate(root=ROOT):
    root=Path(root);errors=[];checks=[]
    def require(label,condition):
        checks.append(label)
        if not condition:errors.append(label)
    def read(rel):return json.loads((root/rel).read_text(encoding='utf-8'))
    puzzles=read('specs/puzzle_catalog.json');by_id={p['id']:p for p in puzzles}
    if not (root/'specs/gameplay_reasoning.json').is_file():
        return dict(result='FAIL',scope='STATIC_DESIGN_DEPTH_NOT_RUNTIME',checks_count=1,errors=['Missing gameplay3.2 reasoning catalog'])
    rules=read('specs/gameplay_reasoning.json');models=read('specs/deduction_models.json')
    knowledge={k['id']:k for k in rules['knowledge']}
    clues={c['id']:p['id'] for p in puzzles for c in p['clues']}
    require('Clue IDs unique',len(clues)==sum(len(p['clues']) for p in puzzles))
    def ancestors(pid,seen=None):
        seen=set() if seen is None else seen
        for d in by_id[pid]['depends_on']:
            if d in by_id and d not in seen:seen.add(d);ancestors(d,seen)
        return seen
    for p in puzzles:
        pid=p['id'];d=p.get('reasoning',{})
        required=['question','hypotheses','accepted_hypothesis','thought_path','observation_routes','feedback','tension','payoff','research_refs']
        require(pid+': authored reasoning fields',all(d.get(f) for f in required))
        if not d:continue
        hs={h['id']:h for h in d['hypotheses']}
        require(pid+': one accepted physical/causal claim',d['accepted_hypothesis'] in hs and sum(h['accepted'] for h in hs.values())==1)
        for h in hs.values():
            refs=h.get('supported_by',[]) if h['accepted'] else h.get('refuted_by',[])
            require(pid+': hypothesis '+h['id']+' has real clue provenance',bool(refs) and all(c in clues for c in refs))
        for i,step in enumerate(d['thought_path']):
            require(pid+': inference '+str(i)+' has discoverable sources',bool(step['observations']) and all(c in clues for c in step['observations']))
            acts=step.get('canonical_actions',[])
            require(pid+': inference '+str(i)+' uses canonical interactions',bool(acts) and step['action'] in acts and set(acts)<=set(p['actions']))
        routes=d['observation_routes']
        require(pid+': two distinct information routes',len(routes)>=2 and len({tuple(r.get('entry_clues',[])) for r in routes})>=2 and len({r['lead'] for r in routes})>=2)
        for r in routes:
            require(pid+': route '+r['id']+' uses local discoverable clues',len(r['clues'])>=2 and bool(r.get('entry_clues')) and set(r['entry_clues'])<=set(r['clues']) and all(clues.get(c)==pid for c in r['clues']) and all(set(step['observations'])<=set(r['clues']) for step in d['thought_path']))
        require(pid+': observations do not become hidden input gates',d.get('observation_gates_solution') is False)
        require(pid+': feedback does not reveal per-slot correctness',d['feedback'].get('per_slot_oracle') is False)
        require(pid+': no reading timer',d['tension'].get('advances_while_reading') is False)
        require(pid+': valid research provenance',set(d['research_refs'])<=set(rules['research_ids']))
        for kid in d.get('uses_knowledge',[]):
            require(pid+': known knowledge '+kid,kid in knowledge)
            if kid not in knowledge:continue
            teachers=knowledge[kid]['mandatory_teachers']
            available=[t for t in teachers if t in by_id and by_id[t]['required_for_main'] and
                       (by_id[t]['chapter']<p['chapter'] or t in ancestors(pid) or t==pid and kid in d.get('local_reteaching',[]) or
                        t in knowledge[kid].get('observation_teachers_at_entry',[]) and by_id[t]['chapter']==p['chapter'] and not by_id[t]['depends_on'])]
            require(pid+': main knowledge reachable '+kid,bool(available) or not p['required_for_main'])
        for target in d['payoff'].get('callbacks',[]):
            require(pid+': callback target exists and not earlier',target in by_id and by_id[target]['chapter']>=p['chapter'])
    require('P06 independent of P05 key',by_id['P06']['depends_on']==[] and 'H02_INNER_KEY' not in by_id['P06']['items']['inputs'])
    require('P10 uses information without hidden solved gate',by_id['P10']['depends_on']==[] and set(by_id['P10'].get('information_inputs',[]))=={'P09','P11'} and by_id['P11']['depends_on']==[])
    require('P18 joins P17 and P19',set(by_id['P18']['depends_on'])=={'P17','P19'} and by_id['P19']['depends_on']==[])
    require('P28 joins both mandatory tasks',set(by_id['P28']['depends_on'])=={'P25','P26'})
    # Independent finite checks, not assertion that a screenshot makes a clue readable.
    seats=models['P05'];valid=[]
    for order in itertools.permutations(seats['people']):
        m=dict(zip(seats['directions'],order))
        if m['north']=='MOTHER' and m['east']=='SON_A' and m['south']=='HANH':valid.append(m)
    require('P05 unique seating from authored relationships',valid==[{k:by_id['P05']['solution'][k] for k in seats['directions']}])
    routes=models['P12'];safe=[r['id'] for r in routes['options'] if routes['arrival_minutes']+r['walk_minutes']<r['flood_minutes']]
    require('P12 arrival and travel eliminate unsafe routes',safe==[by_id['P12']['solution']['safe_route']])
    letters=models['P17'];auth=[r['id'] for r in letters['letters'] if r['seal_continuous'] and r['ink_bleed']]
    require('P17 authenticity requires both marks',auth==by_id['P17']['solution']['authentic'])
    school=models['P16']
    for path in by_id['P16']['solution']['accepted_paths']:
        edges=list(zip(path,path[1:]))
        require('P16 path has real non-flooded doors '+str(path),all(list(e) in school['edges'] and list(e) not in school['blocked_edges'] for e in edges))
    model=read('specs/ending_c_decisions.json');accepted=[]
    for order in itertools.permutations(model['groups']):
        for route in model['school_routes']:
            plan=dict(prefix=['HOLD','OPEN'],order=list(order),school_route=route,finish='RETURN')
            if evacuation_plan_valid(plan,model):accepted.append(plan)
    require('P28 exactly eight valid plans, not one walkthrough',len(accepted)==8)
    require('P28 water changes only on committed crossing',model['advance_event']=='GROUP_CROSS_COMMITTED' and model['advances_while_reading'] is False)
    require('P28 library route requires P16 actual geometry',model['school_routes']['LIBRARY']['path'] in by_id['P16']['solution']['accepted_paths'])
    require('P28 gallery route requires P16 actual geometry',model['school_routes']['UPPER_GALLERY']['path'] in by_id['P16']['solution']['accepted_paths'])
    return dict(result='FAIL' if errors else 'PASS',scope='STATIC_DESIGN_DEPTH_NOT_RUNTIME',checks_count=len(checks),errors=errors,
                valid_evacuation_plans=len(accepted),human_usability='HUMAN_USABILITY_NOT_ASSESSED')


if __name__=='__main__':
    result=validate();print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['result']!='PASS')
