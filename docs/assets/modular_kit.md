# Modular street kit — T-020302

Four BLOCKOUT assets, shared geometry for CH01/the reusable street kit. They inherit Wood/Plaster PBR colors from the T-020301 palette. No external meshes, images or animation clips are inputs. Each has editable Blender source, deterministic recipe, GLB, prefab, metrics and a provenance record under `art/manifest/modular/`. Blender tool license/source pin remains `config/blender.lock.json`; the local authoring binary is not shipped. This is original project geometry, not a downloaded asset pack. Public release clearance remains a separate gate.

| Prefab in `scenes/environment/modules/` | Size | Role |
|---|---|---|
| `fence_2m.tscn` | 2 m long, 1 m high | Two posts, two rails and seven pickets; collision follows actual wood, not an invisible solid fence panel |
| `wall_2m.tscn` | 2 m long, 3 m high, 0.20 m thick | Opaque plaster wall and solid collision |
| `door_open_2m.tscn` | 2 m bay, 3 m high | 1.25 m × 2.25 m clear opening, leaves folded behind jambs |
| `door_closed_2m.tscn` | Same bay/frame | Two closed leaves block the player; decorative handles do not add colliders |

All dimensions use Godot Y-up metres. The root/pivot is the ground-left endpoint `(0,0,0)`, not the bounding-box center. `SocketStart` is `(0,0,0)` and `SocketEnd` is `(2,0,0)`, aligned to the 0.25 m placement grid. Surface details need not lie on the placement grid. In Blender, the same coordinates are converted to Z-up and exported back to Y-up. All source/import transforms use positive unit scale. Adjacent modules placed at X=0/2 meet at their sockets. For a corner, place the next root on the previous end socket and rotate Y by 90 degrees; its end points toward negative Z. Rotate by180/270 for the other directions. Never mirror with negative scale or stretch physics with nonuniform scaling; author a distinct recipe if dimensions change. Corner solid volumes can overlap inside the joint by half the wall thickness; they do not introduce a traversable slit.

Instantiate the prefabs, not just the raw GLB, when collision/sockets are required. They reuse the verified `StreetBlockout` collision integration adapter without changing its behavior: layer1/mask8, authored mesh IDs, fail-loud mismatch, mesh-derived static collision. Marker3D sockets are explicit prefab nodes; the source also includes socket empties. `apply_preview_palette()` is an art review adapter only, not the WorldController. The two door assets are static placement variants; there is no interact-to-open, animation, door save state or inventory lock in this art task.

`scenes/environment/modular_kit_scene.tscn` assembles repeated fences, wall/door bay and a90degree return, plus a reversed fence and closed door. It integrates the actual Player and38degree CameraRig on a physical floor. The bootstrap main scene stays the bootstrap. For large-scale house or interior use, author camera/occlusion/cutaway behavior in that chapter's integration task; this test assembly is not a finished chapter.

Rebuild in a NEW repository directory:

```powershell
python -X utf8 tools/art/rebuild_modular.py --output-root .qa/modular_NEW_ID
# Explicitly install regenerated source/GLB/metrics/prefabs, then reverify:
python -X utf8 tools/art/rebuild_modular.py --output-root .qa/modular_NEW_INSTALL --install
```

Canonical installation was actually exercised in T-020302. Installation updates generator-owned module files only; do not place hand edits in generated prefabs or runtime mesh files. Update manifest hashes and rerun import, physics/render verification after a rebuild. `.blend` save metadata is not byte-stable; compare semantic metrics and GLB bytes across independent runs. Read-only inspection: pinned Blender `--background art/source/modular/MODULE.blend --disable-autoexec --python-exit-code 1 --python tools/art/verify_modular_blend.py`.

Godot suite `modular_kit` checks imported bounds/normals/UV/materials, positive transforms, sockets, collision at four quarter-turn orientations, straight/corner seams and real capsule passage/blocking. Replay `tests/replays/modular_kit.gd` produces REAL/ERASED gameplay/front/wide views and a door-passage capture with synthetic input through the real controller. Evidence/review are under `reports/tasks/T-020302/`. Actual Forward+ software rendering can verify visual integration, not hardware GPU performance, human appeal or final art acceptance. These assets remain BLOCKOUT; no gate is advanced by this document.
