# Content contracts

Baseline3.2: chapter_catalog has7chapters; puzzle_catalog has28designs (14CORE+7mandatorySUPPORT+7SECRET,21 main-required); evidence_catalog has28stablejournalIDs, independent of puzzle count. M01..M06 come from secret puzzles, M07 from P25main. evacuation_route defines seven connected edges and discoverable north/port marks. P27 produces a plan; P28 validates three groups before final C.

Schemas and static checks validate authoring consistency only. Fixtures are small examples, not playable campaign or real saves. No runtime puzzle/content completion is implied. Use `python tools/render_puzzle_cards.py` after editing catalogs; use `python tools/validate_puzzle_design.py` for semantic design checks. Read Puzzle Design Bible and ADR-002. ID migration3.0→3.1 is not blind save-flag remapping; historical catalogs remain under history/.

Gameplay 3.2 hiện hành theo ADR-003: xem `docs/design/comparative_gameplay_research_v32.md`, `docs/design/puzzle_depth_matrix_v32.md` và reasoning trong catalog/cards. 28 puzzle/21 main-required/7 secret và28 journal IDs giữ nguyên. Định nghĩa602 task, trạng thái chỉ ởledger. Kiểm reasoning/routes/tension riêng, không coi tài liệu hoặc finite model là runtime/human playtest.
