extends SceneTree

var failures: Array[String] = []
var checks: int = 0
var captures: Array[String] = []

func _init() -> void:
	call_deferred("_replay")

func _check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures.append(label)

func _capture(name: String) -> void:
	for frame in range(4):
		await process_frame
	await RenderingServer.frame_post_draw
	var path: String = "res://reports/tasks/T-020301/" + name + ".png"
	_check(root.get_texture().get_image().save_png(path) == OK, "capture " + name)
	captures.append(path)

func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var scene: Node3D = load("res://scenes/environment/street_scale_scene.tscn").instantiate()
	root.add_child(scene)
	var kit: StreetBlockout = scene.get_node("Street")
	var rig: CameraRig = scene.get_node("CameraRig")
	var player: CharacterBody3D = scene.get_node("Player")
	for tick in range(30):
		await physics_frame
	_check(kit.initialization_error.is_empty(), "all authored collisions integrated")
	var gameplay: CameraPreset = rig.snapshot_preset()
	for erased in [false, true]:
		kit.apply_preview_palette(erased)
		var prefix: String = "ERASED" if erased else "REAL"
		_check(rig.apply_preset(gameplay), prefix + " gameplay preset")
		await _capture(prefix + "_gameplay")
		var front: CameraPreset = gameplay.duplicate()
		front.offset = Vector3(0, 4.5, 16)
		front.look_offset = Vector3(0, 1.5, -2.3)
		_check(rig.apply_preset(front), prefix + " front preset")
		await _capture(prefix + "_front")
		var wide: CameraPreset = gameplay.duplicate()
		wide.fov_degrees = 45
		wide.offset = Vector3(11, 9, 18)
		wide.look_offset = Vector3(0, 1.4, -2.5)
		_check(rig.apply_preset(wide), prefix + " wide preset")
		await _capture(prefix + "_wide")
	kit.apply_preview_palette(false)
	rig.apply_preset(gameplay)
	Input.action_press("move_forward")
	for tick in range(120):
		await physics_frame
	Input.action_release("move_forward")
	for tick in range(30):
		await physics_frame
	_check(player.position.z < -3.5 and absf(player.position.y) < 0.003 and player.is_on_floor(), "real controller walks through door into house")
	await _capture("door_entered")
	var door_inspection: CameraPreset = gameplay.duplicate()
	door_inspection.offset = Vector3(0, 2, 8)
	door_inspection.look_offset = Vector3(0, 1, -3)
	_check(rig.apply_preset(door_inspection), "front door inspection preset")
	await _capture("door_entered_front")
	_check(RenderingServer.get_current_rendering_method() == "forward_plus", "actual Forward+ renderer")
	var report: Dictionary = {"result": "PASS" if failures.is_empty() else "FAIL", "assertions": checks,
		"failures": failures, "captures": captures, "player_after_entry": str(player.position),
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(),
		"input_mode": "synthetic_actions_real_controller", "quality_state": "BLOCKOUT",
		"phase_scope": "REAL_ERASED_material_previews_shared_geometry_NOT_WorldController_switch", "software": true}
	var file := FileAccess.open("res://reports/tasks/T-020301/runtime.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "  "))
	file.close()
	print("STREET_RENDER_REPLAY ", JSON.stringify(report))
	quit(0 if failures.is_empty() else 1)
