// Uses bundled runtime only. Run from repo root after render_views.py.
import fs from 'node:fs/promises';
process.on('uncaughtException',e=>{console.error(e.message);process.exit(1);});
import {pathToFileURL} from 'node:url';
const modulePath=process.argv[2];
if(!modulePath)throw Error('Pass the bundled @oai/artifact-tool module path from load_workspace_dependencies.');
const {FileBlob,SpreadsheetFile}=await import(pathToFileURL(modulePath).href);
const read=async p=>JSON.parse(await fs.readFile(p,'utf8'));
const plan=await read('plan/backlog.json'),state=await read('state/task_state.json'),chapters=await read('specs/chapter_catalog.json');
const version=plan.meta.version;
const reportDir=`reports/design/v${version.replace('.','')}`;
await fs.mkdir(reportDir,{recursive:true});
const w=await SpreadsheetFile.importXlsx(await FileBlob.load('THE_SEVENTH_HOUSE_AGENT_TRACKER.xlsx'));
const task=w.worksheets.getItem('Tasks'),last=plan.tasks.length+4;
const rows=plan.tasks.map(t=>[t.id,t.sprint,t.story,t.mode,t.title,state.tasks[t.id].status,t.depends_on_tasks.join(', '),t.outputs.join('; '),t.required_verification.join(', '),t.complexity,t.evidence_path,`tasks/${t.id}.md`,t.approval_required]);
const taskTable=task.tables.items[0];
const existingTaskRows=taskTable.getDataRows().length;
if(existingTaskRows<rows.length){
 const spill=task.getRange(`A${existingTaskRows+5}:M${last}`);
 const existing=spill.values;
 if(existing.some((r,i)=>r[0]!=null && r[0]!==rows[existingTaskRows+i][0]))throw Error('Unexpected data below task table; preserve it before refresh.');
 spill.clear({applyTo:'contents'});
 taskTable.rows.add(null,rows.slice(existingTaskRows));
}
for(let r=597;r<=last;r++)task.getRange(`A${r}:M${r}`).copyFrom(task.getRange('A596:M596'),'all');
task.getRange(`A5:M${last}`).values=rows;
task.getRange('A1').values=[[`TASK LEDGER / ${plan.tasks.length} executable contracts`]];
task.getRange('A2').values=[[`Snapshot revision ${state.revision}; gameplay ${version}; source: plan/backlog.json + state/task_state.json.`]];
const dash=w.worksheets.getItem('Dashboard');
dash.getRange('A1').values=[[`NGÔI NHÀ THỨ BẢY\nAGENT EXECUTION / ${version}`]];
dash.getRange('A3').values=[[`36 execution waves; canonical state revision ${state.revision}; task states preserved during design migration.`]];
dash.getRange('A6').formulas=[[`=COUNTA(Tasks!A5:A${last})`]];
dash.getRange('C6').formulas=[[`=COUNTIF(Tasks!F5:F${last},"DONE")`]];
dash.getRange('E6').formulas=[[`=COUNTIF(Tasks!F5:F${last},"BLOCKED*")`]];
dash.getRange('A9').values=[[`PROJECT STATE: IN_PROGRESS; gameplay ${version} is a design baseline, campaign puzzles not implemented.`]];
dash.getRange('E13').values=[['28 puzzles: 14 CORE + 7 SUPPORT + 7 SECRET']];
dash.getRange('A22').values=[[`SOURCE OF TRUTH\nplan/backlog.json + state/task_state.json; snapshot revision ${state.revision}. Design validation is not game QA.`]];
w.worksheets.getItem('Guide').getRange('A2').values=[[`Snapshot revision ${state.revision}; gameplay ${version}, ADR-002 + ADR-003; workbook is a read view, not an independent ledger.`]];
const waves=w.worksheets.getItem('Waves');
for(let i=0;i<plan.sprints.length;i++){
 const s=plan.sprints[i],r=i+5;
 waves.getRange(`A${r}:E${r}`).values=[[s.id,s.phase,s.title,s.goal,s.tasks.length]];
 waves.getRange(`F${r}`).formulas=[[`=COUNTIFS(Tasks!B$5:B$${last},A${r},Tasks!F$5:F$${last},"DONE")`]];
 waves.getRange(`G${r}`).formulas=[[`=IFERROR(F${r}/E${r},0)`]];
 waves.getRange(`H${r}`).values=[[s.gate]];
}
const stories=w.worksheets.getItem('Stories');
for(let i=0;i<plan.stories.length;i++){
 const s=plan.stories[i],r=i+5;
 stories.getRange(`A${r}:F${r}`).values=[[s.id,s.sprint,s.title,s.outcome,s.dependencies.join(', '),s.tasks.length]];
 stories.getRange(`G${r}`).formulas=[[`=COUNTIFS(Tasks!C$5:C$${last},A${r},Tasks!F$5:F$${last},"DONE")`]];
 stories.getRange(`H${r}`).formulas=[[`=IFERROR(G${r}/F${r},0)`]];
}
const gates=w.worksheets.getItem('Gates');
gates.getRange('A5:G14').values=plan.gates.map(g=>[g.id,g.sprint,g.title,g.criteria,g.reviewer,g.external_owner_required?'YES':'NO',state.gates[g.id].status]);
const req=w.worksheets.getItem('Requirements');
req.getRange('A5:F22').values=plan.requirements.map(r=>[r.id,r.title,r.acceptance,r.gates,r.stories.join(', '),r.status]);
const qa=await read('plan/qa_matrix.json');
const qaSheet=w.worksheets.getItem('QA'),qaRows=qa.map(c=>[c.id,c.area,c.scenario,c.expected,c.mode,c.first_sprint,c.gate,c.status]);
const qaTable=qaSheet.tables.items[0],existingQaRows=qaTable.getDataRows().length;
if(existingQaRows<qaRows.length){
 const spill=qaSheet.getRange(`A${existingQaRows+5}:H${qa.length+4}`);
 if(spill.values.some((r,i)=>r[0]!=null && r[0]!==qaRows[existingQaRows+i][0]))throw Error('Unexpected data below QA table.');
 spill.clear({applyTo:'contents'});
 qaTable.rows.add(null,qaRows.slice(existingQaRows));
}
qaSheet.getRange(`A5:H${qa.length+4}`).values=qaRows;
const content=w.worksheets.getItem('Content');
content.getRange('A2').values=[['7 chapters; 28 puzzles (21 required, 7 secret); 7 memories; 28 journal records; 3 endings.']];
content.getRange('A5:J11').values=chapters.map(c=>[c.id,c.house_id,c.title,c.zone,`${c.all_puzzles[0]}–${c.all_puzzles[3]} (3 main + 1 secret)`,c.memory_id,c.essential_evidence.join(', '),c.greybox_sprint,c.id==='CH01'?'S10 / audit S25':c.complete_sprint,c.exit_condition]);
content.getRange('E4:E11').format.columnWidth=32;
content.getRange('D5:E11').format.wrapText=true;
content.getRange('I5:J11').format.wrapText=true;
// Existing row heights remain intentional; fit only affected content rows.
content.getRange('A5:J11').format.rowHeight=60;
w.recalculate();
const report=await w.inspect({kind:'table',range:'Dashboard!A5:G6',include:'values,formulas',maxChars:1600,tableMaxRows:2,tableMaxCols:7});
console.log(report.ndjson);
const actual=dash.getRange('A6:G6').values[0];
if(actual[0]!==plan.tasks.length || actual[2]!==Object.values(state.tasks).filter(t=>t.status==='DONE').length)throw Error('Dashboard count mismatch');
const errors=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:25},maxChars:1500});
await fs.writeFile(`${reportDir}/workbook_formula_scan.json`,JSON.stringify(errors,null,2));
const preview=await w.render({sheetName:'Content',range:'A4:G11',scale:1,format:'png'});
await fs.writeFile(`${reportDir}/workbook_after.png`,new Uint8Array(await preview.arrayBuffer()));
const output=await SpreadsheetFile.exportXlsx(w);
await output.save('THE_SEVENTH_HOUSE_AGENT_TRACKER.xlsx');
await fs.writeFile(`${reportDir}/workbook_update.json`,JSON.stringify({result:'EXPORTED',revision:state.revision,tasks:plan.tasks.length,done:actual[2],puzzles:28,tool:'@oai/artifact-tool',native_excel:'NOT_TESTED'},null,2));
console.log('Exported updated tracker with preserved sheets and formula-driven counts.');
