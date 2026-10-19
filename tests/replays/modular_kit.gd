extends SceneTree

var checks: int = 0
var failures: Array[String] = []
var captures: Array[String] = []

func _init() -> void:
	call_deferred("_replay")

func _check(ok: bool, label: String) -> void:
	checks += 1
	if not ok: failures.append(label)

func _capture(name: String) -> void:
	for frame in range(4): await process_frame
	await RenderingServer.frame_post_draw
	var path: String = "res://reports/tasks/T-020302/" + name + ".png"
	_check(root.get_texture().get_image().save_png(path) == OK, "capture " + name)
	captures.append(path)

func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var scene: Node3D = load("res://scenes/environment/modular_kit_scene.tscn").instantiate()
	root.add_child(scene)
	var rig: CameraRig = scene.get_node("CameraRig")
	var player: CharacterBody3D = scene.get_node("Player")
	for tick in range(30): await physics_frame
	for kit: StreetBlockout in scene.get_node("Modules").get_children():
		_check(kit.initialization_error.is_empty() and kit.global_basis.determinant() > 0.999, str(kit.name) + " imported positive-transform colliders")
	var gameplay: CameraPreset = rig.snapshot_preset()
	for erased in [false, true]:
		for kit: StreetBlockout in scene.get_node("Modules").get_children(): kit.apply_preview_palette(erased)
		var prefix: String = "ERASED" if erased else "REAL"
		_check(rig.apply_preset(gameplay), "gameplay camera")
		await _capture(prefix + "_gameplay")
		var front: CameraPreset = gameplay.duplicate()
		front.offset = Vector3(0, 4.5, 18)
		front.look_offset = Vector3(0, 1.2, -1)
		_check(rig.apply_preset(front), "front camera")
		await _capture(prefix + "_front")
		var wide: CameraPreset = gameplay.duplicate()
		wide.fov_degrees = 45
		wide.offset = Vector3(12, 10, 19)
		_check(rig.apply_preset(wide), "wide camera")
		await _capture(prefix + "_wide")
	for kit: StreetBlockout in scene.get_node("Modules").get_children(): kit.apply_preview_palette(false)
	Input.action_press("move_forward")
	for tick in range(120): await physics_frame
	Input.action_release("move_forward")
	for tick in range(30): await physics_frame
	_check(player.position.z < -3.5 and player.is_on_floor() and absf(player.position.y) < 0.003, "real capsule traverses assembled open doorway")
	var inspection: CameraPreset = gameplay.duplicate()
	inspection.offset = Vector3(0, 2, 8)
	inspection.look_offset = Vector3(0, 1, -3)
	_check(rig.apply_preset(inspection), "door inspection camera")
	await _capture("door_passed")
	_check(RenderingServer.get_current_rendering_method() == "forward_plus", "actual Forward+ renderer")
	var report: Dictionary = {"result": "PASS" if failures.is_empty() else "FAIL", "assertions": checks,
		"failures": failures, "captures": captures, "player_after_entry": str(player.position),
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(),
		"phase_scope": "Shared geometry with REAL/ERASED material previews, not WorldController phase switching",
		"input_mode": "synthetic_actions_real_controller", "quality_state": "BLOCKOUT", "software": true}
	var file := FileAccess.open("res://reports/tasks/T-020302/runtime.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "  "))
	file.close()
	print("MODULAR_RENDER_REPLAY ", JSON.stringify(report))
	quit(0 if failures.is_empty() else 1)
