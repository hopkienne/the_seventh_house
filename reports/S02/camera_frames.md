# T-020204 — Camera safe frames / gameplay baseline3.2

IMPLEMENTED and VERIFIED for reusable framing/layout. Task ledger closure separate. Reviewer codex-primary, self_review=true.

## Policy and implementation

Authored1920x1080, canvas_items, explicit keep-aspect. The content stays16:9;16:10 uses letterbox and21:9 pillarbox rather than widening camera view beyond the set. SafeFrame MarginContainer and SafeFrameSettings Resource reserve5percent on all sides. Accepted settings are copied; invalid/null settings reject without changing layout. Main scene integrates the reusable container; this task does not claim complete menu/settings/journal/localization flows.

## Actual tests

| Window | Zone samples | Actual content capture | Expected window padding, calculated |
| --- | --- | --- | --- |
|1280x720,16:9|WEST/EAST|1280x720|none|
|1280x800,16:10|WEST/EAST|1280x720|40px top/bottom|
|1680x720,21:9|WEST/EAST|1280x720|200px left/right|
|1280x720 restored|WEST/EAST|1280x720|none|

Source replay50assertions/0failures: actual input crosses both Area3D zones for each ratio, feet/head and clue diagonal corners stay inside safe rect; UI label rect fully contained; captures saved; KEEP enum1 and real Forward+ checked. Logical viewport remains1920x1080; safe rect x96..1824/y54..1026. UI rect x96..1824/y493..586 for the QA label. Each sample logs actual window and content sizes, projection coordinates and zone in reports/tasks/T-020204/runtime.json.

The viewport PNG excludes OS-managed bars. Padding values above are calculated from measured window/content dimensions, not a captured desktop/border measurement. Camera3D projection and Control bounds are tested in matching logical viewport coordinates. Inspected ratio captures show readable Vietnamese/English test labels and player/clue visible. Same-zone content-image comparison after resize has maximum mean absoluteRGB change0.0000065104/255, maximum single-channel difference1; no reframe/stretch from extra aspect. Raw metrics image_comparison.json. This measures resize consistency, not aesthetic/human usability.

Unit suite safe_frame2cases7assertions PASS: explicit policy, container, child bounds, invalid margin/null rejection, previous layout preserved. Test-first missing-container failure retained. Candidate all33cases246assertions,0failed/0skipped, import/export/package inspection PASS. No scenes/tests or planning/report files in PCK.

Clean native Windows smoke: hash-matched EXE/PCK copied to .qa/T-020204/native and launched outside editor/source with --resolution1680x720. Actual window1680x720, capture1280x720, authored1920x1080, KEEP1, Windows/Forward+/Vulkan/SwiftShader,5assertions PASS. Native capture opened. This confirms exported configuration; native screenshot is still content-only.

## Candidate and reproduction

Build 20261019T074605916708Z; runtime source SHA256 d79b9e4a69634f058ad9644ae9acbd0b074562adc61a36a906a6ead194685be5. Manifest/raw per-suite logs: reports/builds/20261019T074605916708Z/manifest.json. Binary hashes are recorded in that manifest and task evidence.

- python -X utf8 scripts/build_windows.py
- Pinned Godot --headless --script res://tests/test_runner.gd -- --suite safe_frame
- tools.godot_process.run(['--script','res://tests/replays/camera_frames.gd'],timeout=180,software=True), process-scoped test-only SwiftShader ICD.
- ExportedEXE --resolution1680x720 -- --qa-profile BOOTSTRAP --qa-report res://reports/native_ultrawide.json, cwd clean binary directory. Never add --path to this release template.

## Limits

Functional software render only;1080p hardware performance, physical input/hotplug/audio and human usability NOT_TESTED. UI evidence covers the reusable container with a QA label, not future full menus or large-text LQA. QA scene is excluded from retail. Camera letterbox does not implement CinematicDirector. Campaign puzzles/save/endingC remain DESIGN_ONLY; design validators do not make a runtime gate PASS. Prior owner changes and closed evidence preserved; no gate advanced.
