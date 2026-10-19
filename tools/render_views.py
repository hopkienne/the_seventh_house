#!/usr/bin/env python3
"""Regenerate Markdown cards, CSV snapshots and offline HTML from canonical JSON.
Standard library only. Does NOT mutate state, execute game tasks, or rewrite XLSX.
"""
from __future__ import annotations
import argparse,csv,html,json,re,sys
from pathlib import Path

def task_markdown(t):
    bullets=lambda values:'\n'.join('- '+str(v) for v in values)
    steps=lambda values:'\n'.join(str(i+1)+'. '+str(v) for i,v in enumerate(values))
    return f'''# {t['id']} — {t['title']}

**Wave:** {t['sprint']} · **Story:** {t['story']} · **Mode:** {t['mode']} · **Priority:** {t['priority']} · **Complexity:** {t['complexity']} (không phải ETA)

## Goal
{t['goal']}

## Read before / context tối thiểu
{bullets('`'+x+'`' for x in t['read_before'])}
Đọc output dependency và implementation hiện có. Không nạp toàn bộ backlog. Trạng thái thực lấy từ `state/task_state.json`.

## Preconditions
Dependencies đã expand: {', '.join('`'+x+'`' for x in t['depends_on_tasks']) or 'Không có.'}
Capabilities: {', '.join(t['required_capabilities'])}. Permission: `{t['approval_required']}`. Chỉ xác nhận capability bằng probe thật; thiếu điều kiện kiểm thử phải ghi blocker.

## Outputs / allowed change scope
{bullets('`'+x+'`' for x in t['outputs'])}
Đây là output phải tạo trong repository, không phải source game có sẵn trong gói. Expand folder/glob thành file thật và hash trong evidence. Được thêm tests/helper liên quan; thay shared module phải ghi impact và review; không refactor lan rộng.

## Implementation steps
{steps(t['implementation_steps'])}

## Acceptance criteria
{bullets(t['acceptance_criteria'])}

## Verify / test
{steps(t['verification'])}
Verification kinds bắt buộc: **{', '.join(t['required_verification'])}**. Lệnh RUN-* và prerequisites trong `10_ENVIRONMENT_AND_COMMANDS.md`. Không gọi harness chưa tạo rồi báo PASS.

## Evidence / review / Done
Lưu `{t['evidence_path']}` và `{t['review_path']}` theo template. Mỗi claim có expected/observed/result, output/hash và log/capture phù hợp. Reviewer pass sau implementation; chỉ một agent phải khai self-review.
`{t['conditional_rule']}`
Sau khi evidence thực có, chạy `python tools/agentctl.py review {t['id']}` rồi `python tools/agentctl.py finish {t['id']} --evidence {t['evidence_path']}`.

## Blocked / resume
{t['blocked_behavior']}
{t['resume_instruction']}

## Không làm
{bullets(t['scope_guardrails'])}
'''

def md_table(head,rows):
    esc=lambda s:str(s).replace('|','\\|').replace('\n','; ')
    return '| '+' | '.join(head)+' |\n| '+' | '.join('---' for _ in head)+' |\n'+'\n'.join('| '+' | '.join(esc(v) for v in r)+' |' for r in rows)

def inline(text):
    s=html.escape(text)
    code=[]
    def save(m):code.append('<code>'+m[1]+'</code>');return f'@@CODE{len(code)-1}@@'
    s=re.sub(r'`([^`]+)`',save,s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    def link(m):
        url=html.unescape(m[2]);safe=url.startswith(('https://','http://','#')) or not re.match(r'^[\w+.-]+:',url)
        return '<a href="'+html.escape(url,quote=True)+'">'+m[1]+'</a>' if safe else m[1]
    s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',link,s)
    for i,c in enumerate(code):s=s.replace(f'@@CODE{i}@@',c)
    return s

def markdown(text):
    lines=text.splitlines();out=[];i=0
    while i<len(lines):
        l=lines[i]
        if not l.strip():i+=1;continue
        if l.startswith('```'):
            language=l[3:].strip();i+=1;code=[]
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            out.append('<pre><code data-language="'+html.escape(language)+'">'+html.escape('\n'.join(code))+'</code></pre>');i+=1;continue
        if re.match(r'^#{1,6} ',l):
            n=len(l)-len(l.lstrip('#'));out.append(f'<h{n}>'+inline(l[n:].strip())+f'</h{n}>');i+=1;continue
        if l.startswith('|') and i+1<len(lines) and re.match(r'^\|[\s:|\-]+\|?$',lines[i+1]):
            cells=lambda x:[c.strip() for c in re.split(r'(?<!\\)\|',x.strip().strip('|'))]
            out.append('<div class="tablewrap"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in cells(l))+'</tr></thead><tbody>');i+=2
            while i<len(lines) and lines[i].startswith('|'):
                out.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in cells(lines[i]))+'</tr>');i+=1
            out.append('</tbody></table></div>');continue
        m=re.match(r'^(?:- |\d+\. )',l)
        if m:
            ordered=l[0].isdigit();tag='ol' if ordered else 'ul';out.append('<'+tag+'>')
            while i<len(lines) and re.match(r'^(?:- |\d+\. )',lines[i]):
                out.append('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',lines[i]))+'</li>');i+=1
            out.append('</'+tag+'>');continue
        if l.startswith('> '):out.append('<blockquote>'+inline(l[2:])+'</blockquote>');i+=1;continue
        if re.match(r'^---+$',l):out.append('<hr>');i+=1;continue
        para=[l];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#{1,6} |```|\||- |\d+\. |> )',lines[i]):para.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(para))+'</p>')
    return '\n'.join(out)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));a=ap.parse_args();root=Path(a.root).resolve()
    try:
        plan=json.loads((root/'plan/backlog.json').read_text(encoding='utf-8'));state=json.loads((root/'state/task_state.json').read_text(encoding='utf-8'))
        td={t['id']:t for t in plan['tasks']};sd={s['id']:s for s in plan['stories']}
        def write(rel,content):(root/rel).write_text(content+'\n',encoding='utf-8')
        for t in td.values():write(f'tasks/{t["id"]}.md',task_markdown(t))
        for s in sd.values():
            content=f'# {s["id"]} — {s["title"]}\n\nWave: **{s["sprint"]}** · Epic: {s["epic"]}\n\n## Outcome\n{s["outcome"]}\n\n## Acceptance\n'+'\n'.join('- '+x for x in s['acceptance'])+'\n\n## Dependencies\n'+(', '.join(s['dependencies']) or 'Không có.')+'\n\n## Tasks\n'+md_table(['ID','Agent mode','Outcome','Card'],[[t,td[t]['mode'],td[t]['title'],f'[Mở task](../tasks/{t}.md)'] for t in s['tasks']])+'\n\n## Done\n'+s['definition_of_done']
            write(f'stories/{s["id"]}.md',content)
        for s in plan['sprints']:
            content=f'# {s["id"]} — {s["title"]}\n\n**Execution wave, không có ETA mặc định.**\n\n## Goal\n{s["goal"]}\n\n## Gate\n{s["gate"] or "Theo dependency và definition of done của story."}\n\n## Story → Task\n'
            for sid in s['stories']:
                st=sd[sid];content+=f'\n### {sid} — {st["title"]}\n{st["outcome"]}\n\n'+md_table(['Task','Mode','Outcome','Card'],[[tid,td[tid]['mode'],td[tid]['title'],f'[Mở](../tasks/{tid}.md)'] for tid in st['tasks']])+'\n'
            content+='\n## Exit\nNghiệm thu các task theo evidence và gate; cập nhật handoff. Không dùng ngày hoặc phần trăm cảm tính để chuyển wave.\n'
            write(f'sprints/{s["id"]}.md',content)
        full='# Backlog toàn bộ — Agent Execution v3\n\nBản tra cứu sinh từ plan/backlog.json. Không nạp tất cả vào context. Đọc task được chọn và read_before. Status thực ở state/task_state.json.\n\n'
        for s in plan['sprints']:
            full+=f'\n# WAVE {s["id"]} — {s["title"]}\n\n{s["goal"]}\n'
            for sid in s['stories']:
                st=sd[sid];full+=f'\n## STORY {sid} — {st["title"]}\n\n{st["outcome"]}\n'
                for tid in st['tasks']:full+='\n---\n\n'+task_markdown(td[tid])
        write('02_SPRINT_STORY_TASK_BACKLOG.md',full)
        def csvout(rel,fields,rows):
            with (root/rel).open('w',encoding='utf-8-sig',newline='') as f:
                wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(rows)
        fields=['id','sprint','story','mode','title','status','complexity','depends_on_tasks','outputs','required_verification','evidence_path','review_path','approval_required']
        rows=[]
        for t in plan['tasks']:
            row={k:t.get(k,'') for k in fields};row['status']=state['tasks'][t['id']]['status']
            rows.append({k:' | '.join(v) if isinstance(v,list) else v for k,v in row.items()})
        csvout('data/tasks.csv',fields,rows)
        csvout('data/stories.csv',['id','sprint','title','task_count','done_count'],[{'id':s['id'],'sprint':s['sprint'],'title':s['title'],'task_count':len(s['tasks']),'done_count':sum(state['tasks'][tid]['status']=='DONE' for tid in s['tasks'])} for s in plan['stories']])
        csvout('data/sprints.csv',['id','title','phase','gate','task_count','done_count'],[{'id':s['id'],'title':s['title'],'phase':s['phase'],'gate':s['gate'],'task_count':len(s['tasks']),'done_count':sum(state['tasks'][tid]['status']=='DONE' for tid in s['tasks'])} for s in plan['sprints']])
        records=[]
        paths=[x for x in sorted(root.glob('*.md')) if x.name!='02_SPRINT_STORY_TASK_BACKLOG.md']
        paths+=[*sorted((root/'specs/chapters').glob('*.md')),*sorted((root/'specs/puzzles').glob('*.md')),*sorted((root/'sprints').glob('*.md')),*sorted((root/'stories').glob('*.md')),*sorted((root/'tasks').glob('*.md'))]
        for f in paths:
            rel=f.relative_to(root).as_posix();text=f.read_text(encoding='utf-8');typ={'tasks':'task','stories':'story','sprints':'wave'}.get(rel.split('/')[0],'doc')
            if rel.startswith('specs/chapters'):typ='chapter'
            if rel.startswith('specs/puzzles'):typ='puzzle'
            tid=f.stem;task=td.get(tid,{})
            wave=task.get('sprint',sd.get(tid,{}).get('sprint',tid if typ=='wave' else ''))
            records.append({'id':rel,'title':text.splitlines()[0].lstrip('# '),'type':typ,'wave':wave,'mode':task.get('mode',''),'status':state['tasks'].get(tid,{}).get('status',''),'search':text.lower(),'html':markdown(text)})
        payload=json.dumps({'records':records,'revision':state['revision'],'tasks':len(td),'stories':len(sd),'waves':len(plan['sprints']),'done':sum(t['status']=='DONE' for t in state['tasks'].values())},ensure_ascii=False).replace('</',r'<\/')
        page=HTML_TEMPLATE.replace('__PAYLOAD__',payload)
        write('THE_SEVENTH_HOUSE_AGENT_HANDBOOK.html',page)
        print(json.dumps({'result':'PASS','records':len(records),'task_cards':len(td),'state_revision':state['revision'],'rewritten':['Markdown views','CSV snapshots','offline HTML'],'unchanged':['canonical plan','canonical state','XLSX snapshot'],'scope':'DOCUMENT_VIEWS_ONLY'},ensure_ascii=False,indent=2));return 0
    except (OSError,KeyError,ValueError,TypeError) as e:print(f'View generation failed: {e}',file=sys.stderr);return 1

HTML_TEMPLATE=r'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ngôi Nhà Thứ Bảy — Agent Execution v3</title>
<style>
:root{--bg:#eef3f5;--ink:#19303e;--muted:#627783;--line:#dae4e9;--teal:#146d78;--dark:#142b38}*{box-sizing:border-box}body{margin:0;background:var(--bg);font:15px/1.65 system-ui,-apple-system,Segoe UI,Arial,sans-serif;color:var(--ink)}header{padding:30px 36px 26px;background:var(--dark);color:white;display:flex;justify-content:space-between;gap:30px}header small{letter-spacing:.2em;text-transform:uppercase;color:#9cd2d8}h1{font-size:27px;line-height:1.3;margin:8px 0 6px}header p{margin:0;color:#c9d9df;font-size:13px}.metrics{display:flex;gap:26px;align-items:center}.metrics strong{font-size:27px;display:block;color:#c1e8df}.metrics span{font-size:11px;text-transform:uppercase}.shell{display:grid;grid-template-columns:340px minmax(0,1fr);max-width:1620px;margin:auto;min-height:80vh}aside{border-right:1px solid var(--line);padding:22px 18px;position:sticky;top:0;max-height:100vh;overflow-y:auto}main{padding:25px 38px 70px;min-width:0}.filters{display:grid;gap:8px}.filters input,.filters select{font:inherit;font-size:13px;width:100%;border:1px solid #cbd9df;border-radius:7px;padding:9px;background:white;color:var(--ink)}.filterrow{display:grid;grid-template-columns:1fr 1fr;gap:8px}#count{font-size:12px;color:var(--muted);margin:14px 0 8px}#nav{display:grid;gap:5px}.navitem{text-align:left;border:1px solid transparent;background:transparent;padding:10px 11px;border-radius:7px;font:inherit;font-size:12px;line-height:1.45;color:var(--ink);cursor:pointer}.navitem:hover{background:white;border-color:var(--line)}.navitem.active{background:var(--teal);color:white}.navitem small{display:block;opacity:.7;font-size:10px;margin-bottom:3px}.notice{background:#fff4dc;border:1px solid #ecdab8;border-radius:9px;padding:12px 16px;font-size:12px;margin-bottom:19px}.toolbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px;color:var(--muted);font-size:12px}.toolbar a,.toolbar button{border:1px solid var(--line);border-radius:6px;padding:5px 10px;background:white;color:var(--ink);text-decoration:none;cursor:pointer;font:inherit}article{background:white;border:1px solid var(--line);border-radius:11px;padding:30px 36px;max-width:1100px;box-shadow:0 4px 18px #162d3c04}article h1{font-size:26px;border-bottom:2px solid var(--teal);padding-bottom:18px;margin:0 0 20px}article h2{font-size:19px;line-height:1.45;margin:31px 0 10px;color:var(--teal)}article h3{font-size:16px;margin-top:26px}article p{margin:10px 0}article li{margin:6px 0}article pre{background:#142b38;color:#d9edf3;padding:17px 20px;border-radius:8px;overflow:auto;font-size:12px;line-height:1.6}article code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.85em;overflow-wrap:anywhere;background:#edf3f5;border-radius:3px;padding:2px 4px}article pre code{background:transparent;padding:0;font-size:inherit}article a{color:var(--teal)}article blockquote{border-left:3px solid var(--teal);margin:15px 0;padding:10px 18px;background:#f1f8f7}article hr{border:0;border-top:1px solid var(--line);margin:28px 0}.tablewrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:12px;line-height:1.55;margin:12px 0}th{text-align:left;background:#e8f2f3;color:#17505a}th,td{padding:11px 12px;border:1px solid var(--line);vertical-align:top}tbody tr:nth-child(even){background:#f8fafb}footer{font-size:11px;color:var(--muted);margin-top:18px}.empty{padding:25px;color:var(--muted)}@media(max-width:900px){header{padding:24px;display:block}.metrics{margin-top:20px;gap:30px}.shell{grid-template-columns:1fr}aside{position:static;max-height:330px;border-right:0;border-bottom:1px solid var(--line)}main{padding:20px 14px}article{padding:23px 19px}article h1{font-size:23px}}@media print{header,aside,.toolbar,.notice,footer{display:none}.shell{display:block}main{padding:0}article{box-shadow:none;border:0;padding:0}}
</style></head><body><header><div><small>Agent execution handbook / v3</small><h1>NGÔI NHÀ THỨ BẢY</h1><p>Thực thi toàn bộ game · context nhỏ · dependency rõ · nghiệm thu bằng evidence</p></div><div class="metrics"><div><strong id="mwave"></strong><span>waves</span></div><div><strong id="mstory"></strong><span>stories</span></div><div><strong id="mtask"></strong><span>task cards</span></div><div><strong id="mdone"></strong><span>done</span></div></div></header><div class="shell"><aside><div class="filters"><input id="search" type="search" placeholder="Tìm T-030201, world switch, ending…" aria-label="Tìm nội dung"><div class="filterrow"><select id="type" aria-label="Loại tài liệu"><option value="doc">Tài liệu chính</option><option value="task">Task cards</option><option value="story">Stories</option><option value="wave">Waves / sprints</option><option value="chapter">Chương truyện</option><option value="puzzle">Puzzles</option><option value="all">Toàn bộ</option></select><select id="wave" aria-label="Wave"><option value="">Tất cả wave</option></select></div><select id="mode" aria-label="Agent mode"><option value="">Tất cả agent mode</option></select></div><div id="count"></div><nav id="nav"></nav></aside><main><div class="notice"><strong>Đây là gói hướng dẫn và công cụ quản lý, chưa phải game.</strong> Snapshot revision <span id="revision"></span>. Canonical: plan/backlog.json + state/task_state.json. Dùng tools/render_views.py để làm mới bản xem; không sửa trạng thái trong HTML/Excel.</div><div class="toolbar"><span id="filepath"></span><a id="rawlink" href="START_HERE.md">Mở Markdown</a><button id="print">In tài liệu đang xem</button></div><article id="article"></article><footer>Offline, không CDN, không upload hoặc gọi API. Từng task giữ liên kết về read-before, outputs, kiểm thử và handoff.</footer></main></div><script id="payload" type="application/json">__PAYLOAD__</script><script>
'use strict';const data=JSON.parse(document.getElementById('payload').textContent),records=data.records,$=id=>document.getElementById(id);let selected='START_HERE.md';['wave','story','task','done'].forEach((x,i)=>$('m'+x).textContent=[data.waves,data.stories,data.tasks,data.done][i]);$('revision').textContent=data.revision;
for(let i=1;i<=data.waves;i++){let s='S'+String(i).padStart(2,'0');$('wave').add(new Option(s,s))}Array.from(new Set(records.map(r=>r.mode).filter(Boolean))).sort().forEach(m=>$('mode').add(new Option(m,m)));
function show(id){const rec=records.find(r=>r.id===id);if(!rec)return;selected=id;$('article').innerHTML=rec.html;$('filepath').textContent=rec.id;$('rawlink').href=rec.id;document.querySelectorAll('.navitem').forEach(x=>x.classList.toggle('active',x.dataset.id===id));history.replaceState(null,'','#'+encodeURIComponent(id));}
function filter(){const q=$('search').value.toLocaleLowerCase().trim(),type=$('type').value,w=$('wave').value,m=$('mode').value;const found=records.filter(r=>(type==='all'||r.type===type)&&(!q||r.search.includes(q))&&(!w||r.wave===w)&&(!m||r.mode===m));$('count').textContent=found.length+' tài liệu phù hợp';$('nav').replaceChildren();for(const r of found){const b=document.createElement('button');b.className='navitem'+(r.id===selected?' active':'');b.dataset.id=r.id;const s=document.createElement('small');s.textContent=[r.type.toUpperCase(),r.wave,r.mode,r.status].filter(Boolean).join(' · ');b.appendChild(s);b.appendChild(document.createTextNode(r.title));b.onclick=()=>show(r.id);$('nav').appendChild(b)}}
$('search').oninput=()=>{if($('search').value.trim())$('type').value='all';filter()};['type','wave','mode'].forEach(id=>$(id).onchange=filter);$('print').onclick=()=>window.print();$('article').onclick=e=>{let a=e.target.closest('a');if(!a)return;let href=a.getAttribute('href');if(!href||/^[a-z]+:/i.test(href)||href.startsWith('#'))return;let base=selected.split('/');base.pop();for(let part of href.split('/')){if(part==='..')base.pop();else if(part&&part!=='.')base.push(part)}let path=base.join('/');if(records.some(r=>r.id===path)){e.preventDefault();show(path)}};try{let id=decodeURIComponent(location.hash.slice(1));if(records.some(r=>r.id===id))selected=id}catch{}filter();show(selected);
</script></body></html>'''
if __name__=='__main__':sys.exit(main())
