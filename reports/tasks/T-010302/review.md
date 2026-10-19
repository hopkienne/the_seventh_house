# Review T-010302
Result: PASS. Reviewer: codex-primary; self_review=true, separate source/log/render review.

Scene has Node3D, active perspective Camera3D/FOV38, DirectionalLight3D, environment and Shared-layer collision floor. Main scene registered for F5. 11 actions persist in project.godot with physical A/D/W/S/Shift/E/Q/J/Esc/H/F3 and pad bindings; built-in UI actions preserved. 3 scene cases/57 assertions pass, including actual InputMap event matching, negative unmapped key/pad and scene instantiate/free/reload without leaked nodes. Bootstrap regression remains 2 cases/21 assertions plus expected-negative harness paths.

Rendered smoke ran non-headless on Windows via explicit SwiftShader CPU Vulkan, actual Forward+, 1280x720, 14 sampled colors, 5 assertions, no stderr. Opened PNG: floor/reference column and directional shadow visible, no blank image. This is an engine bootstrap scene, not player movement/campaign/final art. No physical input or native GPU performance claim.

Failure mode found and resolved: main scene initially interpreted test-runner --suite arguments as malformed QA and called quit during suite execution. Main now opts into QA only when QA flags exist. Raw before/after preserved; final suite has empty stderr. Invalid profile, headless render and out-of-scope report path all exit 2 without writing forbidden files. Report path parameter added to bootstrap verifier so later regression runs cannot overwrite closed task evidence. No unresolved acceptance issue for this bootstrap task.
