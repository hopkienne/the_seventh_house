# Gameplay3.1 verification and self-review

Review mode: self_review=true. Scope: owner-requested design migration, not runtime game implementation. No independent reviewer or human playtest claimed.

## Changes verified

- 28 puzzle cards and7chapter cards rendered from canonical catalogs;14CORE+7SUPPORTrequired+7SECRET;21main-required,28journalIDs distinct.
- Located clues, inference, item sources/recipes, action sequence, solutions, partial state, hints, horror triggers and negative/access/revisit cases authored.
- Backlog3.1:598tasks, six new system tasks NOT_STARTED. Existing task states/gates preserved by migration assertion; T-020104 remains IN_PROGRESS. No task finished or gate passed in this session.
- G2 now requires completeCH01P01–P04; S25 is audit/polish, not delayed puzzle production. Future chapter task scopes include all four puzzles.
- P27 plan/P28 trial/validation/final conditions separated, M07 fromP25, school key sourceP16, reusable reflector/lantern/decoy recovery defined.
- Provenance corrected: E08 includes blank school register afterP15 safe, E10 includes mother’s page afterP19; P23 no longer relies on unstated facts.
- Old-ID migration explicitly does not blindly rename solved flags. Save schema now requires design_version3.1; old/unversioned save fixtures rejected by validator tests.

## Actual checks

Final commands and raw output: final_checks.json and final_check_1..10.log.
Plan validation PASS:36waves/146stories/598tasks/7chapters/28puzzles/28records.
Static puzzle consistency PASS:278checks including DAG, reward sources, roles, unique linked-valve solution and map north marks.
9design regression tests,8runtime-data-validator tests,22ledger helper tests PASS. Narrative authoring81checks PASS.
Runtime-data result is PARTIAL, not PASS:0/28puzzles produced. No engine/gameplay/rendered campaign/native input/audio/physical pad/human usability tests run here. No game source diff under scripts/scenes/project.godot.

Excel: edited with bundled artifact-tool, recalculated;598tasks/19DONE read from actual ledger, native tables extended to include new rows;12sheet names and native feature counts preserved. Before/after Content preview viewed. Formula scan has no errors. Native Excel execution NOT_TESTED. HTML/CSV/requirements regenerated from canonical sources.

## Findings corrected during review

Initial validator found4reward source mismatches(E04/E09/E10/E13) caused by reusing the old ID mapping despite changed reward roles; sources now derive from new rewards. Review also found missing school-key pickup and P23 evidence provenance; fixed in P16/P15/P19. Tracker initially displayed new rows outside native table; table ranges extended with guarded refresh, now AgentTasksTable A4:M602, QA A4:H47. Existing baseline task states and historical evidence were not rewritten.

## Remaining uncertainty

HUMAN_USABILITY_NOT_ASSESSED. Difficulty, pacing320minute target,55/25/15/5distribution, emotional impact and market appeal are unmeasured. Puzzle concepts still need scene/art/audio/VIEN/runtime implementation and real input replays. A/B remain meaningful costs; C is an earned alternative and may dominate once unlocked. Do not add new cost/canon silently.

## Maintenance

Edit specs catalogs, rerun tools/render_puzzle_cards.py, tools/write_requirements.py, tools/render_views.py, tools/validate_plan.py and design tests. Tracker builder is tools/update_tracker.mjs; pass the bundled artifact-tool module path from load_workspace_dependencies and run with bundled Node from repo root. Run the spreadsheet skill operation-start marker once before a new editing operation. Do not treat Excel/HTML as a second ledger.
