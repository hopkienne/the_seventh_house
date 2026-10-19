# T-020104 — Movement QA / baseline 3.2

Status: VERIFIED for functional movement; self-review=true. Ledger closure is separate.

Tested source HEAD base `2498ad4bd768b3b6d5c252ecf851fa0b211d30ea`, dirty tree preserved. Candidate `20261019T071623400900Z`; runtime source SHA256 `47f5515c46e925128e5d0637cbbc4fa1e54ba834003418f21be4c72ec20e8209`. Engine 4.7.2.stable.ed1daf0bf, Windows host, Forward+ / Vulkan / SwiftShader Device (Subzero), synthetic Input actions. See ../tasks/T-020104/baseline_sources.json for current design fingerprints.

## Reconciliation

Current baseline: 28 puzzles, 21 required + 7 secret, 8 valid C plans. Four added tasks remain NOT_STARTED behind their original dependencies/gates. Existing production implements movement/bootstrap only; no campaign puzzle or SaveService was ported from old answers. DESIGN is not IMPLEMENTED. Closed task evidence and owner design changes were preserved. This QA changes fixtures/runner only, no player/world/story/save authority. G0 remains historical; no gameplay gate is advanced.

## Results

| Case | Observed | Result |
| --- | --- | --- |
| Slope 20 degrees | Up/down, grounded; upper y=2.052975 m; idle on slope and landing stable <2 mm | PASS |
| Slope 40 degrees | Up/down, grounded; upper y=3.856897 m; idle on slope and landing stable <2 mm | PASS |
| Interrupted / new scene | Input lock stops; new scene Idle and responds | PASS |
| Four walls / diagonal corner | Existing actual StaticBody collisions retested in candidate | PASS |
| Registered engine suites | 21 cases / 180 assertions, failed=0, skipped=0 | PASS |
| Export / pack | Windows EXE + PCK; pack allow/exclude inspection | PASS |
| Headless rendered replay request | Rejected with exit 2 | PASS |
| Diagnostic slope movie | 132 actual MJPEG frames, 1280x720, 30 movie FPS, 4.4 seconds; start/mid/end decoded and reviewed | PASS |

Live comparison, 160x90 window, 120 physics ticks warmup then 300 held ticks per profile, physics=60 Hz. Measurement uses frame_post_draw count / monotonic elapsed time, no fixed-fps or Movie Maker. Final comparison ran alone, after other engine jobs stopped.

| Case | Observed drawn FPS | Distance m | Result |
| --- | --- | --- | --- |
| FPS-30 | 30.000366 | 10.816677094 | PASS |
| FPS-60 | 60.002220 | 10.816677094 | PASS |
| FPS-120 | 119.800006 | 10.816677094 | PASS |

Distance spread = 0.0; allowed <5%. Each profile reached requested rate within the predeclared 10% tolerance and ended grounded. These rates establish functional integration at this QA resolution, not retail performance or minimum hardware.

Initial 320x180 probe: 29.917 / 59.898 / 75.427 observed FPS. 120 FPS NOT_TESTED there; retained fps.json and logs, never relabeled PASS. An additional concurrent diagnostic run is archived under contended_probe and excluded from acceptance. Software driver warned VSYNC_DISABLED unavailable; actual draws were measured despite its fallback. Do not infer screen scanout rate from draw submissions.

Initial slope assertion failed because its hardcoded x>3.1 exceeded the 40-degree landing edge. Reviewed actual height/pose: no production defect; corrected criterion to authored edge + capsule radius. Initial failing logs retained. No production bug was reproduced; diagnostic movie shows the verified traversal rather than a fabricated failure.

## Reproduce

From repository root, pinned helper tools.godot_process.run validates executable SHA256 before every invocation. Raw stdout/stderr paths and build command records are under reports/tasks/T-020104/ and reports/builds/20261019T071623400900Z/.

- `python -X utf8 scripts/build_windows.py` (all registry suites, import, export, package inspection).
- Pinned Godot `--headless --path . --script res://tests/test_runner.gd -- --suite movement_qa`.
- Using process-scoped software ICD helper: `--resolution 160x90 --script res://tests/replays/movement_fps.gd`. Outputs are dedicated QA paths; archive an earlier run before repeating.
- Using the same helper: `--resolution 640x360 --write-movie <repo>/.qa/T-020104/slope_diagnostic.avi --fixed-fps 30 --script res://tests/replays/movement_clip.gd`. Movie Maker encodes at project override 1280x720; window PNG is640x360. Movie timing is diagnostic only.

## Limits

1080p hardware FPS, physical keyboard/gamepad, audio listening, camera cuts, switching, production stairs, campaign/save/puzzle usability are NOT_TESTED here. Sharp riser climbing is not claimed; supported surfaces tested are continuous20/40degree ramps below capsule45degree limit. Human usability remains HUMAN_USABILITY_NOT_ASSESSED. Native exported executable was built and pack-checked but not separately rendered in this task. No FINAL art or full-game completion claim.
