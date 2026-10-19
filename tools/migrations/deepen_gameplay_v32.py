"""One-shot owner-authorized 3.1->3.2 design change; no runtime completion.

After application edit the canonical specs, not this historical migration input.
"""
import copy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def write(rel,data):
    p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    plan=read('plan/backlog.json');state=read('state/task_state.json')
    if plan['meta']['version']!='3.1':raise SystemExit('Only accepts3.1; edit canonical specs after migration.')
    original_state=copy.deepcopy(state)
    puzzles=read('specs/puzzle_catalog.json');ps={p['id']:p for p in puzzles}
    # One record per concept, with actual alternatives and thought steps rather than tags alone.
    def deepen(n,question,false_claim,true_claim,extra_clue,route_a,route_b,steps,wrong,consequence,callbacks,uses,teaches,mode,cue,choice,refs):
        p=ps[f'P{n:02}'];pid=p['id']
        c1,c2=p['clues'][0]['id'],p['clues'][1]['id']
        c3=f'{pid}_C{len(p["clues"])+1}'
        p['clues'].append(dict(id=c3,location=extra_clue[0],observation=extra_clue[1]))
        local=[c1,c2,c3]
        p['reasoning']=dict(
            question=question,accepted_hypothesis=f'{pid}_H_TRUE',
            hypotheses=[dict(id=f'{pid}_H_FALSE',statement=false_claim,accepted=False,refuted_by=[c2,c3]),
                        dict(id=f'{pid}_H_TRUE',statement=true_claim,accepted=True,supported_by=[c1,c2,c3])],
            thought_path=[dict(observations=[local[i%3],local[(i+1)%3]],deduction=s[0],action=s[1],feedback=s[2]) for i,s in enumerate(steps)],
            observation_routes=[dict(id=pid+'_ROUTE_A',lead=route_a,clues=[c1,c2]),dict(id=pid+'_ROUTE_B',lead=route_b,clues=[c3,c1])],
            observation_gates_solution=False,
            commit_mode='EVIDENCE_RELATIONS' if n in [7,15,17,19,23] else 'WORLD_ACTION',
            feedback=dict(wrong=wrong,progress='Hiện thay đổi có thể quan sát ở đồ vật hoặc nhóm quan hệ, không bật xanh từng ô đáp án.',per_slot_oracle=False,
                          retry='Giữ mọi quan sát đã commit và draft; chỉ rollback giao dịch thao tác sai.'),
            payoff=dict(immediate=consequence,callbacks=callbacks),uses_knowledge=uses,teaches_knowledge=teaches,local_reteaching=[],
            tension=dict(mode=mode,cue=cue,player_decision=choice,advances_while_reading=False,
                         trigger='Theo action/state đã commit, một lần; không theo timer mở journal.',
                         failure='Theo negative_case; không xóa E/M, không bắt người chơi đọc trong chase.'),
            research_refs=refs,
            acceptance=dict(reasoning='Ít nhất một giả thuyết bị loại bằng quan sát thực và một suy luận dẫn tới hành động có công dụng.',
                            agency='Hai lộ trình quan sát có đầu mối khác nhau; không ép thứ tự inspect của walkthrough.',
                            usability='Ghi quan sát/giả thuyết/thao tác/hint trên build thật; không suy hiểu biết từ solved flag.'))
        p['design_version']='3.2'
        p['persistent_fields']+=['hypothesis_draft'] if p['reasoning']['commit_mode']=='EVIDENCE_RELATIONS' else []

    deepen(1,'Vì sao tiếng chuông và đồng hồ của mẹ chỉ tới một thời điểm?',
        'Ba tiếng chuông nghĩa là đặt giờ3.', 'Kim dài và kim ngắn cho02:17; số hồi chuông chỉ giúp nhận đúng sự kiện.',
        ('CH01.mother_room.clock_test_window','Ô thử cho thấy bánh phút chạy một vòng trong khi bánh giờ chỉ đi một phần; có mô tả chữ, không cần đợi thời gian thật.'),
        'Từ ghi chú của mẹ tìm chiếc đồng hồ ngoài cửa hàng.', 'Từ chốt kính trên đèn tìm ngăn tủ, thử cơ cấu rồi đối chiếu đồng hồ ngoài phố.',
        [('Tách tín hiệu sự kiện khỏi trị số giờ.','inspect_note','Tiếng chuông không khớp cơ cấu nếu chỉ đặt3giờ.'),('Đọc hai kim và dùng đúng đơn vị.','set_hour_and_minute','Khớp cơ cấu trượt cho phép lấy vòng kính.')],
        'Hai kim chưa chỉ cùng một thời điểm; không báo riêng kim nào đúng.',
        'Tự hoàn tất một việc mẹ chuẩn bị dang dở; thử đèn lần đầu sau khi kính khớp.', ['P15','P25'],[],[],
        'REST','Tiếng chuông lẻ sau commit, không apparition.','Chọn đi khảo sát cửa hàng hay thử ngăn tủ trước.',['RS01','RS02','RS03'])
    deepen(2,'Làm sao đi vào một nơi chỉ còn ở lớp bị xóa mà vẫn lấy được chìa ở lớp thật?',
        'ERASED luôn là lớp tốt hơn vì hàng rào biến mất.','Mỗi lớp mất một phần khác nhau; chỉ các nền chung tạo điểm chuyển an toàn.',
        ('CH01.yard.shared_brick_rubbing','Cùng dấu gạch ởhai lớp, nhưng mép giếng chỉ còn support ởREAL; bản ghim cho so hai silhouette.'),
        'Nhìn hàng rào để tìm cách đi qua.', 'Quan sát gạch giếng và dấu bàn tay trên đèn để dự đoán nơi đứng an toàn.',
        [('So cấu trúc chứ không chỉ màu sắc.','preview_both_layers','Thấy rào và nền giếng không biến mất cùng nhau.'),('Lập một đường qua các nền đồng thuận.','cross_via_shared_pads','Qua rào rồi trở lạiREAL lấy chìa, không teleport.')],
        'Đèn báo thiếu nền hoặc thân va tường; pose và inventory giữ nguyên.',
        'Người chơi nhận ra có thể kiểm chứng những điều người làng phủ nhận.', ['P10','P18','P26'],[],['K_PHASE'],
        'ANTICIPATION','Dấu mưa kết thúc trước rào, không chase.','Chọn quan sát lớp kia trước hay thử điểm chuyển gần giếng.',['RS02','RS04','RS07'])
    deepen(3,'Bức ảnh kể một hành trình thật hay chỉ là ba hình trang trí?',
        'Ghép theo hình đẹp hoặc số trên mặt trước là đủ.','Quan hệ cảnh quan và dấu ghim ởmặt sau cùng xác định thứ tự/chiều ảnh.',
        ('CH01.workshop.wood_offcuts','Hai mảnh thử có grain nối được nhưng lỗ ghim lệch; phép thử cho thấy vân gỗ không đủ để quyết định chiều ảnh.'),
        'Đọc ghi chú của ông Kha trên giá dụng cụ.', 'Thử ghép mảnh gỗ mẫu, nhận ra cần kiểm mặt sau khung.',
        [('Dấu ghim là chứng cứ cấu trúc đáng tin hơn bố cục trang trí.','flip_frame','Các lỗ chỉ nối khi ảnh đúng chiều.'),('Đường từ sông qua cây giải nghĩa thứ tự.','arrange_tiles','Ngăn mở và ảnh cho thấy một chỗ đang bị bỏ quên.')],
        'Khung chưa khép thành một dấu ghim liên tục; không chỉ tile sai.',
        'Ảnh tạo câu hỏi về người vắng mặt; hình neo đã lưu không bị scare xóa.', ['P07','P23','P26'],['K_PHASE'],['K_TRACE'],
        'AFTERMATH','Chỉ một lần bóng trẻ mờ và tiếng gõ, sau khi người chơi đã nhìn đủ ảnh.','Tự chọn lúc lật lại ảnh hoặc lùi ra quan sát phòng.',['RS02','RS03','RS07'])
    deepen(4,'Làm sao đưa Kẻ Gõ Cửa ra khỏi tuyến tới hộc mà không để lộ mình?',
        'Tạo tiếng động ngay cạnh hộc sẽ giúp mở hộc dễ hơn.','Nguồn âm phải kéo điều tra ra khỏi tuyến của người chơi, đồng thời còn cover và đường rút.',
        ('CH01.workshop.cover_peek','Từ cover thấy cả bàn xa và trụ bên gác đều kéo đường investigate ra khỏi hộc; đặt ởNEAR_HATCH khiến tuyến tìm kiếm cắt qua đích.'),
        'Thấy con quay và cót khớp nhau rồi thử nguồn âm.', 'Quan sát một tiếng gõ từ gỗ rơi, nhìn đường đi rồi chọn vị trí mồi.',
        [('Phân biệt nguồn âm với vị trí cuối người chơi.','observe_sound_reaction','Knocker nhìn/đi tới nguồn thực trong cùng phase.'),('Chọn mồi tạo tuyến kín, không chỉ kích hoạt đồ.','place_decoy_on_valid_socket','Có hai vị trí khả dụng với đường cover khác nhau.')],
        'Vị trí này làm đường điều tra đi ngang hộc; cho thu hồi và đổi vị trí khi còn an toàn.',
        'Tìm M01 bằng một kế hoạch do mình đặt; mồi có recovery khi retry.', ['P14','P24'],['K_PHASE'],[],
        'COMMITMENT','Ba tiếng gõ có hướng trước Warn; actor không biết player xuyênphase.','FAR_TABLE hoặcLOFT_POST đều hợp lệ nếu đi theo cover tương ứng.',['RS03','RS04','RS07'])
    deepen(5,'Chiếc bát thừa thuộc về ai, và chỗ ấy có thật sự là chỗ khách?',
        'Đó là chỗ để dành cho khách thỉnh thoảng ghé nhà.','Dấu sử dụng và quan hệ gia đình cho thấy một người con có chỗ ngồi cố định.',
        ('CH02.kitchen.bowl_wear','Bốn bát có mức mòn đồng thời; mặt dưới bát dành ghếNam có cùng dấu chim ởáo năm giữa, không có bát khách mới riêng.'),
        'Nghe bà Liên kể bữa cơm và đọc hướng cửa sổ.', 'Giúp xếp bát, thấy độ mòn bất thường rồi kiểm dấu ghế.',
        [('Thói quen lặp lại bác bỏ lời giải chỗ khách.','inspect_bowl_wear','Bátthứtư có lịch sử sử dụng như ba bát còn lại.'),('Dùng quan hệ đối diện và hướngĐông để xếp chỗ.','place_four_bowls','Chỗtrống trùng dấu sử dụng ởlớpkia.')],
        'Những người đối diện nhau chưa khớp lời kể; nhận xét theo quan hệ, không tô đúng từng ghế.',
        'Bà Liên vô thức với tay tới bát của Hạnh; chìa chỉ mở shortcut, không độc quyền vào phòng kýức.', ['P07','P08','P28'],['K_TRACE'],[],
        'REFLECTION','Một tiếng đũa chạm bát rồi khoảnglặng; không bàn tay bật lên mỗi lần thử.','Đi bàn ăn hoặc vạch chiều cao trước; cảhai dẫn tới đối chiếu ảnh.',['RS01','RS05','RS07'])
    deepen(6,'Quần áo không tên là của người khác gửi lại hay một người đã lớn lên trong nhà?',
        'Các áo cũ chỉ là đồ quyên góp không có cùng chủ.','Nét sửa áo, năm và vạch đo nối thành một lịch sử phát triển của một người.',
        ('CH02.hanh_room.hem_stitch','Đường nới gấu lặp lại trên ba áo theo các năm; dấuCHIM nằm ởngăn đầu, khác thứ tự chiều cao tăng dần.'),
        'Từ bát có dấu chim tới tủ, nếu đã giảiP05.', 'Từ lối ERASED nhìn thấy vạch đo, vào phòng trên nền chung dù chưa có chìaP05.',
        [('Theo dấu sửa áo để xác định đây là cùng một người.','inspect_hem_and_wall','Những năm lớn lên nối được nhau.'),('Ánh xạ ngăn theo biểu tượng, không theo thứ tự năm.','set_sliders','Tủ mở sổ có nét chữ nhận diện.')],
        'Ngăn này đang ghép năm của một áo với vạch của áo khác; không xóa các đối chiếu đã ghim.',
        'Sổ biến một căn phòng trống thành dấu vết của một cuộc đời.', ['P07','P17','P25'],['K_TRACE'],[],
        'REST','Tiếng vải trong phòng yên; không enemy hay apparition.','Vào quaERA rồi mởshortcut bằng chìa sau, hoặc dùng chìaP05 nếu đã có.',['RS01','RS03','RS05'])
    deepen(7,'Có thể chứng minh người thứtư là Hạnh, chứ không chỉ đoán một bóng trong ảnh?',
        'Bóng thứtư là vết hỏng ảnh hoặc một vị khách.','Dấu khung, chữ viết và lịch sử sinh hoạt cùng chỉ một người con trong nhà.',
        ('CH02.storage.photo_envelope','Mã nét thêu trên phong bì trùng áo và mặt sau ảnh; không ghi sẵn câu kết luậnHạnh là người thứtư.'),
        'Theo sổ chữ viếtP06 rồi căn hai bản ảnh.', 'Theo vị trí bátP05 và mã phong bì rồi dùng sổ để xác minh.',
        [('Tách lỗi căn ảnh khỏi câu hỏi danh tính.','align_photo_registration','Hai nguồn ảnh khớp hình, chưa tự kết luận tên.'),('Chứng minh bằng hai nguồn độc lập.','link_bowl_notebook_photo','Chấp nhận quan hệ người trong ảnh thuộcgiađình, rồi tênHạnh.')],
        'Chứng cứ được ghép chưa giải thích được cả chữ viết lẫn vị trí trong giađình; không hiện ô tên đúng.',
        'Minh có thể đối thoại bằng vật chứng; bà Liên chỉ bộc lộ thói quen, không lập tức nhớ tấtcả.', ['P23','P28'],['K_TRACE'],['K_IDENTITY'],
        'AFTERMATH','Tiếng gọi Mẹ ơi một lần sau commit, có caption.','Chọn chứng cứ để hỏi hoặc kiểm lại ảnh; không cần đối chất theo một thứtự thoại.',['RS05','RS06','RS07'])
    deepen(8,'Đường thêu mô tả một hoa văn hay một tuyến tránh nước?',
        'Nối các điểm gần nhất sẽ tái tạo đúng hoa văn.','Mũi thêu mã hóa đường cao; nét đứt biểu thị đoạn không thể đi khi nước lên.',
        ('CH02.hanh_room.scarf_back_sample','Một mẫu nhỏ phía sau khăn cho thấy mũiđứt đi qua kýhiệu nềnthấp; bờnút giống vạchgiày ởsân thật.'),
        'Theo mẫu thêu trên tường để đọc khăn.', 'Ra sân nhìn dấu giày/vệt thấp rồi trở lại so mặt sau khăn.',
        [('Giải nghĩa đường đứt từ hai ngữcảnh.','compare_stitch_and_yard','Nhận raA-C là lối ngắn nhưng thấp.'),('Dựng đường qua các cạnh antoàn.','stitch_route','NhậnM02 là đoạn nối, không toàn tuyếnlênđồi.')],
        'Đường liền trên khăn vẫn đi qua một khoảng nền trũng; cho tháo mũi cục bộ.',
        'Việc Hạnh chuẩn bị đường thoát trở thành điều người chơi có thể dùng sau này.', ['P16','P20','P27','P28'],['K_TRACE'],[],
        'REST','Nhịp bát rấtxa, không thêm scare mới.','Bắtđầu khăn sauP06, kểcảchưa xácnhậnP07.',['RS01','RS03','RS04'])
    deepen(9,'Đèn bến không sáng vì thiếu năng lượng hay vì mạch không đi qua bóng?',
        'Có tayquay là chỉ cần quay thật nhiều.','Phải khớp đúng trục và mạch kín qua bóng; nguồn không chữa được đấu sai.',
        ('CH03.dock.beacon_test_plate','Cửa sổ thử mạch hiện hướng dòng bằng hình/chữ; chậpPOS→NEG không qua bóng khiến cửa sổ báoBYPASS.'),
        'Thấy cọc chìm trong tối rồi tìm nguồn sáng.', 'Thấy đầu vuông trên thuyền và dâytrênkho cùngbờ rồi kiểm mạch.',
        [('Phân biệt thiếu công cụ và cấu hình sai.','test_open_circuit','Quay có chuyển động nhưng mạchhở không sáng.'),('Dùng khớp cơ khí và đường mạch làm bằng chứng.','repair_beacon','Đèn làm rõ cọc, không phục hồi nhịp cầu.')],
        'Dòng chưa đi qua bóng đèn; dây còn nguyên để nối lại.',
        'Ông Phúc nhận ra người chơi biết chăm công cụ của bến; đườngkhảo sátcầu cómụcđích.', ['P10','P11'],[],[],
        'REST','Phản chiếu bóng xa không chuyển thành chase.','Khảo sát console đo nướcP11 hoặc sửađèn trước.',['RS02','RS03','RS04'])
    deepen(10,'Cọc nào đánh dấu bệ có thể đứng, cọc nào chỉ ghi một mức nước cũ?',
        'Cọc còn nhìn thấy là chỗ có thể bước lên.','Dấu cọc từđèn cần được đốichiếu bảnđo; nền đồngthuận mới là nơi chuyển lớp.',
        ('CH03.bridge.shared_mark_legend','Bảng gầnconsole phânbiệt kýhiệucọc đo và kýhiệubệ; cảhai có mặttrênhình ghim, không cầnnhớmàu.'),
        'SửađènP09 rồi dùng bảnđoP11 nhận diện bệ.', 'Hiểu bảnđoP11 rồi dùngđèn chiếu để kiểm vịtrí ngoài bến.',
        [('Loại cọc mốc khỏi các điểm đứng.','compare_pier_marks','ChỉA/B/C có support ởcảhailớp.'),('Nối hai nhịp khác phase thành lộtrình.','cross_ab_then_bc','Đếnkho mà không cólầnchuyểnởkhoảngtrống.')],
        'Đích không có nền; không dịch người chơi tới bệ gầnnhất.',
        'Người chơi hiểu mình đang đọc dấu của trậnlũ, không chỉ bấmQ khi thấy biểu tượng.', ['P12','P16','P28'],['K_PHASE','K_WATER'],[],
        'ANTICIPATION','Gỗ kêu nhưng camera vẫn cho đọc bệ, không enemy mới.','Chọn thứ tự điều tra đèn và console; crossing chỉ sau đủcấu hình.',['RS02','RS04','RS07'])
    deepen(11,'Bảnđo nào ghi đêmlũ, và làm sao đưa ba kim về mốc ấy khi van liên kết?',
        'Chỉ cần đặt kim gần nhất về2 hoặc mỗi van chỉnh riêng một kim.','Mốc bùn chọn mục tiêu, sơđồ ống và phép thử cho biết các cặp kim thayđổi cùng nhau.',
        ('CH03.gauge_room.test_strip','Thử một nấcA làmkim1/2cùngtăng;B làm2/3;có nútreset và vạchghi sựkiện, không sốlầnquayđápán.'),
        'Đọc mốc bùn rồi tìm cách cài máy.', 'Thử van ởconsole cùngbờA rồi tìm hồsơ để biết đích cần đạt.',
        [('Nhận dạng quan hệ điều khiển bằng thử nghiệm córeset.','probe_linked_valves','Phản hồi cho thấy cùng một hành động đổi hai kim.'),('Kết hợp mô hình điều khiển với mục tiêu đêmlũ.','set_gauge_target','Ba kim đồngthuận làm lộ vếtbùn cao trên tường cùngbờA.')],
        'Các kim chưa cùng mô tả một bản ghi; hiểnthị kimvậtlý, không đúng/sai từngvan.',
        'Vếtbùn bácbỏ lời làngchưa ngập và cho quy luật đọcđườngcao.', ['P10','P12','P16','P20','P28'],[],['K_WATER'],
        'ANTICIPATION','Một dấu tay xuất hiện theo beat máy, dừng khiđọc.','Tựthử môhình trước khiđọcghi chú; reset không phạt.',['RS02','RS04','RS07'])
    deepen(12,'Tuyến từng được dùng trước vỡđập có còn antoàn khi nhóm thực sự tới bến?',
        'Chọn chuyến xuấtphát sớm nhất là đủ.','Phải cộng thời gian đi vào giờ nhóm tới và so với giờ ngập của từngtuyến.',
        ('CH03.boatman.rope_notches','Dấu nút dây cao củaHIGH_RAMP tươngứng mép khô trong bảnđo, cho đường kiểm độc lập với lịch chuyến.'),
        'Theo lịch chuyến và mốc giờnước để loại lối.', 'Theo độcao cọc/dây trước rồi dùng lịch để kiểm giảthuyết.',
        [('Tách lịchsử chuyến khỏi điều kiện hànhtrìnhmới.','compare_arrival_and_flood','Hai lối thấp không đủ thời gian khô.'),('Kiểm cảhànhtrình chứ không chỉ đầuđường.','choose_high_ramp','M03 ghiđúng tuyến tới02:07 trước mốcngập02:20.')],
        'Lối này từng mở nhưng sẽngập trước khi nhómđi hết; không báo chỉmộtôgiờsai.',
        'Ông Phúc có thể chỉ vào chính tuyến người chơi đã chứng minh; được dùnglại ởfinale.', ['P27','P28'],['K_WATER'],[],
        'REFLECTION','Tiếng nước qua cọc như kýức, không đếmgiờ thật.','Tínhgiờ hoặc khảo sátđộcao trước, sauđó đốichiếu cảhai.',['RS01','RS04','RS05'])
    deepen(13,'Đâu là buổihọc cuối thật, và vì sao các môn xuất hiện theo thứtự ấy?',
        'Ba biểu tượng trên bảng đã là thứtự đọc từtráisangphải.','Phải xác định đúngbuổi rồi suy quan hệ trước/sau trên những mảnh khác nhau.',
        ('CH04.class3a.drawing_layers','Nétbút vẽ nằm trên bàiđọc nhưng dưới dòng nhạc; dấu lớpmực xácnhận thứtự khi chưa đọcđủthờikhóabiểu.'),
        'Thu ba mảnh lịch và kiểmđồnghồ.', 'Quan sát lớpnéttrên bài tập để đặt giảthuyết rồi kiểm lịch.',
        [('Chọn sựkiện/buổi phùhợp trước khi xếp thứtự.','identify_last_session','Loại hàng thuộc buổi trước.'),('Dùng quan hệ trước/sau thayvì vịtríicontrênbảng.','order_activities','Thứtự mở mục tiêu ởba phòng kếtiếp.')],
        'Thứtự này thuộc một buổi khác hoặc làm quan hệ trước/sau mâu thuẫn.',
        'Những lớp học bắt đầu giống một buổihọc đang bịxóa dở.', ['P14','P15','P21','P25'],[],['K_SEQUENCE'],
        'ANTICIPATION','Một đườngphấn tự kẻ rồi dừng; không hiệntên/quan hệAn.','Theo hồsơ hoặc dấu bài tập trước.',['RS01','RS03','RS05'])
    deepen(14,'Có thể khôi phục buổihọc để tiếp cận archive mà không chỉ đi bấm ba nút?',
        'Kích ba cơcấu bất kỳ là mở cửa.','Mỗi hoạt động tạo vật/chứngcứ có côngdụng cho hoạtđộng tiếp theo.',
        ('CH04.school.activity_results','Đĩa cókhía khônglắpvàomáy nếu chưa có phầnlộsau tranh; thửmáy rỗng cho thấy thiếu đầu vào, không gợi nguyênđápán.'),
        'Theo thứtựP13 và vậtphẩm đầu ra từng phòng.', 'Khảo sát tranh/máy trước, phát hiện đầu vào cònthiếu rồi lầnvề tủsách.',
        [('Phân biệt tínhiệu trìnhtự và dependency vật lý.','inspect_empty_player','Mục tiêu cụthể là tìm đĩa, không bấm lại máy.'),('Dùng kết quả của cănphòngtrước.','restore_activity_chain','Archive mở và có đường lùi antoàn trước cue tuầntra.')],
        'Cơcấu cònthiếu một vật tươngthích, không nhận xét thứtự nếu chưa có đầu vào.',
        'Người chơi phục hồi một hoạtđộng đời thường trước khi đọc hậuquả đêmlũ.', ['P16','P22'],['K_SEQUENCE'],['K_SOUND'],
        'COMMITMENT','Cue bướcchân và tiếnggõ báo vùng tuầntra sau khi archive mở; cácphòngđọcan toàn.','Chọn đườngrút cócover, không épđứngđọc trongchase.',['RS02','RS03','RS07'])
    deepen(15,'Hồsơ mô tả lũ, tiếngchuông và sựpháhủy theo quan hệ nào?',
        'Chuông02:17 gâyra vỡđập vì xuất hiện trong cùng hồsơ.','Thứtự01:48→02:05→02:17 bácbỏ việc chuông khởiđầu đậpvỡ; chưa đủ để biết ai kéo.',
        ('CH04.archive.dispatch_stamps','Dấu tiếp nhận riêng của ba trang nối được mảnhsố4/7/2 với sựkiện; tờtườngthuật sao chép viết tắt khôngthể thay timestamp gốc.'),
        'Thu tài liệu, xếp timeline rồi trích mã.', 'Đọc bản tườngthuật gâynghi ngờ, kiểm dấutiếpnhận và các trang gốc.',
        [('Dùng thứtự thời gian để loại một quan hệ nhânquả sai.','order_original_events','Chuông xảyra sau vỡđập, không lộ người kíchhoạt.'),('Áp dụng thứtự đã chứngminh lên mãlưu trữ.','enter_derived_file_code','Tủ mở, kèm danh sách têntrống trong recordE08.')],
        'Lập luận này cần một sựkiện xảyra trước nguyênnhân được gán; không tựchọn lịch đúng.',
        'Câu hỏi chuyển từ nguyênnhân lũ sang cách làng tiếp tục tồn tại.', ['P17','P19','P23','P28'],['K_SEQUENCE','K_WATER'],['K_CAUSAL'],
        'AFTERMATH','Khoảnglặng khi hồsơnguyênbản mở; không thêm scare archive lầnhai.','Kiểm con dấu hoặc đọc nộidung trước; timeline vẫn tự lập.',['RS05','RS06','RS07'])
    deepen(16,'Cửa sau có mấy đường tới, và đường nào còn dùngđược khi nước chuyển giaiđoạn?',
        'Một đường nối liên tục trên giấy sẽ luôn điđược.','Cần cửa thật, nềncao và trạngthái nước; thưviện chỉ antoàn ởgiaiđoạnđầu, gallerycao giữđườngdựphòng.',
        ('CH04.school.gallery_survey','Từ cửa tầnglửng nhìn đượcUPPER_GALLERY→REAR_GATE; vạch cao cho thấy gallery còn trên nước khi thưviện mất antoàn sau một crossingbeat.'),
        'Ghép sơđồ cửa rồi so bảngmực nước.', 'Đi khảo sát gallery và ngưỡngcửa thực rồi ghim lên sơđồ.',
        [('Loại đường qua sânthấp hoặc tườngkhôngcửa.','connect_actual_doors','Còn hai hànhlang khảdụng ởtrạngtháiđầu.'),('Lập một tuyến dựphòng trước khi cần dùng.','compare_route_water_states','M04 lưu cả thưviện và gallery, không tự chọn giùmP28.')],
        'Đường có mépgiấy nối nhưng không có cửa hoặc đã dưới mực nước đang xem.',
        'Chìa cổngsau córecord tươngứng; biết một tuyến chưa đủ cho mọi trạngthái.', ['P27','P28'],['K_WATER'],[],
        'REST','Gió qua lớp trống, không encounter mới.','Lấy nhánhP16 ngay sauP14 hoặc sau hồsơP15.',['RS03','RS04','RS05'])
    deepen(17,'Lá thư có ngày tháng hợp lý đã đủ đáng tin chưa?',
        'Bức nào có ngày sớm/muộn hợp lý đều là thưgốc.','Nguồn phải thỏa cả niêm liên tục và mực thấm, rồi mới dùng nộidung để xếp thời gian.',
        ('CH05.letter_room.reference_envelope','Phong bì mẹgửi bàHảo cóvết mực qua đườnggấp và niêmliền; bản sao môphỏng ngày nhưng không sao được cảhai dấu vật lý.'),
        'Đọc thư rồi tìm điều bất nhất ởdấumực.', 'Kiểm phongbì gốc trước rồi phânloại hộpthư.',
        [('Kiểm nguồn thôngtin trước khi tin nội dung.','classify_originals','D vàE bị loại bởi hai dạng thiếu dấu khácnhau.'),('Xếp các thư đã được chứngthực.','order_authentic_letters','Mở ghi chú phòngkín mà không xácnhận tênAn.')],
        'Bộ thư này có một nguồn chưa đạt cảhai dấu chứngthực; không hiện riêngD/Eđỏ.',
        'Những ghi chép đềuđặn cho thấy mẹ đã kiệt sức giữ điều bàkhông thể nhớ.', ['P19','P23','P26'],[],['K_AUTH'],
        'REFLECTION','Giấy và motif mẹ, không fullvoice hoặc chase.','Bắt đầu từ nội dung hoặc vật liệu giấy; cảhai hội tụ kiểm nguồn.',['RS03','RS05','RS07'])
    deepen(18,'Hai lớp có đang cản cùng một thôngđiệp, và kính phải làm gì để đọc nó?',
        'Mở cửa sáng nhất ởmột lớp là đủ.','Hai lớp che hai đoạn khácnhau; phải giữ trạngthái đúng và hướng kính vào vịtrí mựcẩn.',
        ('CH05.mother_study.partial_ink_trace','Một nét hiệnkhi mởREAL, nétkhác hiệnkhi mởERASED; môhìnhP19 chora chốt giữthôngđiệp, không cho sẵn góckính.'),
        'ThưP17 dẫn tới phòng, rồi môhìnhP19 giải nghĩa chốt.', 'MôhìnhP19 nêu điều còn thiếu, rồi thưP17 mở đường tới côngcụ.',
        [('Kiểm phần nào thuộc lớp nào.','test_shutters_separately','Mỗi lầnthử cho một phầnnét chứ chưa đủ đọc.'),('Kết hợp vịtrí và hướng từ dấutường.','place_reflector','Thôngđiệp xuất hiện mà kính vẫn tháora dùnglại được.')],
        'Ánhsáng chưa đi qua cảhai đoạn; dùng outline/text thaymàu và tia chói.',
        'Người chơi tự khôi phục một thôngđiệp mẹ không còn đủ sức nói.', ['P20','P23','P26'],['K_PHASE','K_TRACE'],[],
        'REST','Không apparition mới, ánh đèn dừng khi đủ nét.','Khảo sát chớp hoặc tìm dấutường trước khi lắp kính.',['RS02','RS03','RS07'])
    deepen(19,'Nhàbị xóa có đồng nghĩa người ở đó đã chết, và môhình đang ghi thờiđiểm nào?',
        'Đang đứng trongH05 nghĩa làH05chưa thu hồi, hoặc cụmtắt chỉ là dânđãchết.','REALvàrecordkhác nhau; dấu thu hồi theo nhà cho trạngthái5tắt/2sáng mà chưa kếtluận sốphận từngngười.',
        ('CH05.study.model_entry_log','Nhật ký tiếp cận từ entry có niêmgốc/đườngmực mẫu riêng; ghi H05 vừa thu hồi trong khi cửađèn vẫn cho vào record. Có thể kiểm nguồn tạiđây nếu chưa giảiP17.'),
        'Đọc nhật ký thường rồi đốichiếu môhình.', 'Quan sátH05 ởhai lớp rồi hỏi môhình vìsao nhà vẫn vào được.',
        [('Phân biệt quan sát hiện tại và tínhchất của record.','compare_h05_layers','Không dùng việc đứng trongnhà làm bằngchứng cụm cònactive.'),('Đối chiếu5sựkiện và kiểm nguồn nhật ký.','set_anchor_states','Mở quy tắcduytrì và trang về mộtngườicon ởtháp trongE10.')],
        'Cấu hình đang trộn thờiđiểm trước và sau thu hồiH05; không khẳngđịnh aiđãchết.',
        'Người chơi hiểu mónnợ trước khi được yêu cầu quyếtđịnh kếtthúc.', ['P18','P23','P24','P28'],['K_CAUSAL','K_AUTH'],['K_AUTH'],
        'REFLECTION','Bóng mẹ xuất hiện một lần nhưrecordđangviết, rồi tan; không đuổi theo.','Khảo sát môhình trướcP17 hoặc theo thư tới sau.',['RS04','RS05','RS07'])
    deepen(20,'Có thể dùng cùng tấm kính để đọc một lối đi khác, không chỉ dòng chữ trên tường?',
        'Một góc làm bóng đẹp là lời giải.','Bóng phải nối các lối thật trên nềncao; cảổđặt, hướng và topology đều cần khớp.',
        ('CH05.backyard.high_paving_view','Nhìn từ cửa sau thấy lốiSIDE_EXIT nối nềncao; ổA tạo ảnhđẹp nhưng rơi vàoLOW_PAVING.'),
        'Theo dấu bóngtrênsàn rồi tìm cách đặt kính.', 'Khảo sát lốiđi thật trước rồi tìm cách dùngkính để đọc nétbóng.',
        [('Kiểm ýnghĩa khônggian của hình tạo được.','trace_shadow_against_yard','Loại cấu hình khớphình nhưng qua nềntrũng.'),('Vận dụng côngcụ quen vào mụcđích mới.','set_reflector_and_trace','M05 nối tiếp đườngđãtìm, không mở secret bằng maymắn xoayđồ.')],
        'Hình nối được nhưng tuyến này đi xuống khoảngthấp; không consume kính.',
        'Lá thư cuối cho thấy mẹ đã chuẩn bị đường cho người khác, chưa gọi tênAn.', ['P27','P28'],['K_PHASE','K_WATER','K_TRACE'],[],
        'REST','Khoảngyên sau đoạnmẹ; không scare thưởng secret.','Đọc bóng trước hoặc đi khảo sát nền thật trước.',['RS02','RS04','RS07'])
    deepen(21,'Ba chức năng của chuông phụ thuộc nhau thế nào?',
        'Chuông nào nghe mạnh hơn thì kích trước, hoặc 1/2/3 là thứtự mặcđịnh.','Giữ phải ổnđịnh trước mở, trảchỉ khi đườngmở; âm và icon mô tả cùng quy tắc.',
        ('CH06.mechanics.safe_test_result','Bộthử cáchly chora kếtquả khi OPEN trướcHOLD: chốttrượt vềchỗcũ; RETURN trướcOPEN khôngdịchcầu. Không tácđộng lõi.'),
        'Đọc hướngdẫn chức năng rồi thử xácminh.', 'Thử bộmẫu, nhìn các lỗi cơkhí rồi kiểm hướngdẫn.',
        [('Suy quan hệ trước/sau từ kếtquả thử.','test_bell_functions','Thấy vìsaoMỞtrướcGIỮkhông duytrì được lối.'),('Ánhxạ chức năng vào cần có nhãn.','order_functions','Nhận chìa nhưng không khiến nhà nào bịthu hồi.')],
        'Trạngthái chưa được giữ hoặc lối chưa mở; âm có caption, không yêu cầu nhịpthời gian.',
        'Người chơi học quy tắc sẽ tự vận hành lúc cứu người.', ['P22','P24','P28'],['K_SEQUENCE'],['K_HOLD_OPEN'],
        'ANTICIPATION','Tiếnggõngoàiphòng có hướng; bộmẫu an toàn.','Đọc trước hoặc thử trước; tự reset môhình không phạt.',['RS02','RS03','RS07'])
    deepen(22,'Thứtự kéo cần và cấu hình bánh có phải cùng một đápán?',
        'Đặt mọi trường thành1/3/2 sẽ mở cầu.','Trìnhtự điều khiển lấy từ chức năng; khớprăng là một quan hệhìnhhọc riêng.',
        ('CH06.counterweight.inspection_slot','Khe kiểm cho thấy dấuđôi trên mépkhớp chỉnối khi bánhở0/2/1; nhãntrêncầnkhông phải sốnấc bánh.'),
        'Mang kếtquảP21 tới cần rồi kiểm bánh.', 'Khảo sát khớpbánh trước để hiểu cần đang mở khóa phần nào.',
        [('Phânbiệt hai loại biến trong một cơcấu.','pull_ordered_levers','Chốt giữổnđịnh nhưng cầu chưa hạ nếu bánh chưa khớp.'),('Dùng hìnhhọc quan sát được để cănkhớp.','align_gears','Cầu hạ, cho qua và mở shortcut về vùngan toàn.')],
        'Chốt đã giữ nhưng đườngkhớp chưa liên tục; không reset thứtự đãcommit.',
        'Thànhcông có nhịp giải tỏa trước khi bước tới người không tên.', ['P24','P26','P28'],['K_HOLD_OPEN','K_SOUND'],[],
        'COMMITMENT','Cảnhgiới cócue trước khi rời phòngmáy; không capture trongcloseup.','Chọn đườngcover/shortcut để qua vùngtuầntra; mởviewmớibịchặn khiChase.',['RS02','RS04','RS07'])
    deepen(23,'Người trongảnh, dòngtên trống và ngườiởtháp có phải cùng một người — và có quan hệ gì với Minh?',
        'Đó là một ngườigiữchuông không liênquan hoặc chính mẹMinh thời trẻ.','Mãgiađình/nétchữ/tuổi trongảnh và ghi chú haiđứacon chứngminh An là emgái và là ngườiởlại.',
        ('CH06.memory_room.photo_reverse','Ảnh có mãgiađình, ngày chụp tươngđối và chỗtênAN; tuổi mẹ trên phongbì không thể là đứatrẻ6tuổi. Không gọi tên trướcCH06.'),
        'Từ dòngtrốngE08 tới ảnhE12 rồi dùngE10chứngminh ngườiởtháp.', 'Từ trangmẹE10 tớiảnhE12 rồi kiểm mãgiađìnhE08; cảba vẫn cần có trongjournal.',
        [('Chứngminh cùngmộtngười qua mã và tuổi, không chỉ tênđọcđược.','link_same_person','Bảnđồquan hệ hìnhthành mà chưa tự phátreveal.'),('Chọn quan hệgiađình và vai trò táchbiệt.','confirm_identity_with_relations','Revealchỉ sau commitcủangườichơi; An21tuổi và kýức6tuổi đượcphânbiệt.')],
        'Bộquan hệ chưa giải thích được tuổi và ghi chúgiađình; không thử lầnlượt tên để nhận ôđúng.',
        'Người chơi tìm lại một người em qua côngviệc tựđiềutra; An không thành phản diện.', ['P25','P26','P28'],['K_IDENTITY','K_AUTH','K_CAUSAL'],[],
        'AFTERMATH','Reveal rung/âm vừa phải, córeducedeffects và skipfinalization.','Chọn nguồnđầu để liênhệ; xácnhận chỉ khi tựtin, khôngtimer.',['RS05','RS06','RS07'])
    deepen(24,'Lối bảo trì nào còn được giữ khi các xích thu hồi lần lượt mất lực?',
        'Mọi đườngxích còn nhìnthấy đều đangchịulực.','Phải nối với cụm còn giữ và tránh đường thấp, rồi đặt chốt theo chức năng đã học.',
        ('CH06.tower.chain_tension_marks','Cửa sổcạnhboard cho thấy đườngxíchthấp võng dùhình cònđó; dấu nêntảngcao trùng sơđồbảotrì.'),
        'Theo lịchthu hồi từP19 rồi lần xích.', 'Quan sát xíchchịulực từ cửa sổ rồi đốichiếu lịch và chốtP21.',
        [('Tách hình còn tồn tại khỏi khả năng đỡ thực.','trace_live_chain','Loại tuyếnthấp và xích đãmấtđiểmgiữ.'),('Áp dụngGIỮ/MỞđểchọn tuyếncao.','set_maintenance_latches','M06ghi một đoạn an toàn, không kích hoạt ending.')],
        'Chốt đúng hình nhưng đang dựa vào một xích không chịu lực; không thôngbáoriêngchốtnàođúng.',
        'Người chơi có thể tìm lối này trước cuộcgặpAn nhưng chưa được biết danh tính.', ['P27','P28'],['K_HOLD_OPEN','K_CAUSAL'],[],
        'REST','Tiếngxích trongtháp, không lặp cinematicreveal.','BắtđầusauP22 trướcP23 hoặc quaylạisauđối thoại.',['RS02','RS04','RS07'])
    deepen(25,'Những mónđồ tuổi thơ thuộc các kỷniệm nào, và vìsao hộp còn giấu một đườngđi?',
        'Cần mang con quay thật từ nhánhbí mậtP04 tới đây.','Đây là cácvậtrecord tại nhà; quan hệ nétvẽ chỉ thứtự kýức và dẫn tới đoạnđườngM07.',
        ('CH07.family_house.paper_boat_fold','Mặttrong thuyềncó dấuđothước mới hơn tròconquay, nhưng nếpảnhchụp nằmsau đó; cho mộtđườngđối chiếu khác tranhtrên tường.'),
        'Đọc bốnkhungvẽ rồi sắpđồ.', 'Lật đồrecordđể đặt giảthuyết thứtự rồi kiểm nétvẽ.',
        [('Xácđịnh đồ ởđây là vật của record, không questitem phải mangtới.','inspect_memory_objects','Có đủvật ởmainroute dù thiếuP04.'),('Dùng quan hệtrước/sau để khôiphục kỷniệm.','order_childhood_objects','HộpmởM07 và một khoảnglặng trướcquyết định.')],
        'Thứtự này làm nétđo mới xuất hiện trước sựkiện mà nó dựavào; không xóa đồrecord.',
        'Người chơi nhớ lại haiđứatrẻ có lịch sử chung và một kếhoạch còn dangdở.', ['P27','P28'],['K_SEQUENCE','K_TRACE'],[],
        'REFLECTION','Âmchơi trẻemxa, không jumpscare trướcfinale.','Giải hộptrước hoặc mởcửaP26trước; finalpanel chờ cảhai.',['RS03','RS05','RS07'])
    deepen(26,'Những ký hiệu quen thuộc là mã tùyý hay biểu đạt ba chức năng của lõi?',
        'Lấy hìnhtrông giốngnhau rồi xoay vòng ngẫunhiên là đủ.','Dấu ghim giữkýức, vòngkín biểu thị thờigianlặp, chốt giữđiểmneo; đúngvai trò mới nhậnđèn.',
        ('CH07.core_door.function_preview','Mỗi vòng thử chỉ lộ một chuyểnđộng dạngghim/vòng/chốt; không tô đúngkýhiệu, người chơi đối chiếu với bản ghim cũ.'),
        'Theo kýhiệutừkhungảnh/nhậtký/đốitrọng đãghim.', 'Thửcửa đểhiểu chức năngcần, rồi mởjournalđối chiếu nguồn.',
        [('Nhậnra một quy tắc cũ trong ngữcảnh mới.','compare_symbol_functions','Mỗi nguồn giải một vai trò, không cần thêmmãmới.'),('Áp dụngcấuhình và dùngđèn nhưchìa thu hồiđược.','open_core_with_lantern','Mởrecordđêmlũ, chưa returntime hay tự chọnending.')],
        'Cơcấu chưa ghép đúng ba chức năng; giữ draft vòng, đèn không bịconsume.',
        'Các phát hiện rải qua game được vận dụng thật để tới lõi.', ['P27','P28'],['K_TRACE','K_AUTH','K_HOLD_OPEN'],[],
        'ANTICIPATION','Nướcxa saucánhcửa, không đồnghồ đangchạy.','Mởcửatrước hộpP25 hoặc sau, rồi quay lại panel khiđủđiềukiệnmain.',['RS02','RS04','RS05'])
    deepen(27,'Một đường liền trên bản đồ đã đủ để cứu ba nhóm chưa?',
        'Đủ7mảnh hoặc ghépđược nétliền là đã cứu xong.','Mỗi đoạn phải có cổng/hướng đúng và điểm nhập của ba nhóm; đây mới là một kếhoạch cóthể thử.',
        ('CH07.core.route_group_overlay','Tấmphủ nhómchỉvị trí xuấtphát và dấunềncao; một cáchghép trôngliền nhưng đưa trường tới cửađãđóng hoặc saiđiểmnhập.'),
        'Ghép tuyếnđầu/cuốirồigắn ba nhóm.', 'Ghim ba nhóm và trạngtháiđườngtrước, rồi tìm cácđoạnnối chung.',
        [('Tách topology, hướng và khả năng dùng tuyến.','rotate_and_join_fragments','Bảnđồ phản hồi hởcổng hoặc nhánh qua đoạnkhônghợplệ, không tômộtmảnhđúng.'),('Đối chiếu lộtrình vớimọi nhóm thayvì chỉHILLđích.','attach_groups_and_confirm_plan','route_plan_ready đặt; validated vẫnfalse.')],
        'Đường còn bỏ một nhóm hoặc đi qua chỗ không có lối; không chỉ đánh dấu fragment đúng.',
        'Người chơi tạo một phương án cứu người từ kiếnthức tíchlũy, chưa được trao chiếnthắng sẵn.', ['P28'],['K_WATER','K_TRACE'],[],
        'ANTICIPATION','Tiếngchuôngtrầm và ánhsánglộ tuyến, không nước tăng khi ghép.','Ghép từnhàđếnđồi hoặc từđiểmnhập cácnhóm; cùng một graphđược chấpnhận.',['RS04','RS05','RS07'])
    deepen(28,'Có thể vận hành phương án cứu người khi điều kiện thayđổi, và lựa chọn cuối có giá gì?',
        'Lập bảnđồ xong nghĩa là nhấnC sẽ cứu tấtcả, hoặc cứ làm theo một thứtự cốđịnh.','Phải chuẩn bịGIỮ/MỞ, chọn đường theo beat, đưa đủ3nhóm rồi mớiTRẢ; A/Bvẫn là hai cách xửlý mónnợ hợp lệ.',
        ('CH07.evacuation.decision_preview','Trước mỗicrossing, mốc nước và caption báo giaiđoạn kếtiếp. Thưviện antoàn khi chưa nhómnàocross; gallerycao còn dùngđược vềsau.'),
        'Lập phươngán từP27 rồi kiểmtrước từngcrossing.', 'Khảo sátpreviewtuyến/nhóm, điều chỉnh kếhoạch trước khicommit.',
        [('Đọc điều kiện hiện tại thayvì chép lại một walkthrough.','preview_next_crossing','Người chơi biết crossing sẽ đổi gì, đọc/pause không tựtăngbeat.'),('Chuẩn bị cơcấu và thực hiện kếhoạch cóthể điềuchỉnh.','hold_open_cross_groups','Các thứtự nhómkhác nhau hợp lệ nếu chọnđường đúng.'),('Xácnhận saukhi kếtquả đãđược kiểmchứng.','validate_then_return','Chỉ3nhóman toàn mớivalidated/finalC; sai giữcheckpoint và không forcedB.')],
        'Tuyến không còn phùhợp với beat hiện tại; giữ cácnhómđã antoàn, quay lại quyếtđịnh này để chọn gallery. A/Bkhôngbịgắn nhãn sai.',
        'Cao trào đo sựhiểu biết và trách nhiệm của người chơi; epiloguevàtuổi giữ đúngcanon.', [],['K_WATER','K_SEQUENCE','K_HOLD_OPEN','K_CAUSAL'],[],
        'COMMITMENT','Nước/âmtheocrossing đãcommit; cuevàcaptionbáo trướcnhánhthayđổi.','Chọn A/BhoặcthửC; Ccó6thứtự nhóm và8kếhoạchđường hợp lệ, đượcreplan.',['RS04','RS05','RS07'])

    # Physical layout/action changes needed for genuine branching, not just prose routes.
    ps['P04']['depends_on']=['P02']
    ps['P04']['solution']['accepted_decoy_sockets']=['FAR_TABLE','LOFT_POST']
    ps['P04']['negative_case']+=' FAR_TABLE và LOFT_POST đều phải solve được bằng cover tương ứng; NEAR_HATCH sai. Không bắt hoàn tấtP03 để lấyM01.'
    ps['P06']['depends_on']=[]
    ps['P06']['items']['inputs']=[]
    ps['P06']['scene']='CH02.hanh_room.wardrobe; vào qua cửa bịxóa từsân và bệShared bêntrong ngay từentry. ChìaP05 chỉ mở shortcutREAL; không khóa độcquyền phòng. Ba thanhtrượt và vạchđo theo catalog.'
    ps['P06']['layout']=ps['P06']['scene']
    ps['P06']['actions'][0]='enter_erased_room_from_yard'
    ps['P07']['depends_on']=['P05','P06']
    ps['P07']['solution']['required_evidence']=['E03']
    ps['P08']['depends_on']=['P06']
    ps['P09']['reasoning']['payoff']['callbacks']=['P10']
    ps['P11']['depends_on']=[]
    ps['P11']['scene']='CH03.gauge_room.panel cùngbờA, lối vào từbến khôngqua cầuP10; vếtbùn trên tường phòngmáy cũng ởbờA. Console ba kim1/2/3, reset[1,1,1], sơđồvan liênkết. ĐènP09 và console cóthể khảo sát theo hai thứtự.'
    ps['P11']['layout']=ps['P11']['scene']
    ps['P10']['depends_on']=['P09','P11']
    ps['P12']['depends_on']=['P10','P11']
    ps['P16']['depends_on']=['P14']
    ps['P16']['solution']['accepted_paths']=[['CLASS3A','LIBRARY','REAR_GATE'],['CLASS3A','UPPER_GALLERY','REAR_GATE']]
    ps['P16']['solution']['water_conditions']={'LIBRARY':[0],'UPPER_GALLERY':[0,1,2]}
    ps['P16']['scene']+=' UPPER_GALLERY là hànhlangcao cócửanối3A→gallery→REAR_GATE; nhìnthấy từbệan toàn, không leo/nhảy. Bảng nước cho xembeat0/1/2.'
    ps['P16']['layout']=ps['P16']['scene']
    ps['P16']['hints'][2]='Beat0 có thể đi3A→thưviện→cổngsau; sau crossingđầu dùng3A→gallerycao→cổngsau. Cảhai tránh sânthấp và cầnchìacổng.'
    ps['P19']['depends_on']=[]
    ps['P19']['scene']='CH05.study.anchor_model vànhậtkýthường mởtừentry, không cầnkínhP18. Mẫu chứngthực giấy đi kèmcho kiểm nguồn khi chưa giảiP17. Năm cụmH01..H05 đãthu hồi, H06/H07active.'
    ps['P19']['layout']=ps['P19']['scene']
    ps['P19']['reasoning']['local_reteaching']=['K_AUTH']
    ps['P18']['depends_on']=['P17','P19']
    ps['P20']['depends_on']=['P18']
    ps['P24']['depends_on']=['P22']
    ps['P25']['depends_on']=[]
    ps['P26']['depends_on']=[]
    ps['P27']['depends_on']=['P25','P26','P04','P08','P12','P16','P20','P24']
    ps['P28']['depends_on']=['P25','P26']
    ps['P28']['solution'].update(gate_preparation=['HOLD','OPEN'],accepted_group_orders='ANY_PERMUTATION_WITH_STATE_VALID_ROUTES',school_route_policy='LIBRARY_AT_BEAT_0_OR_UPPER_GALLERY_AT_BEAT_0_1_2',valid_plan_count=8)
    ps['P28']['hints'][2]='GIỮ rồiMỞ. Bến điHIGH_RAMP; trường qua thưviện chỉởbeat0, hoặc gallerycaoởbeat0/1/2; sân điHIGH_COURTYARDS vàcổng1→3→2. Đủ3nhóman toàn mớiTRẢ. Có thể chọn thứtự nhóm.'
    ps['P28']['persistent_fields']+=['gate_preparation','crossing_order','school_route_choice','decision_preview_state']
    ps['P28']['inference']='Chọn A/B theo cái giá đã biết, hoặc lập và điều chỉnh phương ánC: chuẩn bịcổng, đọc trạngthái nước, chọn tuyến và thứtự nhóm, xácnhận chỉsau khi đủ3nhóman toàn.'
    # Do not retain a jumpscare attached to every puzzle. New tension contract owns presentation.
    for p in puzzles:
        t=p['reasoning']['tension'];p['horror']=t['mode']+': '+t['cue']+' Lúc đọc/closeup an toàn không tăng nguy cơ; once trigger theo state.'
    write('specs/puzzle_catalog.json',puzzles)

    def rule(kid,name,teachers,optional,consumers):return dict(id=kid,rule=name,mandatory_teachers=teachers,optional_teachers=optional,consumers=consumers,hard_gate=False)
    rules=dict(design_version='3.2',research_ids=[f'RS{i:02}' for i in range(1,8)],
        policy='Knowledge and hypotheses are authoring/provenance, not collectible count or hidden read gates. Re-teach locally when branch order permits.',
        knowledge=[
            rule('K_PHASE','Chuyển cùngpose chỉ khi lớpđích còn support/không overlap; lớpđổi cả cấu trúc và thôngtin.',['P02'],[],['P03','P04','P10','P18','P20']),
            rule('K_TRACE','Dấu trên vật phải được giải nghĩa bằng ngữcảnh hoặc một nguồn độc lập.',['P03'],[],['P05','P06','P07','P08','P18','P20','P25','P26','P27']),
            rule('K_WATER','Giờ sựkiện khác giờ nước tới; độcao và thời gian toàn hànhtrình quyếtđịnh lốian toàn.',['P11'],['P12'],['P10','P12','P15','P16','P20','P27','P28']),
            rule('K_SEQUENCE','Quan hệ trước/sau xác định chuỗi, không phải vịtríicon trên hình.',['P13'],[],['P14','P15','P21','P25','P28']),
            rule('K_AUTH','Kiểm nguồn gốc bằng cảniêmliên tục và mựcthấm trước khi dùng nộidung.',['P17','P19'],[],['P19','P23','P26']),
            rule('K_HOLD_OPEN','GIỮ→MỞ→TRẢ là chức năng nhânquả; kýhiệuvàâm là hai cách biểuđạt cùngmộtluật.',['P21'],[],['P22','P24','P26','P28']),
            rule('K_IDENTITY','Cùngngười, quan hệgiađình và vai trò là các mệnhđề khác nhau, cần chứngcứ hỗtrợ.',['P07'],[],['P23']),
            rule('K_CAUSAL','Hai sựkiện liênquan không mặc nhiên là nguyênnhân; dùng thứtự và cơchế để phânbiệt.',['P15'],[],['P19','P23','P24','P28']),
            rule('K_SOUND','Knocker điều tra nguồn âm thực và lastseen, không biết player xuyênphase.',['P14'],['P04'],['P22'])])
    write('specs/gameplay_reasoning.json',rules)
    write('specs/deduction_models.json',dict(design_version='3.2',scope='FINITE_AUTHORING_FIXTURES_NOT_RUNTIME',
        P05=dict(people=['MOTHER','SON_A','HANH','SON_B'],directions=['north','east','south','west'],constraints=['mother opposite south courtyard door','HANH opposite MOTHER','SON_A east']),
        P12=dict(arrival_minutes=124,options=[dict(id='LOW_PIER',walk_minutes=3,flood_minutes=120),dict(id='REED_BANK',walk_minutes=3,flood_minutes=123),dict(id='HIGH_RAMP',walk_minutes=3,flood_minutes=140)]),
        P17=dict(letters=[dict(id='A',seal_continuous=True,ink_bleed=True),dict(id='B',seal_continuous=True,ink_bleed=True),dict(id='C',seal_continuous=True,ink_bleed=True),dict(id='D',seal_continuous=False,ink_bleed=True),dict(id='E',seal_continuous=True,ink_bleed=False)]),
        P16=dict(edges=[['CLASS3A','LIBRARY'],['LIBRARY','REAR_GATE'],['CLASS3A','UPPER_GALLERY'],['UPPER_GALLERY','REAR_GATE'],['CLASS3A','SHORT_YARD']],blocked_edges=[['CLASS3A','SHORT_YARD']]),
        P04=dict(valid_decoy_sockets=['FAR_TABLE','LOFT_POST'],invalid_socket='NEAR_HATCH',invariant='Sound source pulls investigate away from hatch and authored cover remains connected; verify real nav/perception at runtime.')))
    write('specs/ending_c_decisions.json',dict(design_version='3.2',scope='AUTHORED_DECISION_MODEL_NOT_RUNTIME',groups=['GROUP_FAMILIES','GROUP_SCHOOL','GROUP_RIVERSIDE'],
        water_beats=[0,1,2,3],advance_event='GROUP_CROSS_COMMITTED',advances_while_reading=False,
        school_routes={'LIBRARY':dict(path=['CLASS3A','LIBRARY','REAR_GATE'],safe_at_beats=[0]),'UPPER_GALLERY':dict(path=['CLASS3A','UPPER_GALLERY','REAR_GATE'],safe_at_beats=[0,1,2])},
        gate_preparation=['HOLD','OPEN'],gate_finish='RETURN',valid_plan_count=8,
        preview='Show current and next beat, route closure, waiting groups and reversible decisions before committing. No real-time countdown.',
        on_wrong='Restore pre-decision checkpoint, retain already safe groups/E/M and give reason. Never force endingB.',
        final_c='main_ready AND all_memories AND route_plan_ready AND exactly_three_unique_groups_safe AND evacuation_route_validated AND explicit_return_confirmation',
        a_b='main_ready; neither optional plan nor trial completion required'))
    chapters=read('specs/chapter_catalog.json')
    questions=[
        'Vì sao Minh nhớ một ngôi nhà mà cảlàng phủnhận?',
        'Ai đãsống trong cănphòngtrống và vìsao thói quen vẫn giữ chỗ cho họ?',
        'Làng từng ngập đến đâu và một đườngthoát phải được đánhgiá thế nào?',
        'Lịch sử nào đãbị xóa, và hồsơ nào đủ để bácbỏ lời kể hiện tại?',
        'Mẹ đãduy trì điều gì trong15năm và nguồn nào cho biết cái giá?',
        'Ngườiởtháp là ai, cóquan hệ gì với Minh, và chuông thực sự vận hành ra sao?',
        'Người chơi sẽ dùng hiểu biết này để xử lý mónnợ và chuẩn bị cứu người thế nào?']
    bonding=[
        'Minh lắp lại đồ mẹ chuẩn bị; có thể dừng xem nét sửađèn, không thêm quest.',
        'Bà Liên nhờ đặt bátởsân; hànhđộng nhỏ dùng cùng prop, lời nói thayđổi sau khi xácnhậnHạnh.',
        'Giúp ôngPhúc kiểm dâybuộc ởbến; sau đó ông chỉvào tuyến người chơi đã chứngminh.',
        'BácTư giữ một bài tập không tên; khi phục hồi buổihọc, ông sửa lại ghế chứ chưa nhớtất cả.',
        'Tựlật các trang mẹ viết lại, đủkhoảnglặng để thấy sựkiệtsức; không fullvoice.',
        'CuộcgặpAn có quyềnđợi/xem lại chứngcứ trước xácnhận; không timer buộc bấm.',
        'Những nhóm đại diện có người/đồ quen từchương trước; nhóm đangđợi có caption, không chỉicon.']
    for i,c in enumerate(chapters):
        c['design_version']='3.2';c['investigation_question']=questions[i];c['bonding_beat']=bonding[i]
        c['investigation_graph']=dict(puzzle_dependencies={p['id']:p['depends_on'] for p in puzzles if p['chapter']==c['id']},
            observation_order='Independent room/prop observations may be gathered before puzzle commit; show an intelligible lead for each branch.',
            shortcut='Open a persistent return route after the chapter choke point; never bypass phase safety.')
        c['tension_policy']='One authored intense encounter at most in CH01(optional),CH04,CH06; CH07 uses decision pressure. CH02/CH03/CH05 use anticipation/reflection without chase.'
    write('specs/chapter_catalog.json',chapters)
    route=read('specs/evacuation_route.json');route['decision_model']='specs/ending_c_decisions.json';route['valid_plan_count']=8
    write('specs/evacuation_route.json',route)
    # Existing save layout stays the same; explicit design version prevents reinterpreting changed puzzle semantics.
    schema=read('specs/schemas/save.schema.json');schema['properties']['design_version']['const']='3.2';write('specs/schemas/save.schema.json',schema)
    fixture=read('specs/fixtures/save_empty_CH01.json');fixture['design_version']='3.2';write('specs/fixtures/save_empty_CH01.json',fixture)
    write('specs/design_migration_v31_to_v32.json',dict(from_version='3.1',to_version='3.2',ids_preserved=True,affected=['P04','P06','P07','P08','P10','P11','P12','P16','P18','P19','P20','P24','P26','P27','P28'],policy='No blind solved-flag migration. No produced campaign saves at design change. Keep originals and reject unsupported import; migration needs separate verification before support.'))

    # Retarget future tasks only and add four concrete production tasks.
    td={t['id']:t for t in plan['tasks']};sd={s['id']:s for s in plan['stories']}
    template=td['T-070210']
    additions=[
        ('T-070211','ST-0702','S07','Provenance và giả thuyết có liên kết giới hạn',['scripts/evidence/hypothesis_controller.gd','tests/evidence/hypothesis/'],['T-070209'],
         'P07/P15/P17/P19/P23 nhận draft/typedlinks có nguồn; không NLP và không28proofboards. Feedback theo nhóm mâu thuẫn, không per-slot oracle; đúngđápánkhông bị hidden-read gate; save/reload draft và chapter spoiler guard.'),
        ('T-070212','ST-0702','S07','Nhánh khảo sát có mục tiêu và preview thao tác',['scripts/interaction/action_preview.gd','tests/integration/inquiry_routes/'],['T-070211'],
         'Theo thought_path/observation_routes từngcard; cluepins cho hỏi/so/đọc lại, không auto-solve. Hai đường quan sát hợp lệ và alternate valid actions không bị ép walkthrough; range/phase/LOS vẫn bắtbuộc; branch leads và shortcut nhìn thấyđược.'),
        ('T-080405','ST-0804','S08','Kiểm chứng anticipation và hai tuyến mồiP04',['data/encounters/CH01.json','reports/S08/tension_routes.md','tests/encounters/'],['T-080404'],
         'P04FAR_TABLE/LOFT_POST đều khảdụng qua cover thực; NEAR_HATCH sai córecovery. Cue trướcWarn, perception không xuyênphase; closeup safe boundary và Chasereject; mộtscarekhônglặp. Ghi rendered route/state/caption, không dùng staticmodel thaynav.'),
        ('T-250205','ST-2502','S25','Decision model sơ tán theo trạng thái và tám kế hoạch',['scripts/endings/evacuation_decisions.gd','tests/endings/decision_plans/'],['T-250201'],
         'HOLD→OPEN trước chuyển nhóm; cả6thứtự nhóm hỗtrợ; thưviện chỉbeat0/gallerycao beat0..2 tạo8planhợp lệ. Crossingcommit mới tăngwaterbeat; preview/nước/pause/save/replan đúng. RETURN sớm từchối, sai giữnhómđã antoàn, finalCchỉsau3nhóm; A/Bkhôngcầntrial.')]
    new_ids=[]
    for tid,sid,wave,title,outputs,deps,goal in additions:
        t=copy.deepcopy(template);t.update(id=tid,story=sid,sprint=wave,title=title,goal=goal,outputs=outputs,
            acceptance_criteria=[goal],depends_on_tasks=deps,dependencies=[],
            evidence_path=f'reports/tasks/{tid}/evidence.json',review_path=f'reports/tasks/{tid}/review.md',
            read_before=['AGENTS.md','04_TECHNICAL_EXECUTION_CONTRACTS.md','14_PUZZLE_DESIGN_BIBLE.md','docs/decisions/ADR-003-reasoning-and-tension.md','specs/gameplay_reasoning.json','specs/ending_c_decisions.json',f'stories/{sid}.md'])
        t['implementation_steps'][1]=goal
        t['required_capabilities']=list(dict.fromkeys(t['required_capabilities']+['gpu_render']))
        plan['tasks'].append(t);sd[sid]['tasks'].append(tid)
        state['tasks'][tid]=dict(status='NOT_STARTED',executor_id=None,evidence=None,blocker=None,notes=[],updated_at=None);new_ids.append(tid)
    td['T-070210']['depends_on_tasks'].append('T-070212')
    td['T-250202']['depends_on_tasks'].append('T-250205')
    for t in plan['tasks']:
        if state['tasks'][t['id']]['status']!='NOT_STARTED':continue
        for sid in t.get('dependencies',[]):
            if sid!=t['story'] and sid in sd:
                t['depends_on_tasks']=list(dict.fromkeys(t['depends_on_tasks']+sd[sid]['tasks']))
        wave=int(t['sprint'][1:])
        if wave in [7,8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]:
            for rel in ['docs/decisions/ADR-003-reasoning-and-tension.md','specs/gameplay_reasoning.json']:
                if rel not in t['read_before']:t['read_before'].append(rel)
            t['acceptance_criteria'].append('Gameplay3.2: triển khai thought_path, hai observation_routes, feedback không per-slot oracle, knowledge provenance/callback và tension của card liên quan; không dùng solved flag để kết luận người chơi hiểu/thích.')
    for s in plan['sprints']:s['tasks']=[tid for sid in s['stories'] for tid in sd[sid]['tasks']]
    for req in plan['requirements']:
        if req['id']=='R06':req['acceptance']+=' Gameplay3.2 có hypothesis/refutation, nhánh quan sát hội tụ và tái vận dụng kiến thức; thông tin thu không là hidden read gate.'
        if req['id']=='R09':req['acceptance']+=' Anticipation/commitment/aftermath theo scene; không spam scare hoặc capture trong safe closeup; thử được cả hai mồiP04.'
        if req['id']=='R02':req['acceptance']+=' P28 có8planhợp lệ và replan theo beat; plan,trial,validation,finalcommit tách rõ.'
    for g in plan['gates']:
        if g['id']=='G2':g['criteria']+=' Kiểm hai lộ trình quan sát, hai mồiP04, reasoning feedback, cue/recovery và không hidden-read gate; difficulty/appeal chưa có người thật ghi NOT_ASSESSED.'
        if g['id']=='G4':g['criteria']+=' Cả8plan sơtán hợp lệ và các route bịngập đúngbeat; callback nguồn cũ được dùngthật, không chỉ dẫn thoại.'
    plan['meta'].update(version='3.2',design_revision='ADR-003',task_count=len(plan['tasks']))
    state.update(plan_version='3.2',revision=state['revision']+1)
    assert all(state['tasks'][k]==v for k,v in original_state['tasks'].items())
    assert state['gates']==original_state['gates']
    write('plan/backlog.json',plan);write('state/task_state.json',state)
    write('reports/design/v32/migration.json',dict(scope='DESIGN_MIGRATION_NOT_RUNTIME',new_tasks=new_ids,existing_task_states_preserved=True,gates_preserved=True,task_count=len(plan['tasks']),revision=state['revision']))
    print('Authored3.2 reasoning for28puzzles; physical branches and4new tasks defined; no runtime completion.')


if __name__=='__main__':main()
