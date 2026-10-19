# T-020301 — street blockout review

Reviewer: codex-primary; `self_review=true`. Separate review pass after implementation, source/diff inspection and actual image inspection. Scope: baseline 3.2, ST-0203 scale blockout, not FINAL art or chapter acceptance.

Result: PASS for the task acceptance: genuine metre-scale source, 4 m corridor and a doorway that admits the actual player capsule.

## Implemented and measured

- Original Vietnamese house silhouette: pitched clay roof/ridge, plaster walls, timber posts, open doorway/leaves, slatted window facings, fence wings, bench and earthen jar. Stable asset ID `ENV_STREET_BLOCKOUT_01`, CH01, SHARED. 56 mesh objects, 732 triangles, eight PBR color materials, complete UV/normals, 45 authored static collision bodies. Static asset, no rig/animation or external images/libraries.
- Real source `art/source/blockout_street.blend` reopened in pinned Blender 4.5.3 LTS. Independent world-bounds measurement: street clear width 4.0 m, doorway 1.25 m wide and 2.25 m high. Source metric scale 1.0. Explicit GLB imports into Godot 4.7.2; `.gdignore` prevents a second automatic Blender import. Root ground pivot is at zero; imported street upper surface is Y=0.
- `scenes/environment/street_scale_scene.tscn` integrates the street prefab, existing real Player CharacterBody3D and CameraRig at 38 degrees. It is a separate playable integration scene; bootstrap main scene stays the bootstrap. Shared collision uses layer1/mask8.
- Centered capsule (height1.70 m, diameter0.56 m) walks into the house by held input and real physics: Z=-4.350001 m, feet Y=0.000855 m, grounded. Offset X=0.85 m is blocked by the jamb (Z=-2.119056 m), with natural collision deflection. Three corridor lanes at Z=-1.65/0/1.65 m remain walkable and grounded. Only initial fixture placement is authored; no teleport or pose clamp is used to pass a collision.
- Two final independent generator runs (`rebuild_c/d`) have equal complete semantic manifests and byte-identical GLB. The verified wrapper rebuild also matches. Final semantic SHA256 `ea2d5b048731d8764077e804da242216e19864d19edae85322a111b8e082cded`; GLB SHA256 `bfab705624fc0fc676e270370854423769c24cb7b5cdb342b1410255364311d3`. `.blend` serialization includes save metadata: no byte-determinism claim for Blender source.

## Findings and resolutions

1. Initial bench leg names contained punctuation sanitized by Godot, leaving only41/45 colliders. Kept the initial model and failing logs. Generator now authors sanitized stable IDs; integration fails loudly if collision IDs do not resolve, and the regression asserts both successful initialization and all45 collision bodies. This was found within the open task, not a defect in a closed task; no fabricated REWORK ticket.
2. Render review found `ambient_light_source=SKY` without a Sky resource, blacking out the interior. Corrected to COLOR with zero sky contribution. Preserved the earlier images under `initial_render/` and `pre_ambient_fix/`; final captures were rendered again and all eight opened. Roof/posts/door silhouette and material assignment are readable; frontal inspection now visibly shows the capsule inside the doorway.
3. Exterior oblique camera still correctly occludes the player behind opaque walls/roof after entry. The frontal QA inspection proves entry without hiding geometry. A completed interior cutaway/camera system is not part of this scale task and remains future chapter integration; the separate scene is not presented as a finished house gameplay route.
4. Candidate source hashing previously omitted production art. Added runtime art/export and art/materials and a regression that modifies mesh bytes at the same path; the candidate hash changes. Package inspection now requires the GLB, prefab and integration scene while retaining authoring/QA exclusions. No test validator was weakened.

## Verification and reproduction

`reports/tasks/T-020301/evidence.json` pins exact final artifacts, build ID and commands. Engine suite `street_blockout`: 3 cases, 227 assertions, zero failed/skipped. Full registry: 36 cases, 473 assertions, zero failed/skipped. Python build guard tests: 6 passed. Plan, puzzle design278 checks and puzzle depth587 checks pass only for static design consistency (28puzzles/21main-required/7secret and8evacuationplans).

Final rendered replay: 18 checks, eight 1280x720 captures, actual Forward+/Vulkan on SwiftShader Device (Subzero), Windows. Opened REAL and ERASED gameplay/front/wide, exterior door-entered and front door-entered images. Grounding/position comes from physics, not an image-only inference. REAL/ERASED are material review adapters over shared geometry, not an implemented WorldController phase switch. Native exported EXE BOOTSTRAP smoke is reported separately from source street rendering; it does not assert native campaign gameplay.

Rebuild into a NEW directory: `python -X utf8 tools/art/rebuild_street.py --output-root .qa/street_NEW_ID`. Read-only reopen: pinned Blender `--background art/source/blockout_street.blend --disable-autoexec --python-exit-code 1 --python tools/art/verify_street_blend.py`. Full import/test/export/PCK inspection: `python -X utf8 scripts/build_windows.py`. Replay: pinned Godot `--rendering-method forward_plus --rendering-driver vulkan --audio-driver Dummy --script res://tests/replays/street_blockout.gd` through `tools.godot_process.run(..., software=True)`. Wrapper installation option reviewed; final canonical files were copied from verified rebuild_c, not claimed installed through an unexecuted option.

Source and runtime hashes/provenance are in `art/manifest/blockout_street.asset.json`. Blender portable archive matches checksum lists independently retrieved from dotsrc and RWTH mirrors, binary version/hash verified. GPL applies to the local authoring tool; no Blender binary or third-party mesh/texture input is shipped. Original asset production does not authorize public publication.

## Limits

Asset quality remains BLOCKOUT. No FINAL rubric, human appeal/playtest, GPU1080p performance, physical gamepad or audible mix approval. Software rendering is functional visual evidence only; CAP-001 remains. Full chapter, puzzles/reasoning, endings, SaveService, phase switching and character rig remain outside this task. No gate is promoted. Owner baseline migration and prior uncommitted production files/evidence preserved; no reset, checkout, mixed commit or public upload.
