# G0 — Baseline technical acceptance

Reviewer recommendation: PASS cho G0 bootstrap; self_review=true, reviewer codex-primary. Task/gate được ghi qua agentctl sau evidence review, không sửa state trực tiếp. Đây không phải Full Game, final art/audio hoặc release approval.

## Candidate và scope

Commit source snapshot: `5fb6d50defa62f0f66b7811c348853b76c96665d`. Build `20261019T040053405815Z`, runtime source SHA256 `e2644d93f1c34e2aab3407a3682da39fa787b5d3152ead36206e15e5ad53e1bf`; helper source_hash đã xác nhận candidate khớp runtime source hiện tại. Artifact build có manifest/raw logs; không dùng commit cũ để ký source mới.

Scope digest từ catalog và docs/product_scope.md: 7 chương/7 nhà, 14 puzzle, 7 memory, 28 journal records và A/B/C Must; giữ save/recovery, VI/EN, keyboard/gamepad, Windows x64, final assets/audio. Scope file SHA256 `21faf27a6ebd475485e0e0957e63ea5bb651985c7b3a249a9e650bfae8117fcc`. Runtime content vẫn PARTIAL,0/7 chapter,0/14 puzzle,0/28 records,0/3 ending; đây là đầu vào sản xuất tương lai, không nghiệm thu nội dung tại G0.

## Evidence được đối chiếu

- Toolchain: Godot4.7.2.stable.official.ed1daf0bf; editor và matching templates tải thật/official SHA256, version.txt4.7.2.stable, Windows template hashes trong lock.
- Four registered engine suites chạy trước export: bootstrap21 + scene57 + utilities6 + asset_import29 =113 assertions,11 cases,0 failed/skipped. Negative assertion/unknown suite/zero tests/bad arguments/invalid Callable có explicit nonzero FAIL, không đóng PASS từ parser/import-only.
- Plan validation PASS; ledger22, data-validator6, build-process5 tests PASS. Runtime data validator PARTIAL1 produced file; --require-complete đã fail đúng. Không ghi toàn bộ game content PASS.
- Actual EXE/PCK export và empty-project pack inspection PASS: có runtime JSON/main scene; không tests/tools/planning/reports/host config/build cũ trong paths đã kiểm. Clean checkout baseline và EXE smoke đã chạy ở T-010304, tracked source diff0; PCK bit identity chưa xác lập.
- Native candidate EXE/PCK vừa copy sang thư mục mới .qa/g0_smoke/20261019T040053405815Z/ rồi chạy trực tiếp ngoài editor trên Windows. Actual Forward+/Vulkan/SwiftShader CPU,5 smoke assertions,0 failed/skipped,1280x720 capture,14 sampled colors,exit0,empty stderr. Không thay headless cho native/frame.
- EXE SHA256 `2160d4ed2cc9b3ef9ef2827dafb826b2b34a2ff34387ff0c706e0f255b590497`; PCK SHA256 `2cb91f6d3d14534b339f937c8d2b525189fe9ac32eca4335387ea0624a84542e`. Capture SHA256 `de27712f9053c7ffadc102b8b86aa6a2bed01e94a0c19df4c5b0e91979a1be85`.
- Static GLB được tạo/import/render/rebuild thật, vẫn BLOCKOUT; report gaps rig/custom shader/navigation/profiling tại reports/S01/skill_spike.md. Agent-owned art/audio paths và risk/permission queue có thật, không cần freelancer.

## Review findings và giới hạn

Các lỗi đã có regression: renderer auto fallback dù exit0, root CSV import warnings, runtime-data filter quá rộng, build-manifest leak, main QA hiểu nhầm suite args, provider Callable bị giải phóng. Latest candidate suites/package/native smoke pass; không hạ validator hoặc gate để qua lỗi.

Native NVS310 hardware Forward+ không chạy; functional render dùng software explicit process-only theo ADR-001. Hardware performance, physical pad/hotplug/keyboard và audible mix NOT_TESTED; CAP-001 OPEN cho task/gate cần chúng. Rig/animation/custom phase shader/navigation và campaign systems chưa implement; không dùng G0 ký thay future acceptance.

Scope/capabilities/permission defaults/import/export/native bootstrap đủ tiêu chí G0. Paid spend0,publishfalse,không remote/push/upload/legal signature. HUMAN_USABILITY_NOT_ASSESSED. Reviewer pass của cùng agent, không độc lập. G1…G9 vẫn NOT_EVALUATED; không TECHNICALLY_COMPLETE, READY_FOR_RELEASE hoặc PUBLISHED.
