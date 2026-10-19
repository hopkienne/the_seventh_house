# T-020201 separate self-review

PASS; reviewer/executor codex-primary, self_review=true.

AC: FOV/offset configurable via CameraPreset Resource; main integrates reusable CameraRig/Camera3D with perspective38degree initial preset; no mouse orbit handlers. Invalid/null/NaN/opposite-side/clipping configurations reject before state mutation, previous pose/FOV retained. Two test-first failures retained; final camera suite2cases13assertions PASS. Candidate all23cases193assertions passed; import/export/PCK inspection passed. Runtime replay6checks PASS on Windows Forward+/Vulkan SwiftShader; default/tuned1280x720 PNGs opened and compared, synthetic mouse does not rotate. This is functional framing, not FINAL art/hardware performance or human usability.

Review found old art render fixture hardcoded Camera3D path after rig extraction, and capsule occluded its prop. Fixed path, hid unrelated player only in prop fixture, made capture output configurable with fresh default reports/runtime/stool.png. Initial occluded PNG retained; repeated actual renderer capture reviewed, stool visible with geometry/material/shadow. Closed T-010402 image/evidence unchanged. Tests/fixture-only fix after build cannot change exported runtime source hash. No need to change product design or add fabricated production bug.

Changed shared main scene/bootstrap and scene tests only for rig integration. Existing physics/input/locomotion/corridor/movement QA all passed in candidate. Follow/deadzone/smoothing/zone transitions/aspect remain tasks020202..204; not claimed done here. No story/world/save authority or puzzle answers changed. Baseline3.2 and gate constraints unchanged.
