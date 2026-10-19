"""Render design cards from canonical catalogs. Never modifies runtime or task state."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / 'specs' / name).read_text(encoding='utf-8'))


def render(root=ROOT):
    global ROOT
    ROOT = Path(root)
    puzzles = read('puzzle_catalog.json')
    chapters = read('chapter_catalog.json')
    for p in puzzles:
        pid = p['id']
        clues = '\n'.join(f"- `{c['id']}` tại `{c['location']}`: {c['observation']}" for c in p['clues'])
        actions = '\n'.join(f'{i+1}. `{action}`' for i, action in enumerate(p['actions']))
        hints = '\n'.join(f'| {i+1} | {hint} |' for i, hint in enumerate(p['hints']))
        rewards = ', '.join(f'`{r}`' for r in p['rewards']) or 'Không thêm journal record; mở khả năng/đường đi theo trạng thái.'
        d=p['reasoning']
        hypotheses='\n'.join(f"- **{'Kết luận được hỗ trợ' if h['accepted'] else 'Giả thuyết cần loại'}:** {h['statement']} Nguồn: {', '.join(h.get('supported_by',h.get('refuted_by',[])))}." for h in d['hypotheses'])
        thought_path='\n'.join(f"{i+1}. {s['deduction']} → {' → '.join('`'+a+'`' for a in s['canonical_actions'])} → {s['feedback']} (quan sát: {', '.join(s['observations'])})." for i,s in enumerate(d['thought_path']))
        inquiry_routes='\n'.join(f"- `{r['id']}`: {r['lead']} Đầu mối bắt đầu: {', '.join(r['entry_clues'])}. Nguồn khi tiếp tục khảo sát: {', '.join(r['clues'])}." for r in d['observation_routes'])
        depth_section=f'''## Câu hỏi, giả thuyết và đường suy luận 3.2

**Câu hỏi:** {d['question']}

{hypotheses}

{thought_path}

Hai hướng điều tra có đầu mối cụ thể; có thể hội tụ tại nguồn chung:

{inquiry_routes}

Các giả thuyết ở đây là hướng authoring, không bắt thêm một menu đáp án ở mọi puzzle. Commit mode: `{d['commit_mode']}`. Clue quan sát theo thứ tự nào cũng được khi tiếp cận vật lý hợp lệ. Có đủ chứng cứ cần thiết và một đáp án đúng thì chấp nhận, không bắt click đủ từng clue-ID. UI không tự điền kết luận.

Phản hồi sai cụ thể: {d['feedback']['wrong']}
Phản hồi tiến triển: {d['feedback']['progress']}

## Tri thức tái sử dụng và kết quả có ý nghĩa

Luật vận dụng: {', '.join(d['uses_knowledge']) or 'onboarding/công cụ thông thường'}. Luật được dạy: {', '.join(d['teaches_knowledge']) or 'củng cố luật đã biết'}. Các K-ID là trace authoring, không là currency hoặc một read-gate mới. Tham chiếu `specs/gameplay_reasoning.json`.

Kết quả tức thời: {d['payoff']['immediate']}
Được dùng lại tại: {', '.join(d['payoff']['callbacks']) or 'resolution/epilogue'}. Callback chỉ phát sau quan sát và chapter guard, không tự spoil luật/chuyện ở chương sau. Nguồn nghiên cứu: {', '.join(d['research_refs'])}, chi tiết ở nghiên cứu comparative_gameplay_research_v32.

## Quyết định dưới áp lực

Mode `{d['tension']['mode']}`. Cue: {d['tension']['cue']}
Lựa chọn của người chơi: {d['tension']['player_decision']}
Không tăng nguy cơ khi đọc. Trigger theo state/action commit, một lần; Warn/Chase không cho mở closeup mới. Phải kiểm cơ hội thực hiện lựa chọn bằng runtime, không chỉ nhìn sơ đồ.
'''
        text = f'''# {pid} — {p['title']}

**Baseline:** 3.2 · **Chapter:** {p['chapter']} · **Role:** {p['role']} · **Main-required:** {str(p['required_for_main']).lower()} · **Status:** DESIGN_ONLY.
Sinh từ `specs/puzzle_catalog.json` bằng `python tools/render_puzzle_cards.py`. Không sửa card để thay đáp án mà bỏ catalog. Đọc `14_PUZZLE_DESIGN_BIBLE.md` và ADR-002 + ADR-003 trước triển khai.

## Scene, entry và địa điểm tương tác

{p['scene']}

Entry: chapter đã mở theo chapter catalog; prerequisite puzzles: {', '.join(p['depends_on']) or 'không có puzzle trước trong chương'}. Liên kết thông tin, không phải khóa: {', '.join(p.get('information_inputs',[])) or 'xem thought_path và knowledge matrix'}. Không dùng memory/lore tùy chọn khóa main. Props/clues được inspect sớm nếu layout cho phép; các dependency là điều kiện thao tác/tiến triển, không khóa đọc ghi chú vô cớ.

## Quan sát và điều phải suy ra

{clues}

**Suy luận:** {p['inference']}

Journal cho ghim đúng thông tin đã thấy, không auto-fill lời giải. Đáp án được chấp nhận nếu hợp lệ; không yêu cầu inspect một tờ giấy như khóa vô hình, trừ evidence/physical item cần để chứng minh hoặc thao tác. Các locators là stable scene/prop IDs cần tạo trong runtime, không phải file đã tồn tại.

## Các tương tác khả dụng

{actions}

Đây là danh mục action để triển khai; thought_path bên dưới minh họa trình tự hợp lệ. Hai vị trí mồi P04 là lựa chọn thay thế, không bắt dùng cả hai. Không bắt mọi hành động độc lập theo một thứ tự duy nhất. Dùng `apply_action` qua resolver/inspection view; UI không đặt solved trực tiếp. Drag/rotate/flip có nút keyboard/pad tương đương; range/LOS/phase vẫn áp dụng.

{depth_section}

## Đáp án và tiêu chí thành công

```json
{json.dumps(p['solution'],ensure_ascii=False,indent=2)}
```

Success phải kiểm toàn bộ trường liên quan, không chỉ đủ item/count hoặc action cuối. P23 cần link+relation; P27 cần topology/orientation/group joins; P28 là lựa chọn có hậu quả, không coi A/B là đáp án sai. P27 không set evacuation_route_validated. Với P28, SOLVED/resolution chỉ sau playable ending và credits reachable; panel entry không cần P28 solved.

## Vật phẩm và phần thưởng

```json
{json.dumps(p['items'],ensure_ascii=False,indent=2)}
```

Recipe và nguồn vật phẩm theo `specs/item_catalog.json`; vật cần nhặt trong scene không được auto-grant từ trường inputs. Reward: {rewards}
Reward source duy nhất, commit một lần. P23 E12 là ảnh thu ở entry trước confirm; không circular self-reward. M07 từ P25, không từ P27. L01–L07 có inspect riêng trong chapter, không cần grant chỉ vì puzzle solved.

## Sai, feedback và phục hồi

{p['negative_case']}

Wrong input trả feedback về loại bất nhất, giữ IN_PROGRESS; không mất clue/items đã commit, không reset chapter. Recipe wrong-use không consume. Reset local rõ phạm vi; không xóa record. Essential item có recovery hoặc inventory retained; không ép replay cả chương.

## State và save/load

`LOCKED → AVAILABLE → IN_PROGRESS → SOLVED`. Snapshot chung: state, inspected_ids, reward_committed, presentation_once_ids. Trường riêng: {', '.join('`'+f+'`' for f in p['persistent_fields'])}.
Save qua StateRegistry/SaveService, serialized IDs/value types; không NodePath/RID/instance refs. Save trong transaction deferred; reload trước/sau mỗi bước giữ kết quả và reward đúng một lần. Cancel/close không silently reset. Controller không sửa WorldController/schema riêng.

## Hints tự nguyện

| Cấp | VI authoring text |
| --- | --- |
{hints}

H/menu mở ngay theo yêu cầu, không quảng cáo/chờ; cấp1 chỉ hướng quan sát, cấp2 quan hệ, cấp3 walkthrough. EN localization keys đích `puzzle.{pid}.hint.1..3`; dịch đủ nghĩa trong task authoring/LQA, các key này chưa phải runtime translations đã có.

## Kinh dị và accessibility

{p['horror']}

Event một lần theo persistent presentation ID, skip/close/focus cleanup. Không xóa evidence neo. Closeup an toàn không capture; Warn/Chase chặn mở closeup mới. Text/caption/icon thay cue chỉ màu/cao độ/flash; 150% text không che targets.

## Ca nghiệm thu phải triển khai

- **{pid}-HAPPY:** từ entry hợp lệ, thao tác qua implementation tới success; assert đáp án/state/reward/exit đúng và reward exactly once.
- **{pid}-WRONG:** {'thử RETURN sớm, lặp nhóm hoặc chọn tuyến đã ngập trong C trial; A/B là lựa chọn hợp lệ, không thuộc ca sai' if pid=='P28' else 'dùng cấu hình không thỏa điều kiện trong solution'}; assert không solve sai, feedback có lý do, sửa được mà không mất vật/chứng cứ.
- **{pid}-ORDER:** inspect/thu clues theo thứ tự khác; lời giải hợp lệ vẫn được chấp nhận, trừ dependency vật lý/evidence rõ trong card.
- **{pid}-LOAD:** snapshot/restore trước và sau từng action, mở lại closeup; tentative slots/angles/recipes và once flags nhất quán.
- **{pid}-EXPLOIT:** kiểm nguyên văn negative case phía trên, spam/reentrant và use sai target/phase/range; không debug-grant reward.
- **{pid}-ACCESS:** keyboard-only, synthetic pad, mouse, mute, reduced effects, VI/EN, text150%; physical pad ghi riêng.
- **{pid}-REVISIT:** giải xong, rời/load/revisit; không duplicate, không reset required puzzle khác; SECRET thiếu không chặn A/B.
- **{pid}-REASON:** tái hiện thought_path, thử giả thuyết sai với phản chứng thực; không chỉ assert solved khi nhập golden answer.
- **{pid}-ROUTES:** cả hai observation_routes và mọi alternate solution được nêu phải đi tới được qua input/scene thật; không ép cùng thứ tự inspect.
- **{pid}-FEEDBACK:** sai trả đúng loại mâu thuẫn, không per-slot oracle hoặc auto-fill; clue pins chỉ chứa nguồn đã thấy.
- **{pid}-TENSION:** cue/commit/aftermath, retry và pause/focus đúng; không advance khi đọc, không xóa clue hoặc duplicate scare.

Runtime outputs phải tạo: `data/puzzles/{pid}.json`, controller/adapter trong `scripts/puzzles/`, fixtures `tests/fixtures/puzzles/{pid}/`, logs/captures đúng build. Card tồn tại hoặc static validator pass không xác nhận các ca này đã chạy.
'''
        (ROOT / f'specs/puzzles/{pid}.md').write_text(text, encoding='utf-8')
    for c in chapters:
        ps = [p for p in puzzles if p['chapter'] == c['id']]
        rows = '\n'.join(f"| {p['id']} | {p['role']} | {p['title']} | {', '.join(p['depends_on']) or 'chapter entry'} |" for p in ps)
        text = f'''# {c['id']} / {c['house_id']} — {c['title']}

Baseline3.2, sinh từ chapter/puzzle catalogs; DESIGN_ONLY cho nội dung mới. Nhà: {c['house_name']}. Không gian: {c['zone']}.
Mục tiêu pacing: {c['pacing_target_minutes']} phút, chưa playtest; không dùng delay hoặc backtracking rỗng ép thời lượng.

## Entry, exit và reveal

Entry: `{c['entry_condition']}`. Exit: `{c['exit_condition']}`.
Main-required: {', '.join(c['required_puzzles'])}. SECRET: {', '.join(c['secret_puzzles'])}, không khóa main/A/B. Essential records: {', '.join(c['essential_evidence'])}; memory {c['memory_id']}; lore {c['lore_id']} qua inspect riêng, không thêm ID.
Reveal: **{c['reveal']}**. Áp dụng Story Bible và ADR-002: không tiết lộ An/quan hệ trước CH06; CH05 vào record H05 sau lần thu hồi thứ 5; flashback và cơ thể sau returntime tách biệt.

## Puzzle graph và nhịp chương

Câu hỏi của chương: **{c['investigation_question']}**
Điểm gắn bó với nhân vật: {c['bonding_beat']}

```json
{json.dumps(c['investigation_graph'],ensure_ascii=False,indent=2)}
```

Tension policy: {c['tension_policy']}

| ID | Vai trò | Trải nghiệm | Phụ thuộc puzzle |
| --- | --- | --- | --- |
{rows}

Đọc từng card trước authoring. Một cuộc gặp/quan sát đời thường tạo mục tiêu cụ thể, sau đó cho tự chọn thứ tự clues khi không có dependency vật lý. Kết quả một puzzle mở thông tin/vật/đường hữu ích cho puzzle sau. Journal ghim để không bắt đi lại chép biểu tượng. Sự kiện kinh dị theo trigger trong card, không tự chèn chase vàoCH02/CH03/CH05 hoặc jumpscare sau mọi vật.

## Memory và revisit

{c['memory_id']} có source trong evidence catalog; M01..M06 từSECRET, M07 từP25main. Mỗi memory nối đúng một cạnh trong evacuation_route.json. Sau main exit vẫn revisit được tới trước final confirmation; không respawn enemy unsafe hoặc reset các puzzle đã solve. P27 là plan, P28 mới kiểm chứng3nhóm.

## Checkpoints và outputs

Entry `{c['id']}_ENTRY` ở REAL/Shared support; trước encounter/reveal/exit có checkpoint tương ứng. CH07 có PRE_CHOICE, PRE_EVACUATION và checkpoint trước mỗi quyết định nhóm. Capture giữ clue; closeup/journal/pause không tăng nước.

Phải tạo `scenes/levels/{c['id']}/{c['id'].lower()}.tscn`, `data/chapters/{c['id']}.json`, `data/dialogue/{c['id']}.json`, bốn puzzle runtime files, camera/checkpoint resources, item/clue/recipe registries, asset/audio manifests, VI/EN. Reuse WorldController/SaveService, không clone controller theo chương.

## Nghiệm thu

Entry→main exit không debug grants và không cần SECRET; cả bốn puzzle happy/wrong/load/order/exploit/access/revisit. Thu memory trước/sau main nếu hợp lệ; skip/focus/closeup locks; mute/reduced effects/150%VIEN; rendered art/camera/audio riêng. Full chapter phải có assets/cues/animation final, không chỉ logic headless.

Production wave ban đầu: greybox {c['greybox_sprint']}, final {c['complete_sprint']}. Ngoại lệ ADR-002: CH01 cả P01–P04 phải qua G2 ở S10; S25 chỉ audit/polish, không trì hoãn puzzle. CH02–CH07 không bắt đầu production khi G2/G3 chưa đạt. Thiếu người chơi thật ghi HUMAN_USABILITY_NOT_ASSESSED, không tự gọi bot là người chơi.
'''
        (ROOT / f"specs/chapters/{c['id']}.md").write_text(text, encoding='utf-8')
    lines=['# Ma trận làm sâu 28 puzzle / gameplay 3.2','','Sinh từ puzzle_catalog.json. Đây là thay đổi thiết kế, không là bằng chứng đã implement hoặc playtest.','','| Puzzle | Điều thay đổi | Câu hỏi của người chơi | Luật vận dụng / dạy | Payoff |','| --- | --- | --- | --- | --- |']
    for p in puzzles:
        d=p['reasoning']
        values=[p['id']+' — '+p['title'],d['design_delta'],d['question'],', '.join(d['uses_knowledge'])+' / '+', '.join(d['teaches_knowledge']),d['payoff']['immediate']]
        lines.append('| '+' | '.join(v.replace('|','/').replace('\n',' ') for v in values)+' |')
    lines+=['','Đọc card trong specs/puzzles/ cho nguồn, giả thuyết, phép thử, phản hồi, routes và testcases. Nghiên cứu tham chiếu: [nguồn và giới hạn](comparative_gameplay_research_v32.md).','']
    (ROOT/'docs/design/puzzle_depth_matrix_v32.md').write_text('\n'.join(lines),encoding='utf-8')
    return len(puzzles), len(chapters)


if __name__ == '__main__':
    print('Rendered puzzle/chapter design cards:', render())
