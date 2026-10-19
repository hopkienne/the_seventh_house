"""One-shot owner-requested design migration. No game implementation or task completion.

Catalogs remain the authoring authority after this migration; do not rerun to edit them.
Run from the repository root. Refuses an already migrated plan.
"""
import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def write(rel, value):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    plan = load('plan/backlog.json')
    if plan['meta']['version'] != '3.0':
        raise SystemExit('Only accepts v3.0; edit canonical catalogs directly after migration.')
    state = load('state/task_state.json')
    before_tasks = copy.deepcopy(state['tasks'])
    before_gates = copy.deepcopy(state['gates'])
    for name in ['puzzle_catalog', 'chapter_catalog']:
        write(f'specs/history/{name}_v3.json', load(f'specs/{name}.json'))
    source = Path(r'C:\Users\kienth\.codex\attachments\16b95f57-6f1a-4e77-b43c-1e1ae0e578fe\Pasted text.txt')
    raw = source.read_bytes()
    proposal_copy=ROOT/'docs/design/owner_proposal_28_puzzles.txt'
    proposal_copy.parent.mkdir(parents=True,exist_ok=True)
    proposal_copy.write_bytes(raw)
    mapping = dict(zip([f'P{i:02}' for i in range(1, 15)],
                       ['P02','P03','P05','P06','P10','P11','P14','P15','P17','P18','P22','P23','P27','P28']))

    def remap(value):
        if isinstance(value, str):
            value = re.sub(r'(?<![A-Za-z0-9])P(0[1-9]|1[0-4])(?![0-9])', lambda m: mapping[m[0]], value)
            return value.replace('14 puzzle', '28 puzzle').replace('14 câu đố', '28 câu đố')
        if isinstance(value, list): return [remap(v) for v in value]
        if isinstance(value, dict): return {k: remap(v) for k, v in value.items()}
        return value

    # Closed task definitions/evidence are historical; only future work is retargeted.
    plan['stories'] = remap(plan['stories'])
    plan['sprints'] = remap(plan['sprints'])
    for task in plan['tasks']:
        if state['tasks'][task['id']]['status'] == 'NOT_STARTED':
            task.update(remap(task))
    puzzles = []

    def add(n, title, role, deps, scene, clues, inference, actions, solution, items,
            rewards, negative, hints, horror, persistence):
        pid = f'P{n:02}'
        chapter = f'CH{(n-1)//4+1:02}'
        puzzles.append(dict(id=pid, chapter=chapter, title=title, role=role,
            required_for_main=role != 'SECRET', depends_on=deps, scene=scene,
            layout=scene, clues=[dict(id=f'{pid}_C{i+1}', location=c[0], observation=c[1]) for i,c in enumerate(clues)],
            inference=inference, actions=actions.split('|'), solution=solution,
            items=items, rewards=rewards, reward_evidence_id=next((r for r in rewards if r.startswith('E')), None),
            negative_case=negative, hints=hints, horror=horror, persistent_fields=persistence.split('|'),
            implementation_status='DESIGN_ONLY', difficulty=['TUTORIAL','EASY','MEDIUM','MEDIUM','MEDIUM','HARD','SYNTHESIS'][(n-1)//4]))

    add(1,'Chiếc đồng hồ ngừng chạy','SUPPORT',[],
        'CH01.mother_room.clock_cabinet; cửa hàng ông Nhân mở từ entry, không cần đèn. Đèn thiếu vòng kính nằm trên bàn mẹ.',
        [('CH01.mother_room.note','Ba tiếng chuông đánh dấu lúc đồng hồ ngoài cửa hàng dừng; không phải số 3 là giờ.'),('CH01.nhan_shop.clock','Mặt 12 giờ: kim dài ở phút 17, kim ngắn nhích qua 2; bản phóng to có vạch phút và mô tả chữ tương đương.')],
        'Phân biệt kim giờ/phút và đối chiếu hai vị trí; đồng hồ trong tủ không in sẵn 02:17.',
        'inspect_note|inspect_shop_clock|set_hour_2|set_minute_17|confirm|take_lens|fit_lens|take_lantern',
        {'hour':2,'minute':17,'dial':'12_HOUR'},
        {'inputs':[],'outputs':['LANTERN_LENS','LANTERN'],'recipes':['FIT_LENS']},[],
        '02:35, 03:17 và kim đảo không mở; lấy kính/lắp lại không nhân đôi đèn; không được cần ERASED để tìm kính.',
        ['Đồng hồ bên cửa hàng dừng cùng một tiếng chuông.','Kim dài chỉ phút, kim ngắn chỉ giờ; hãy lưu ảnh vào journal.','Chọn giờ 2, phút 17; lấy vòng kính rồi lắp vào đèn trên bàn mẹ.'],
        'SOLVED: một tiếng chuông từ đồng hồ không hoạt động; phát một lần, không khóa tay người chơi.',
        'hour|minute|lens_taken|lens_fitted|lantern_taken')
    add(2,'Hàng rào giữa hai thế giới','CORE',['P01'],
        'CH01.yard: x=0..24m,z=-1.5..1.5; rào REAL x=8; bệ A x=6/B x=10 Shared; chìa REAL x=11; cửa ERASED x=15; dấu xưởng x=18. Giếng phụ z=1 có hố ERASED; tuyến chính luôn có sàn.',
        [('CH01.yard.fence','Rào có ở REAL, mất ở ERASED; đèn cho preview hình học chưa commit.'),('CH01.yard.well','Nền cạnh giếng bị thủng ở ERASED; hai bệ gạch còn ở cả hai lớp.')],
        'Lập đường đổi lớp: vượt rào ở ERASED, lấy chìa REAL rồi mở cửa ERASED tại các bệ an toàn.',
        'inspect_fence|switch_a_erased|cross_fence|switch_b_real|lift_well_brick|take_key|switch_b_erased|unlock_workshop|inspect_workshop_trace',
        {'anchor_phases':['ERASED','REAL','ERASED'],'key_id':'H01_DOOR_KEY','door_phase':'ERASED'},
        {'inputs':['LANTERN'],'outputs':['H01_DOOR_KEY'],'recipes':[]},['E01'],
        'Không Q trên hố/qua tường; reject giữ pose/inventory; không bypass theo Z; key không nằm trong hố buộc chết.',
        ['Rào và nền không tồn tại giống nhau ở hai lớp.','Qua rào tại bệ A, về REAL ở bệ B để tìm chìa dưới gạch.','ERASED qua rào → REAL lấy chìa → ERASED mở cửa xưởng.'],
        'Cửa mở: bóng áo vàng ở xa; không hiện tên hay quan hệ với Minh.',
        'key_taken|door_open|trace_inspected')
    add(3,'Bức ảnh bị tháo rời','CORE',['P02'],
        'CH01.workshop.photo_bench; ba tile gỗ ở ngăn mở dưới bàn; ghi chú trên giá dụng cụ, mặt sau khung có đường ghim liên tục.',
        [('CH01.workshop.tool_shelf','Ghi chú: bờ nước dẫn tới gốc cây; chỗ trú nằm sau gốc cây, không ghi nguyên chuỗi tile.'),('CH01.workshop.frame_back','Dấu ghim mép chỉ khớp liên tục khi tile đúng chiều; hình hai đứa trẻ không ghi tên.')],
        'Kết hợp quan hệ cảnh quan với mép ghim để suy ra thứ tự và chiều tile.',
        'take_three_tiles|inspect_note|flip_frame|orient_tiles|arrange_tiles|confirm|take_photo_record',
        {'slot_order':['RIVER','TREE','TWO_CHILDREN'],'rotations':[0,0,0]},
        {'inputs':[],'outputs':['PHOTO_TILES'],'recipes':[]},['E02'],
        'Chỉ xếp đúng thứ tự nhưng tile lộn ngược vẫn sai; không gọi hai đứa trẻ là anh em trước CH06.',
        ['Đường ghim và cảnh vật kể cùng một hành trình.','Bắt đầu ở bờ nước, theo tới gốc cây; kiểm tra mặt sau từng tile.','Sông → cây đa → hai đứa trẻ; cả ba tile để đúng chiều.'],
        'Lật ảnh: bóng thứ hai mờ tạm rồi tiếng gõ ngoài khung; ảnh neo/journal giữ bản đã thấy. Closeup an toàn, actor chỉ xuất hiện khi thoát.',
        'tile_positions|tile_rotations|photo_taken|scare_seen')
    add(4,'Tiếng gõ trong xưởng','SECRET',['P03'],
        'CH01.workshop.side_alcove; Knocker ERASED chắn hộc; bàn mồi cách hộc 4m, cover Shared ở giữa, lối rút không bị khóa.',
        [('CH01.workshop.side_door','Tiếng gõ thử từ prop làm Knocker quay về nguồn âm; caption biểu thị hướng.'),('CH01.workshop.clock_case','Cót tháo được từ đồng hồ xưởng khác đồng hồ mẹ; con quay có rãnh cùng biểu tượng đầu cót.')],
        'Suy ra hành vi nghe âm và công dụng của con quay cót; chọn vị trí mồi xa hộc, không chỉ bấm đợi.',
        'observe_sound_reaction|take_top|take_spring|combine_wound_top|place_decoy_far_table|activate_decoy|use_cover|open_hidden_drawer|take_m01',
        {'recipe':'WOUND_TOP','decoy_socket':'FAR_TABLE','retrieve_socket':'HIDDEN_DRAWER'},
        {'inputs':['WOODEN_TOP','WORKSHOP_SPRING'],'outputs':['WOUND_TOP'],'recipes':['WOUND_TOP']},['M01'],
        'Mồi đặt cạnh hộc không tạo tuyến an toàn; bắt không mất clue; mồi quay lại socket/reset cót khi checkpoint/revisit, không hữu hạn một lần.',
        ['Nó hướng về nơi phát tiếng động.','Con quay và dây cót có thể tạo tiếng gõ ở chiếc bàn xa.','Ghép con quay+cót, đặt bàn xa, kích hoạt rồi đi qua cover tới hộc.'],
        'Cảnh giới/chase có cue; không capture khi đang ghép đồ trong closeup an toàn.',
        'recipe_known|decoy_socket|decoy_state|drawer_open|m01_taken')
    add(5,'Bốn chiếc bát','CORE',[],
        'CH02.dining.table; Bắc cố định theo biểu tượng cửa sổ, không theo camera; bát ở tủ chạn mở, dấu ghế ERASED và sơ đồ dưới bàn.',
        [('CH02.dining.table_underside','Chủ nhà đối diện cửa ra sân, Hạnh đối diện mẹ; sơ đồ không ghi đủ tên.'),('CH02.kitchen.dialogue','Anh cả ngồi phía mặt trời mọc; dấu trên cửa sổ định hướng Đông; dấu ghế ERASED xác nhận chỗ thứ tư.')],
        'Kết hợp quan hệ đối diện, hướng Đông và dấu ghế để xác định bốn người, không dựa phong tục.',
        'inspect_table_back|inspect_erased_seats|hear_meal_memory|place_four_bowls|confirm|take_inner_key',
        {'north':'MOTHER','east':'SON_A','south':'HANH','west':'SON_B'},
        {'inputs':[],'outputs':['H02_INNER_KEY'],'recipes':[]},['E03'],
        'Quay camera không đổi slot IDs; đổi SON_A/B phải sai; biểu tượng hướng có chữ, không đòi kiến thức văn hóa.',
        ['Các dấu ghế mâu thuẫn với số người được thừa nhận.','Mẹ đối diện Hạnh; anh cả ở phía mặt trời mọc.','Bắc mẹ, Đông anh cả, Nam Hạnh, Tây em trai.'],
        'Một chiếc đũa rơi, dấu bàn tay ló rồi mất; reduced-flash dùng fade dài; không encounter.',
        'bowl_slots|inner_key_taken')
    add(6,'Tủ quần áo không có chủ','SUPPORT',['P05'],
        'CH02.hanh_room.wardrobe; vào qua cửa ERASED rồi đổi tại bệ Shared bên trong; ba thanh trượt trên tủ.',
        [('CH02.hanh_room.height_wall','Vạch HOA năm Y1=95, CHIM Y2=110, SAO Y3=125; chữ năm và thước cm đọc được.'),('CH02.storage.clothing_tags','Nhãn ba ngăn lần lượt CHIM, SAO, HOA; năm trên áo chứng minh không xếp ngăn theo tuổi tăng dần.')],
        'Ánh xạ biểu tượng ngăn sang năm/vạch chiều cao; không đơn thuần chọn vạch cuối.',
        'unlock_inner_room|enter_erased|switch_shared_pad|inspect_height_wall|inspect_tags|set_three_sliders|confirm|take_hanh_notebook',
        {'drawer_order':['BIRD','STAR','FLOWER'],'slider_cm':[110,125,95]},
        {'inputs':['H02_INNER_KEY'],'outputs':['HANH_NOTEBOOK'],'recipes':[]},[],
        '95,110,125 theo thứ tự tăng là sai; nền/cửa bảo đảm đường về; không thao tác tủ xuyên vách.',
        ['Các ngăn dùng biểu tượng, không dùng thứ tự năm.','Nối CHIM/SAO/HOA trên áo với vạch tường.','Đặt ba thanh theo thứ tự ngăn: 110, 125, 95 cm.'],
        'Âm vải chạm sau lưng, không apparition bắt buộc và không attack.',
        'slider_cm|notebook_taken')
    add(7,'Bức ảnh gia đình thiếu người','CORE',['P06'],
        'CH02.storage.lightbox; kính và hai mảnh ảnh trong phong bì mở ở phòng Hạnh; góc nhìn REAL/ERASED có dấu đăng ký khác nhau.',
        [('CH02.dining.real_photo','REAL ba người, góc khung có dấu vuông/chấm đăng ký.'),('CH02.hanh_room.erased_photo','ERASED thêm người thứ tư; nét thêu và chữ Hạnh trong sổ nối được với mặt sau ảnh.')],
        'Chồng đúng hai bản và đối chiếu chữ viết để chứng minh người thứ tư là Hạnh; không chỉ ghép ảnh cho đẹp.',
        'record_real_photo|record_erased_photo|take_overlay_pieces|align_registration|select_name_evidence|confirm|confront_lien',
        {'alignment':['SQUARE_TOP_LEFT','DOT_BOTTOM_RIGHT'],'name':'HANH','proof_item':'HANH_NOTEBOOK'},
        {'inputs':['HANH_NOTEBOOK'],'outputs':['PHOTO_OVERLAYS'],'recipes':[]},['E04'],
        'Không auto solve khi thu đủ mảnh; chọn ảnh không đăng ký đúng hoặc tên không có chứng cứ trả feedback.',
        ['Khung ảnh lưu hai phiên bản của cùng một chỗ trống.','Căn hai dấu vuông/chấm, rồi so chữ sau ảnh với sổ.','Vuông trên trái, chấm dưới phải; dùng sổ Hạnh để xác nhận tên.'],
        'Tiếng Mẹ ơi và caption sau xác nhận; bà Liên không bị buộc nhớ hoàn toàn chỉ vì đối chất.',
        'overlay_transform|selected_proof|confrontation_done')
    add(8,'Chiếc khăn thêu','SECRET',['P07'],
        'CH02.hanh_room.embroidery_frame; khăn trên ghế mở sau đối chất; mẫu mũi thêu ở tường phòng.',
        [('CH02.hanh_room.stitch_sample','Mũi liền qua nút A tới B, tránh ô gạch chéo biểu thị nền trũng.'),('CH02.hanh_room.scarf','Bốn nút thêu A/B/C/D; đường A-C là đoạn sân ngập, không phải đường tắt.')],
        'Áp dụng quy tắc nối và loại đoạn thấp, dựng đoạn tiếp theo của tuyến tổng chứ không tuyến riêng thẳng lên đồi.',
        'inspect_stitch_sample|flip_scarf|connect_nodes|confirm|take_m02',
        {'path':['A','B','D','C'],'blocked_edges':[['A','C']]},
        {'inputs':[],'outputs':[],'recipes':[]},['M02'],
        'Nối tắt A-C phải sai; retry giữ mẫu; M02 thiếu vẫn qua chương.',
        ['Đường chỉ né các ô nền trũng.','Dùng kiểu mũi ở mẫu tường; đường ngắn nhất chưa chắc khô.','Nối A → B → D → C, tránh cạnh A-C.'],
        'Nhịp đặt bát ngoài phòng, không jumpscare mới.',
        'stitched_edges|m02_taken')
    add(9,'Đèn hiệu ở bến sông','SUPPORT',[],
        'CH03.dock.beacon; kho sửa chữa ở cùng bờ A và luôn mở, không nằm sau cây cầu cần đèn.',
        [('CH03.dock.boat','Tay quay có đầu vuông, khớp trục đèn; pin ký hiệu +/− trên ổ dây.'),('CH03.dock.store','Dây cách điện và sơ đồ mạch cho biết phải nối hai đầu khác cực vào terminal đúng, không nối chập.')],
        'Chọn công cụ đúng khớp và đóng mạch theo sơ đồ; ánh đèn là công cụ quan sát cọc, không tự sửa cầu.',
        'take_crank|take_insulated_wire|inspect_circuit|fit_crank|connect_wire|turn_crank|record_pier_marks',
        {'crank_socket':'SQUARE','wire_connections':[['POS','LAMP_IN'],['LAMP_OUT','NEG']]},
        {'inputs':['DOCK_CRANK','INSULATED_WIRE'],'outputs':['BEACON_READY'],'recipes':['BEACON_REPAIR']},[],
        'Dây sai báo mạch hở/chập bằng hình và chữ, không cháy mất dây; không cần bơi/nhảy lấy đồ.',
        ['Kho cùng bờ có dụng cụ cho đèn.','Đầu vuông khớp tay quay; dòng phải đi qua bóng đèn trước khi về cực âm.','Lắp tay quay; POS→LAMP_IN và LAMP_OUT→NEG, rồi quay.'],
        'Cọc phản chiếu bóng người không có trên bến; chỉ presentation.',
        'crank_fitted|wire_connections|beacon_on|marks_recorded')
    add(10,'Cây cầu tồn tại ở hai thời điểm','CORE',['P09'],
        'CH03.bridge A/B/C Shared; AB chỉ ERASED, BC chỉ REAL; cọc từ đèn bến đánh dấu bệ và hướng đi.',
        [('CH03.dock.pier_marks','Cặp cọc vuông đánh dấu nền đồng thuận ở A/B/C.'),('CH03.bridge.phase_preview','AB mất ở REAL, BC mất ở ERASED; rail không cho vòng Z.')],
        'Dùng dấu cọc để dự đoán nơi có thể đổi lớp và nối hai nhịp không cùng tồn tại.',
        'inspect_pier_marks|switch_a_erased|cross_ab|switch_b_real|cross_bc|activate_store_exit',
        {'anchors':['A','B','C'],'anchor_phases':['ERASED','REAL']},
        {'inputs':['LANTERN'],'outputs':[],'recipes':[]},['E05'],
        'Q giữa nhịp reject không đổi pose; save ở B về được A/C; beacon không là resource cạn.',
        ['Các cọc vuông đánh dấu chỗ còn nền ở cả hai lớp.','A–B cần ERASED, B–C cần REAL.','Đổi sang ERASED ở A, qua B rồi đổi REAL tới C.'],
        'Gỗ kẽo kẹt/nước xa, không enemy mới.',
        'crossed_ab|crossed_bc|exit_open')
    add(11,'Ba bánh van đo mực nước','CORE',['P10'],
        'CH03.gauge_room.panel; ba kim có nấc1/2/3, vị trí ban đầu [1,1,1]; reset chỉ reset máy, không xóa hồ sơ.',
        [('CH03.boatman.note','Đêm lũ trùng mốc bùn thứ hai; không ghi chuỗi thao tác.'),('CH03.gauge_room.pipe_diagram','Van A tăng kim1+kim2, B tăng kim2+kim3, C tăng kim1+kim3; mỗi bước tăng vòng 1→2→3→1.')],
        'Suy ra tác động liên kết rồi tìm cấu hình đưa cả ba kim về mốc2; khác ba van độc lập chép số.',
        'inspect_mud_record|inspect_pipe_diagram|test_linked_valves|set_linked_valves|confirm|inspect_high_mud',
        {'initial':[1,1,1],'target':[2,2,2],'coupling':[[1,1,0],[0,1,1],[1,0,1]],'turns_mod3':[2,2,2]},
        {'inputs':[],'outputs':[],'recipes':[]},['E06'],
        'Đặt một kim2 không solve; mỗi van quay modulo3; reset rõ; không timer làm mất cơ hội đọc.',
        ['Ba van tác động lên những cặp kim khác nhau.','Đưa cả ba kim về mốc bùn, không chỉ kim trước mặt.','Từ reset [1,1,1], quay mỗi van A/B/C hai nấc; ba kim về [2,2,2].'],
        'Vạch bùn/dấu tay dâng theo beat thao tác, dừng khi inspect; Q chỉ qua WorldController tại pose an toàn.',
        'gauge_positions|valve_turns|mud_recorded|horror_beat')
    add(12,'Sổ người lái đò','SECRET',['P11'],
        'CH03.boatman.route_book; hồ sơ trang trái là giờ chuyến, trang phải là mốc đường ngập; journal cho ghim cả hai.',
        [('CH03.boatman.departures','Ba lối: LOW_PIER sẵn01:55/ngập02:00; REED_BANK sẵn01:58/ngập02:03; HIGH_RAMP sẵn01:50/ngập02:20.'),('CH03.boatman.warning_slip','Nhóm tới bến02:04; mỗi lối cần3 phút; phải đến cuối trước giờ ngập và trước vỡ đập02:05 không phải điều kiện hoàn tất hành trình.')],
        'Loại tuyến theo thời gian cả nhóm thực sự đi qua, không theo giờ xuất phát chuyến cũ; HIGH_RAMP tới02:07 vẫn khô.',
        'inspect_departures|pin_flood_marks|compare_arrival_times|select_route|confirm|take_m03',
        {'arrival':'02:04','duration_minutes':3,'safe_route':'HIGH_RAMP','safe_until':'02:20'},
        {'inputs':[],'outputs':[],'recipes':[]},['M03'],
        'Chọn REED_BANK dù chuyến01:58 sớm phải sai; phân biệt thời điểm đập vỡ và nước tới từng lối; không cần biết thủy văn.',
        ['Giờ chuyến cũ không bảo đảm lối còn khô khi nhóm tới.','Tính thời điểm tới cuối mỗi lối, so với giờ nước ngập.','Nhóm02:04, đi3 phút tới02:07: chỉ HIGH_RAMP chưa ngập trước02:20.'],
        'Dấu tay ướt trên sổ sau solve; không xóa giờ đã ghi.',
        'selected_route|comparison_notes|m03_taken')
    add(13,'Thời khóa biểu bị xóa','SUPPORT',[],
        'CH04.class3a.timetable; ba mảnh ở bàn giáo viên, cặp mở, bảng thông báo; phòng tiếp cận trước khóa archive.',
        [('CH04.class3a.teacher_piece','Đọc trước Vẽ; buổi cuối không có môn nào lặp.'),('CH04.school.notice_piece','Hát sau Vẽ; đồng hồ/buổi chỉ đúng hàng cuối, không ba hàng lẫn lộn.')],
        'Dựng thứ tự từ quan hệ trước/sau và xác định đúng buổi, không tìm nguyên chuỗi in trên giấy.',
        'collect_teacher_piece|collect_bag_piece|collect_notice_piece|identify_last_session|order_activities|confirm',
        {'sequence':['READING','DRAWING','MUSIC']},
        {'inputs':[],'outputs':['LAST_TIMETABLE'],'recipes':[]},[],
        'Thứ tự đúng của buổi khác không mở; dùng icon+text, không nghe cao độ.',
        ['Những mảnh giấy mô tả quan hệ giữa các tiết.','Đọc trước Vẽ, Hát sau Vẽ; dùng buổi cuối trên đồng hồ.','Buổi cuối: Đọc → Vẽ → Hát.'],
        'Phấn tự kẻ ba ô trống, không hiện tên An/tiếng gọi anh trước CH06.',
        'collected_pieces|chosen_session|activity_order')
    add(14,'Ba lớp học bị khóa','CORE',['P13'],
        'CH04.school.activity_route; ba phòng mở vào được, khóa chỉ ngăn ngăn tủ/thiết bị và archive; không phải ba cửa khóa nối vòng.',
        [('CH04.class3a.bookcase','Gáy sách tạo mép tranh, lấy được dải tranh sau thao tác Đọc.'),('CH04.art_room.canvas','Dải tranh khớp bức vẽ, mặt sau chỉ socket máy phát; máy dùng đĩa chữ/icon không đo cao độ.')],
        'Vận dụng thứ tự từ P13 và dùng kết quả mỗi phòng làm đầu vào phòng sau; hành động có công dụng thay vì đi bấm ba nút.',
        'open_reading_cabinet|take_painting_strip|restore_canvas|take_player_disc|fit_disc|start_music_player|unlock_archive',
        {'sequence':['READING','DRAWING','MUSIC'],'painting_orientation':0,'disc_socket':'MATCHED_NOTCH'},
        {'inputs':['LAST_TIMETABLE'],'outputs':['PAINTING_STRIP','MUSIC_DISC'],'recipes':[]},['E07'],
        'Chạy máy trước không unlock; wrong order reset tentative stage, giữ đồ đã lấy; capture giữ progress; không bắt đọc khi chase.',
        ['Mỗi căn phòng để lại một vật cho căn tiếp theo.','Tủ sách cho dải tranh; tranh cho đĩa đúng máy.','Đọc lấy dải → phục hồi tranh lấy đĩa → lắp đĩa và bật máy.'],
        'Tên trên bảng bị xóa còn một dòng trống; tiếng gọi không nêu anh/em hay tên Minh; cue knock trước tuần tra.',
        'activity_stage|canvas_state|disc_fitted|archive_open')
    add(15,'Hồ sơ đêm lũ','CORE',['P14'],
        'CH04.archive.timeline_desk; ba trang thu trong archive và alcove gần, cover rõ; mã tủ không in nguyên trên bất kỳ trang nào.',
        [('CH04.archive.documents','WARNING01:48 mang mảnh số4; DAM_BREAK02:05 mang mảnh7; FIRST_BELL02:17 mang mảnh2.'),('CH04.archive.safe_legend','Xếp sự kiện theo thời gian tăng rồi đọc mảnh số từ trái sang phải; không gọi FIRST_BELL là thời điểm VILLAGE_FLOOD.')],
        'Xếp sự kiện thật rồi trích mã hồ sơ472; nhận ra chuông xảy ra sau đập vỡ nhưng chưa tự kết luận ai kéo.',
        'collect_warning|collect_break_notice|collect_bell_log|order_events|derive_file_code|enter_code|open_safe|record_destroyed_village',
        {'sequence':['WARNING','DAM_BREAK','FIRST_BELL'],'times':['01:48','02:05','02:17'],'file_code':'472'},
        {'inputs':[],'outputs':[],'recipes':[]},['E08'],
        'Nhập0217 vào khóa3ô phải sai; capture giữ tài liệu; giờ chính xác là canon hư cấu mới, không ngày lịch cố định.',
        ['Ba tờ là một hồ sơ bị tách, không phải ba mật khẩu.','Xếp theo giờ rồi ghép mảnh số của từng tờ.','01:48 → 02:05 → 02:17; mã hồ sơ 472.'],
        'Hồ sơ làng bị hủy hiện dưới vết bùn; enemy không spawn nhìn thẳng player sau load.',
        'collected_pages|ordered_events|entered_code|safe_open')
    add(16,'Sơ đồ sơ tán trường học','SECRET',['P15'],
        'CH04.school.map_board; các mảnh ở những phòng đã mở; góc bản đồ ghi hướng Bắc cố định.',
        [('CH04.school.exit_plan','3A nối LIBRARY nối REAR_GATE; SHORT_YARD thấp, FRONT_GATE đóng do nước.'),('CH04.school.flood_sheet','Cạnh3A-SHORT_YARD ngập; LIBRARY-REAR_GATE cao hơn vạch nước; nối qua đúng cửa, không qua tường.')],
        'Ghép topology theo cửa và loại cạnh ngập để tìm tuyến thoát thực, không chỉ ghép hình cho khít.',
        'collect_corridor_pieces|align_north|connect_doors|exclude_flooded_edges|confirm|take_m04',
        {'path':['CLASS3A','LIBRARY','REAR_GATE'],'blocked_edges':[['CLASS3A','SHORT_YARD']]},
        {'inputs':[],'outputs':[],'recipes':[]},['M04'],
        'Đường liên tục về hình nhưng qua sân ngập không hợp lệ; xoay không được thay hướng Bắc của bản đồ nền.',
        ['Cửa nối quan trọng hơn mép giấy.','Sân thấp đã ngập; tìm đường qua thư viện ra cổng sau.','3A → thư viện → cổng sau.'],
        'Tiếng bước chân dừng ngoài cửa, không lặp scare bảng.',
        'piece_transforms|selected_edges|m04_taken')
    add(17,'Những lá thư không theo thứ tự','SUPPORT',[],
        'CH05.letter_room.sorting_desk; giấy so sánh của mẹ trong ngăn không khóa; không có chase ở chương này.',
        [('CH05.letter_room.seal_sample','Thư thật phải có cả dấu niêm liên tục qua mép và vết mực thấm mặt sau; bản sao thiếu ít nhất một dấu.'),('CH05.letter_room.letters','A=đêm lũ(thật), B=năm duy trì(thật), C=ghi chú đèn cuối(thật); D=ngày sớm nhưng dấu lệch; E=ngày muộn nhưng không thấm mực.')],
        'Phân biệt nguồn tin đáng tin trước khi xếp thời gian; ngày tháng một mình không đủ.',
        'inspect_reference_seal|flip_five_letters|classify_authenticity|order_authentic_letters|confirm|take_hidden_room_note',
        {'authentic':['A','B','C'],'reject':['D','E'],'sequence':['FLOOD_NIGHT','MAINTENANCE_YEARS','LAST_LANTERN_NOTE']},
        {'inputs':[],'outputs':['MOTHER_ROOM_NOTE'],'recipes':[]},[],
        'Xếp cả5 theo ngày không solve; dấu thấm hiển thị hình/text ở reduced effects; không đòi phân biệt màu mực.',
        ['Ngày đúng chưa chắc là thư thật.','Kiểm tra cả niêm qua mép và mực thấm mặt sau.','Loại D/E; xếp A đêm lũ → B duy trì → C ghi chú đèn cuối.'],
        'Nét chữ đứt dần, motif mẹ; không yêu cầu full voice acting.',
        'letter_faces|authentic_selection|letter_order')
    add(18,'Ánh sáng xuyên hai thế giới','CORE',['P17'],
        'CH05.mother_study; cửa chớp REAL ở trái, ERASED ở phải, giá kính Shared ở giữa có 4 nấc góc; vật kính trong ngăn mở bằng note.',
        [('CH05.mother_study.diagram','Đường khắc tia gồm hai đoạn, mỗi lớp che một đoạn; ký hiệu giá cho biết góc90 hướng vào tường viết.'),('CH05.mother_study.wall','Khi một cửa mở chỉ hiện nửa nét, có caption và outline; kính được giữ trên giá, không bị tiêu hao.')],
        'Ghép trạng thái hai lớp với hướng phản chiếu cố định; không mô phỏng quang học tổng quát.',
        'take_reflector|open_real_shutter|switch_shared_center|open_erased_shutter|fit_reflector|rotate_to_wall|record_hidden_ink',
        {'real_shutter':True,'erased_shutter':True,'reflector_degrees':90},
        {'inputs':['MOTHER_ROOM_NOTE'],'outputs':['REFLECTOR'],'recipes':[]},['E09'],
        'Hai cửa mở nhưng kính sai hướng không reveal; kính dùng tiếp P20, không bị khóa/consume vĩnh viễn.',
        ['Mỗi lớp che một phần đường sáng.','Mở hai cửa ở hai lớp rồi hướng kính về vết chữ.','Mở REAL trái, ERASED phải tại bệ chung; kính ở góc90 vào tường.'],
        'Hiện dòng Tôi có hai đứa con, chưa cho tên/tuổi người bị neo.',
        'real_shutter|erased_shutter|reflector_socket|reflector_angle|ink_recorded')
    add(19,'Cơ cấu bảy điểm neo','CORE',['P18'],
        'CH05.study.anchor_model; bảy đĩa khắc ký hiệu nhà; thứ tự được xác định từ journal năm lần thu hồi, không đồng hồ thực.',
        [('CH05.study.maintenance_log','Các lần thu hồi theo mốcchương H01→H05; mô hình dùng bóng đèn tắt cho cụm đã thu hồi.'),('CH05.study.model_legend','H06/H07 vẫn sáng; H05 đã tắt ở entryCH05; việc vào record H05 qua đèn không phải nhà còn nguyên REAL.')],
        'Phân biệt thu hồi và phá hủy, đối chiếu house symbols với nhật ký để dựng trạng thái hiện tại.',
        'inspect_model_legend|review_house_records|assign_discs|set_anchor_states|confirm|record_maintenance_rules',
        {'inactive':['H01','H02','H03','H04','H05'],'active':['H06','H07']},
        {'inputs':[],'outputs':[],'recipes':[]},['E10'],
        'Không bật tắt theo wall-clock; wrong state chỉ reset model; chưa xác nhận danh tính người neo.',
        ['Mô hình thể hiện cụm nào đã bị thu hồi, không phải nhà nào anh đang đứng trong.','Đối chiếu năm lần đầu với hai đĩa chưa đến lượt.','Tắt H01–H05, giữ H06/H07 sáng.'],
        'Bóng mẹ ngồi viết, tan thành bụi khi gọi; ký ức, không hồi sinh hay phản diện.',
        'disc_assignment|anchor_states|rules_recorded')
    add(20,'Bức thư cuối cùng','SECRET',['P19'],
        'CH05.backyard.shadow_board; cùng REFLECTOR của P18 có thể tháo/đặt lại; hai ổ kính hợp lệ,4góc mỗi ổ.',
        [('CH05.backyard.floor_marks','Bóng cổng ở ổA không nối qua vạch cao; ổB có dấu giày cùng nét kính.'),('CH05.backyard.wall_mark','Ở góc180 của ổB, ba nét tạo đường từ cửa sau sang lối cao; không đòi nhìn đen trên đen.')],
        'Kiểm chứng vị trí lẫn góc, ghép bóng thành tuyến liên tục tránh nền trũng.',
        'retrieve_reflector|inspect_shadow_marks|place_socket_b|rotate_180|trace_safe_path|open_floor_hatch|take_m05',
        {'socket':'B','angle_degrees':180,'path':['BACK_DOOR','HIGH_PAVING','SIDE_EXIT']},
        {'inputs':['REFLECTOR'],'outputs':[],'recipes':[]},['M05'],
        'Không cho kính biến mất giữaP18/P20; pathtrùng hình nhưng quaLOW_PAVING sai; thiếuM05khôngkhóaH06.',
        ['Có nhiều chỗ đặt kính, nhưng chỉ một chỗ nối được lối cao.','So dấu giày với ổB rồi kiểm tra cả ba nét bóng.','ỔB, góc180; cửa sau → nền cao → lối bên.'],
        'Lá thư nhắc người bị quên không đọc tên An trướcCH06; yên tĩnh sau đoạn mẹ.',
        'reflector_socket|reflector_angle|traced_path|m05_taken')
    add(21,'Ba hồi chuông','SUPPORT',[],
        'CH06.mechanics.training_bells; bộ chuông mẫu cách ly, không điều khiển chuông lõi hoặc gây thu hồi.',
        [('CH06.mechanics.manual','Giữ nhịp phải ổn định trước khi Mở lối; Đưa trở về chỉ sau Mở lối; icon/text cho cảba chức năng.'),('CH06.mechanics.test_rig','Kích hoạt sai cho biết mối quan hệ, reset vô hại; âm mẫu có caption hình nhịp tương đương.')],
        'Suy ra quan hệ phụ thuộc cơ khí, không chơi rhythm hay thuộc cao độ.',
        'inspect_manual|test_three_bells|order_functions|confirm|take_counterweight_key',
        {'sequence':['HOLD','OPEN','RETURN'],'bell_mapping':{'1':'HOLD','2':'RETURN','3':'OPEN'}},
        {'inputs':[],'outputs':['COUNTERWEIGHT_KEY'],'recipes':[]},[],
        'Không nhập yêu cầu timing; mute giải được; thử bộ mẫu không được chuyển ending/giếtNPC.',
        ['Các chức năng phụ thuộc nhau.','Giữ nhịp trước Mở; Trở về sau Mở.','GIỮ → MỞ → TRỞ VỀ, tương ứng chuông1 → 3 → 2.'],
        'Knocker cảnh giới ngoài phòng máy; closeup tại bệ an toàn, không capture khi đọc.',
        'test_history|function_order|counterweight_key_taken')
    add(22,'Bộ đối trọng 1–3–2','CORE',['P21'],
        'CH06.counterweight.panel; ba cần theo ID1/2/3, ba bánh có các nấc0/1/2; cầu hạ là state authored.',
        [('CH06.mechanics.result','P21 cho thứ tự tác động cần1→3→2, không phải giá trị của ba cần.'),('CH06.counterweight.gear_marks','Dấu nửa khía nối thành đường khi bánh trái ở0, giữa2, phải1; mô hình cận cảnh có vạch nổi/text.')],
        'Tách thứ tự kích hoạt khỏi cấu hình bánh răng; vận dụng hai nguồn, không chép một mã cho mọi trường.',
        'use_counterweight_key|pull_1|pull_3|pull_2|align_gears|confirm|cross_lowered_bridge',
        {'pull_order':[1,3,2],'gear_detents':[0,2,1]},
        {'inputs':['COUNTERWEIGHT_KEY'],'outputs':[],'recipes':[]},['E11'],
        'Giá trị[1,3,2]không là cấu hình hợp lệ của bánh0..2; spam không double trigger; không lên cầu trướccommit.',
        ['Cần gạt điều khiển trình tự, bánh răng điều khiển khớp nối.','Dùng1→3→2 từ chuông, rồi nối các nửa khía.','Kéo1,3,2; đặt bánh trái0, giữa2, phải1.'],
        'Đối trọng chuyển lộ silhouette áo vàng trưởng thành; không bosscombat.',
        'pull_history|gear_detents|bridge_lowered')
    add(23,'Người không có tên','CORE',['P22'],
        'CH06.memory_room.evidence_table; ảnhE12collect ởentrytrước xác nhận; E08/E10đã ởjournal; hiện bảng quan hệ có socketchữ/icon.',
        [('JOURNAL.E08','Hồ sơ trường có dòng bị xóa với mã giađình trùng ảnh; không gọi tên/quan hệ ởCH04.'),('JOURNAL.E10','Nhật ký mẹ có người con bị giữ ở tháp; không phải người kích hoạt đầu tiên.'),('CH06.memory_room.photo_E12','Ảnh hai đứa trẻ, nét tên AN ởmặtsau chỉđọcđượctạiđây; tênMinh và mãgiađìnhđủ nối.')],
        'Tự nối người trong hồ sơ ↔ người trong ảnh ↔ người ởtháp và chọn quan hệ emgái; đủba chứng cứ không tự reveal.',
        'collect_e12_photo|pin_e08_e10_e12|connect_same_person|choose_sister_relation|confirm_identity|finalize_reveal',
        {'required_evidence':['E08','E10','E12'],'links':[['E08','E12','SAME_PERSON'],['E10','E12','TOWER_ANCHOR']],'relation':'YOUNGER_SISTER','identity':'AN'},
        {'inputs':[],'outputs':[],'recipes':[]},['E12'],
        'Thiếurecordchỉrevisitkhônggrantgiả; chọnmẹ/ngườikíchhoạtphảisai; skipđặtidentityrevealedkhônggrantM06.',
        ['Ba nguồn có dấu chỉ cùng một người.','Mã gia đình nối ảnh với hồ sơ; nhật ký nói ai ở lại tháp.','Nối E08↔E12 cùngngười, E10↔E12 ngườiởtháp; quan hệemgái, tênAn.'],
        'Reveal An hiện21tuổi; hồiức6tuổi chỉ flashback; Minh9tuổi kéo đầu tiên, mẹ duy trì sau.',
        'e12_collected|evidence_links|selected_relation|identity_committed|reveal_finalized')
    add(24,'Đường đối trọng cuối cùng','SECRET',['P23'],
        'CH06.tower.maintenance_chain_board;7đườngxích,3chốt; bảngđườngđitáchbộmôphỏngP21vàchuônglõi.',
        [('CH06.tower.chain_legend','Dấu nhà H01..H07 và nhật ký cho thứ tự thu hồi; chốt A khóađườngthấp, Bmởlối bảo trì, Cgiữđườngcao.'),('CH06.tower.inspection_window','Xíchthấp đứt trước lốiđồi; thấy trực tiếp đường bảo trì khôngngập; dấu mũitên không chỉ màu.')],
        'Theo thứ tự cụm để loại xích mất lực, chọn cấu hình nối đường cao; không tạo tuyến thứ8.',
        'inspect_chain_legend|trace_recalled_clusters|set_latches|confirm_safe_walk|take_m06',
        {'latches':{'A':'CLOSED','B':'OPEN','C':'HOLD'},'route':'MAINTENANCE_HIGH'},
        {'inputs':[],'outputs':[],'recipes':[]},['M06'],
        'Thửbảngkhôngđượcgiảiending; wronglatchchỉfeedback; capturekhôngmấtmảnh; lốinàynốiđoạnM06canonical.',
        ['Xích nối đường thấp đã mất điểm giữ.','Khóa đường thấp, mở lối bảo trì, giữ đường cao.','A=CLOSED, B=OPEN, C=HOLD; chọn MAINTENANCE_HIGH.'],
        'Một hồi chuôngtrầm sau solve, không phátlại revealAn.',
        'latches|chosen_walk|m06_taken')
    add(25,'Chiếc hộp ký ức tuổi thơ','SUPPORT',[],
        'CH07.family_house.childhood_box; con quay/ thuyền giấy/ảnh/thước là vật ký ức bản ghi, không lấy mất mồiP04.',
        [('CH07.family_house.wall_drawings','Bốn khung: quay trướclầnđothước; thuyềnsauquaytrướcảnh; thướcgiữaquayvàthuyền.'),('CH07.family_house.box_slots','Slotcóiconđồvật, đánhsố từtráisangphải; hiệnMinh/Annhỏlàkýứcđãreveal.')],
        'Dựng thứ tự kỷ niệm từ quan hệ trước/sau, không bắt người chơi nhớ cảnh chưa từng thấy.',
        'inspect_childhood_drawings|collect_memory_objects|order_objects|confirm|open_box|take_m07',
        {'sequence':['TOP','HEIGHT_RULER','PAPER_BOAT','PHOTO']},
        {'inputs':[],'outputs':['CHILDHOOD_OBJECT_SET'],'recipes':[]},['M07'],
        'KhôngdùngWOODEN_TOPthậtcủaP04đểkhóamain; M07thuởmainnhưngM01..06khônglàprerequisite.',
        ['Các nét vẽ cho quan hệ giữa những kỷ niệm.','Thước ở sau con quay nhưng trước thuyền; ảnh cuối.','Con quay → thước đo → thuyền giấy → ảnh.'],
        'Tiếng chơi trẻ em xa; cảm xúc, không thêm jumpscaretrướcquyếtđịnh.',
        'memory_objects|ordered_objects|box_open|m07_taken')
    add(26,'Cánh cửa của ngôi nhà thứ bảy','CORE',['P25'],
        'CH07.core_door.three_rings; ổ đèn Shared có dây giữ nên đèn luôn thu hồi được sau mở; bản ghim cluetrướcđâyđọctạiđây.',
        [('JOURNAL.E02_E10','Nét ghim khungảnh=hìnhHAI_DẤU cho kýức; nét vòngkhépnhật ký=VÒNG cho thờigian.'),('JOURNAL.E11','Khía giữđối trọng=CHỐT cho neo; chính vịtrí ba nhãn trên cửa chỉvai trò.')],
        'Nhận ra ý nghĩa ký hiệu lặp xuyên chương, ánh xạ đúng vòng chức năng rồi dùngđèn như chìa.',
        'review_symbol_pins|rotate_memory_ring|rotate_time_ring|rotate_anchor_ring|dock_lantern|confirm|open_core_door|retrieve_lantern',
        {'rings':{'MEMORY':'TWO_MARKS','TIME':'LOOP','ANCHOR':'LATCH'},'key':'LANTERN'},
        {'inputs':['LANTERN'],'outputs':[],'recipes':[]},['E13'],
        'Khônginđủba đápántrêncửa; đènkhôngtiêuhao; chưaM01..06vẫnmởđượcA/B; mởcửachưareturntime.',
        ['Ba biểu tượng đã có ở những vật anh từng kiểm tra.','Khung ảnh, nhật ký, đối trọng lần lượt giải nghĩa ba vòng.','Kýức=TWO_MARKS, thờigian=LOOP, neo=LATCH; đặt đèn, mở rồi lấy lại đèn.'],
        'Bản ghi đêmlũ hiện saucửa; chưa đưa cơ thểngườilớnvềquákhứthật.',
        'ring_symbols|lantern_docked|core_door_open')
    add(27,'Bản đồ cuối cùng','SECRET',['P26','P04','P08','P12','P16','P20','P24'],
        'CH07.core.route_table; सातmảnhM01..M07 vàmũiBắc; quay 0/90/180/270 bằng nút hoặcdrag snapped; dockchốtđầucuối cóID.',
        [('JOURNAL.M01_M07','Mỗi mảnh có from/to và mép nối,7đoạn kế nhau từH07_FRONTđếnHILL.'),('CH07.core.route_legend','Ba nhánh nhóm phải nối vào đoạn cao, không qua cạnhđỏngập; màu có chữblocked/safe.')],
        'Ghép hướng/cổng/nhánh thành đồ thị an toàn, không chỉ đủ sốmảnh; thử sai giữbảnđãghim.',
        'place_seven_fragments|rotate_to_ports|connect_route_edges|attach_three_groups|confirm_map|set_route_plan_ready',
        {'memory_order':[f'M{i:02}' for i in range(1,8)],'rotations_degrees':[0,90,180,270,0,90,180],
         'group_join_nodes':{'GROUP_FAMILIES':'H02_COURTYARD','GROUP_SCHOOL':'H04_SCHOOL_REAR','GROUP_RIVERSIDE':'H03_DOCK_RAMP'}},
        {'inputs':[],'outputs':[],'recipes':[]},[],
        'ChỉđủMkhôngauto solve; P27chỉđặt route_plan_ready, khôngevacuation_route_validated, khôngendingCcomplete; thiếumảnhcóđườngrevisit.',
        ['Bảy mảnh phải nối từ nhà tới đồi, cùng ba nhánh nhóm.','So cổng đầu/cuối, hướng Bắc và lối cao; không chỉ đếm mảnh.','ThứtựM01..M07; góc0/90/180/270/0/90/180; nhómnhàởH02, trườngH04, bếnH03.'],
        'Tuyếnthứba sáng ởmức kếhoạch; tooltip cần kiểm chứng ba nhóm, khônghứađãcứuxong.',
        'fragment_transforms|route_edges|group_joins|route_plan_ready')
    add(28,'Phán quyết của chiếc chuông','CORE',['P26'],
        'CH07.core.final_mechanism + authored evacuation; checkpoint trướcconfirmation vàtrước mỗiquyếtđịnhnhóm; khôngfluid/crowdsim.',
        [('JOURNAL.route_clues','M03chọnHIGH_RAMP; M04chọnLIBRARY→REAR_GATE; M02/M05lốisâncao; P21/P22cổng1→3→2.'),('CH07.core.consequence_panel','A thayneo; Btrảthờigian tuyếnmặcđịnhcómấtmát; CthửtuyếntừP27trướccommittrảthờigian.')],
        'ĐánhgiácáigiáA/B, hoặcvận dụnglạiquyluậtnước/cửa/cổngđểchứngminhtuyếnC; khôngnútC tựwin.',
        'inspect_consequences|open_choice|select_a_b_or_c_trial|confirm_trial_or_choice|resolve_group_decisions|validate_three_groups|final_confirm|play_resolution|credits',
        {'A':'REPLACE_ANCHOR','B':'RETURN_TIME','C':'PLAN_THEN_VALIDATE_THEN_RETURN',
         'group_solutions':{'GROUP_RIVERSIDE':['HIGH_RAMP'],'GROUP_SCHOOL':['USE_SCHOOL_KEY','LIBRARY','REAR_GATE'],'GROUP_FAMILIES':['HIGH_COURTYARDS','GATE_1','GATE_3','GATE_2']},
         'water_progress':'DECISION_BEATS_ONLY','final_c_requires':['ALL_SEVEN_MEMORIES','AN_IDENTITY_REVEALED','ROUTE_PLAN_READY','THREE_GROUPS_SAFE','EVACUATION_ROUTE_VALIDATED']},
        {'inputs':[],'outputs':[],'recipes':[]},['E14'],
        'A/BkhôngcheckP27; Ctrialchỉcầnplan+M+identity, Cfinalcầnvalidate; sai trảcheckpoint giữMkhôngforcedB; chưađủnhómkhôngcreditsC.',
        ['A/B luôn là hai cách xử lý món nợ; tuyến khác phải được chứng minh.','Dùng vạch nước cho bến, cửa sau cho trường, lối cao và cơ cấu cổng cho sân.','BếnHIGH_RAMP; trường dùngchìa→thưviện→cổngsau; sânlốicao→cổng1,3,2; đủbangruprồimớixácnhậnC.'],
        'Nước tiến theo quyết định; đứng đọc/journal/pause không tăng; nhómđượcbiểuđạtbằngsilhouetteâmthanh/caption; tuổiB/Cđúngcanon.',
        'selected_ending|trial_active|water_beat|group_decisions|safe_group_ids|evacuation_route_validated|confirmation_committed|resolution_complete')

    # Fix accidental typography before publishing canonical prose.
    for p in puzzles:
        p['scene'] = p['scene'].replace('सात','bảy ')
        p['layout'] = p['scene']
    write('specs/puzzle_catalog.json', puzzles)
    chapters = load('specs/chapter_catalog.json')
    times = [35,40,45,50,45,50,55]
    core = [[2,3],[5,7],[10,11],[14,15],[18,19],[22,23],[26,28]]
    support = [1,6,9,13,17,21,25]
    secret = [4,8,12,16,20,24,27]
    zones = ['Phòng mẹ / cửa hàng ông Nhân / sân / xưởng mộc ông Kha / hộc bên',
             'Sân chung / bàn ăn / bếp / phòng Hạnh / phòng cất đồ',
             'Bến / kho cùng bờ A / cầu / chòi lái đò / phòng đo nước',
             'H04 / lớp 3A / phòng mỹ thuật / phòng âm nhạc / archive / cửa sau',
             'H05 / phòng thư / phòng mẹ / mô hình neo / sân sau',
             'H06 / chuông mẫu / cơ khí / đối trọng / buồng ký ức / tháp',
             'H07 / hộp tuổi thơ / cửa lõi / bàn bản đồ / record sơ tán / đồi']
    for i,c in enumerate(chapters):
        c.update(main_puzzles=[f'P{n:02}' for n in core[i]],support_puzzles=[f'P{support[i]:02}'],
            secret_puzzles=[f'P{secret[i]:02}'],required_puzzles=[f'P{n:02}' for n in sorted(core[i]+[support[i]])],
            all_puzzles=[f'P{n:02}' for n in range(4*i+1,4*i+5)],pacing_target_minutes=times[i],zone=zones[i])
        c['exit_condition']=' AND '.join(f'{pid.lower()}_solved' for pid in c['required_puzzles'])
        if i==6: c['exit_condition']='p25_solved AND p26_solved AND p28_resolution_complete AND credits_reachable'
        if i==0:c['house_name']='Nhà/xưởng mộc ông Kha'
    write('specs/chapter_catalog.json',chapters)
    records=load('specs/evidence_catalog.json')
    for e in records:
        if e.get('source_puzzle'):e['source_puzzle']=mapping[e['source_puzzle']]
        if e['kind']=='MEMORY':
            i=int(e['id'][1:])-1
            e['source_puzzle']=f'P{([4,8,12,16,20,24,25][i]):02}'
        if e['kind']=='ESSENTIAL':
            e['source_puzzle']=next(p['id'] for p in puzzles if e['id'] in p['rewards'])
    # Stable journal IDs keep identity; descriptions now match their new concrete observation.
    titles={'E01':('Dấu vết trong xưởng ông Kha','Traces in Kha’s workshop'),
            'E03':('Bàn ăn bốn chỗ','The four-place table'),
            'E04':('Bức ảnh xác nhận Hạnh','The photo identifying Hanh'),
            'E09':('Dòng chữ dưới ánh đèn','Words revealed by lamplight'),
            'E10':('Nhật ký duy trì bảy điểm neo','The seven-anchor maintenance log'),
            'E13':('Cửa lõi và ba ký hiệu','The core door and its three symbols')}
    for e in records:
        if e['id'] in titles:e['vi'],e['en']=titles[e['id']]
    write('specs/evidence_catalog.json',records)
    route=load('specs/evacuation_route.json')
    route.update(plan_puzzle='P27',execution_puzzle='P28',
        plan_flag='route_plan_ready',validation_flag='evacuation_route_validated',
        validation_condition='P28_THREE_GROUPS_SAFE',water_progress='DECISION_BEATS_ONLY')
    write('specs/evacuation_route.json',route)
    write('specs/puzzle_id_migration_v3_to_v31.json',dict(
        from_version='3.0',to_version='3.1',mapping=mapping,
        retired_semantics=['P13 main core branch is replaced by mandatory P25/P26; only its optional map branch maps to P27'],
        policy='Never infer save compatibility from matching Pxx strings. No produced runtime puzzle/save campaign exists at migration. Future old-save import must validate design_version and replay/restore explicitly; never blindly rename solved flags.',
        owner_source_sha256=hashlib.sha256(raw).hexdigest()))

    plan['meta'].update(version='3.1',updated='2026-10-19',design_revision='ADR-002',
                        puzzle_count=28,core_puzzle_count=14,support_puzzle_count=7,secret_puzzle_count=7)
    for r in plan['requirements']:
        if r['id']=='R05':r['acceptance']+=' Closeup object inspect/flip/rotate, keyboard/pad equivalents, inventory inspect/combine/use đúng target; không tương tác xuyên vách.'
        if r['id']=='R06':r['acceptance']='28 puzzle P01–P28: 14 CORE + 7 SUPPORT bắt buộc + 7 SECRET; mỗi chương 3 main-required + 1 secret; clue→inference→action rõ, hints3tầng tựnguyện; reload/negative/revisit. M01..M06 secret, M07 từ P25; thiếu secret không khóa A/B.'
    for g in plan['gates']:
        if g['id']=='G2':g['criteria']='CH01 P01–P04 hoàn chỉnh: closeup/inventory/recipes/journal pins/hints, main P01/P02/P03 + secret P04; 35 phút mục tiêu chưa đo; tám profile rendered, art/audio/save/stealth, no forced hint. HUMAN_USABILITY_NOT_ASSESSED nếu chưa playtest người thật. Không nhân rộng CH02–CH07 qua G2 fail.'
        if g['id']=='G4':g['criteria']='7 chương, 28 puzzle (14 CORE+7 SUPPORT+7 SECRET), 7 memory, 28 journal IDs,3ending; art/audio/dialoguefinal; all28 puzzle verified, main21 không cần secret; P27plan/P28validation tách biệt; end-to-end.'
    td={t['id']:t for t in plan['tasks']}
    sd={s['id']:s for s in plan['stories']}
    sd['ST-0702']['title']='CH01 giải đố quan sát–suy luận với closeup và inventory'
    sd['ST-0702']['outcome']='Người chơi giải P01/P02/P03 bằng manh mối trong nhiều phòng; P04 được tích hợp encounter S08, toàn CH01 qua G2 trước nhân rộng.'
    sd['ST-0702']['acceptance'] += ['Closeup/inventory/combine/journal pins/hints dùng chung, keyboard/pad không phụ thuộc kéo chuột.', 'CH01 P01–P04 có unique solve rules và rendered wrong/reload/revisit; M01 optional cho main.']
    new_specs=[
        ('InspectableObject và giao diện kiểm tra cận cảnh', ['scripts/interaction/inspectable_object.gd','scenes/ui/inspection_view.tscn'], 'Range/LOS/phase check trước mở; zoom/flip/rotate có nút keyboard/pad tương đương; lock có owner, journal/menu/focus/close không rò lock; closeup an toàn không capture.'),
        ('Inventory quest và recipe giao dịch nguyên tử', ['scripts/inventory/inventory_manager.gd','data/items/','data/recipes/'], 'Inspect/combine/use bằng stable IDs; recipe FIT_LENS/WOUND_TOP; use sai không tiêu hao; reload giữa combine không duplicate/lost items; reused reflector/lantern/decoy luôn có recovery.'),
        ('PuzzleManager và partial-state persistence', ['scripts/puzzles/puzzle_manager.gd','tests/puzzles/'], 'Catalogv3.1 IDs; dependency DAG; apply_action/snapshot/restore/reset; SOLVED monotonic; callbacks không tự sửa WorldController/save; mọi slot/rotation/recipe stage lưu qua registry.'),
        ('Journal ghim manh mối và liên kết chứng cứ', ['scripts/evidence/journal_service.gd','scenes/ui/clue_pins.tscn'], '28 record IDs giữ nguyên; note IDs không tự tăng journal count; ghim đúng những gì đã inspect, không spoiler/answer auto-fill; P23 link+relation phải do người chơi chọn.'),
        ('HintManager ba cấp theo trạng thái và input tương đương', ['scripts/puzzles/hint_manager.gd','data/hints/CH01.json'], 'H/menu tự nguyện, không timer/ads; cấp1 attention,cấp2 relation,cấp3 explicit; VI/EN keys, mute/reduced effects/150%text/keyboard/pad; không đánh solved hoặc tự kéo slot.'),
        ('Tích hợp và kiểm thử các hệ puzzle trước authoring CH01', ['tests/integration/puzzle_systems/','reports/S07/puzzle_systems.md'], 'Dùng actions thật inspect→combine→use→snapshot→restore→hint, wrong target/focus loss/unsafe Q; engine+rendered, không fake solve; evidence riêng capabilities. Sau đó T-070201 author nội dung P01..P03, S08 thêmP04.')]
    previous=['T-070104','T-040104','T-050204']
    new_ids=[]
    for j,(title,outputs,goal) in enumerate(new_specs,5):
        tid=f'T-0702{j:02}'
        t=copy.deepcopy(td['T-070201'])
        t.update(id=tid,title=title,goal=goal,outputs=outputs,acceptance_criteria=[goal],
            depends_on_tasks=previous,dependencies=[],complexity='M',
            read_before=['AGENTS.md','04_TECHNICAL_EXECUTION_CONTRACTS.md','14_PUZZLE_DESIGN_BIBLE.md','specs/chapters/CH01.md','stories/ST-0702.md'],
            evidence_path=f'reports/tasks/{tid}/evidence.json',review_path=f'reports/tasks/{tid}/review.md',
            required_verification=['ARTIFACT_REVIEW','ENGINE_TEST','RENDERED_RUNTIME'])
        t['implementation_steps'][1]=goal
        plan['tasks'].append(t)
        state['tasks'][tid]=dict(status='NOT_STARTED',executor_id=None,evidence=None,blocker=None,notes=[],updated_at=None)
        new_ids.append(tid);previous=[tid]
    sd['ST-0702']['tasks']=new_ids+sd['ST-0702']['tasks']
    td['T-070201']['depends_on_tasks'] += [new_ids[-1]]
    td['T-070201']['goal']='Author P01 đồng hồ/đèn, P02 hàng rào, P03 khungảnh theo v3.1; không dùng đáp án cạnh khóa hoặc debug grants.'
    td['T-070201']['acceptance_criteria']=[td['T-070201']['goal']]
    td['T-070201']['outputs']=['data/puzzles/P01.json','data/puzzles/P02.json','data/puzzles/P03.json']
    td['T-070201']['implementation_steps'][1]=td['T-070201']['goal']
    td['T-070203']['title']='Thêm ba tầng hint tự nguyện cho CH01'
    td['T-070101']['goal']='Khóa CH01 P01–P04 35phút mục tiêu; route cận cảnh hoàn chỉnh, không tách slice10–15phút làm gate thayCH01.'
    td['T-070101']['acceptance_criteria']=[td['T-070101']['goal']]
    td['T-250301']['goal']='Audit/hoàn thiện P03/P04/M01 từ CH01 đã nghiệmthuG2; không trì hoãn gameplay CH01 tớiS25.'
    td['T-250301']['acceptance_criteria']=[td['T-250301']['goal']]
    td['T-250301']['title']='Audit CH01 và payoff M01 theo baseline mới'
    for task in plan['tasks']:
        if state['tasks'][task['id']]['status']!='NOT_STARTED':continue
        wave=int(task['sprint'][1:])
        if wave in [4,7,8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]:
            for rel in ['14_PUZZLE_DESIGN_BIBLE.md','docs/decisions/ADR-002-puzzle-first-gameplay.md']:
                if rel not in task['read_before']:task['read_before'].append(rel)
        ch=next((i for i in range(2,8) if wave in [9+2*i,10+2*i]),None)
        if ch:
            task['puzzle_scope']=chapters[ch-1]['all_puzzles']
            task['implementation_steps'].append('Scope chapter theo v3.1: '+', '.join(task['puzzle_scope'])+'; 3 bắt buộc và 1 secret phải được sản xuất/kiểm thử, secret không khóa main. Đọc card puzzle tương ứng trong specs/puzzles trước authoring.')
    # S23/S24 is CH07, formula above covers it. Explicit full CH01 and ending work.
    for s in plan['sprints']:
        s['tasks']=[t for sid in s['stories'] for t in sd[sid]['tasks']]
    plan['meta']['task_count']=len(plan['tasks'])
    for task in plan['tasks']:
        assert all(d!=task['id'] for d in task['depends_on_tasks'])
    state.update(plan_version='3.1', revision=state['revision']+1)
    assert all(state['tasks'][k]==v for k,v in before_tasks.items())
    assert state['gates']==before_gates
    write('plan/backlog.json',plan)
    write('state/task_state.json',state)
    write('reports/design/v31/migration.json',dict(
        timestamp=datetime.now(timezone.utc).isoformat(),kind='DESIGN_MIGRATION_NOT_GAME_QA',
        old_tasks=len(before_tasks),new_tasks=len(state['tasks']),added_tasks=new_ids,
        existing_task_states_unchanged=True,gates_unchanged=True,
        owner_proposal_sha256=hashlib.sha256(raw).hexdigest(),plan_version='3.1'))
    print('Migrated authoring contracts to v3.1; 28 designs, 6 new unstarted system tasks, no task completions.')


if __name__=='__main__':main()
