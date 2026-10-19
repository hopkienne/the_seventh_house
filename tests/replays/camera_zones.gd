extends SceneTree

var failures: Array[String] = []
var samples: Array[Dictionary] = []
var checks: int = 0
var _scene: Node3D
var _direction: String = ""
var _captured_blend: bool = false

func _init() -> void:
	call_deferred("_replay")

func _check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures.append(label)

func _capture(name: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	_check(root.get_texture().get_image().save_png("res://reports/tasks/T-020203/" + name + ".png") == OK, "capture " + name)

func _walk(scene: Node3D, action: String) -> void:
	var camera: Camera3D = scene.get_node("CameraRig/Camera3D")
	var director: CameraDirector = scene.get_node("CameraDirector")
	Input.action_press(action)
	Input.action_press("run")
	_direction = action
	_captured_blend = false
	var axes_ok: bool = true
	for tick in range(110):
		await physics_frame
		axes_ok = axes_ok and camera.global_basis.x.dot(Vector3.RIGHT) > 0.5
	Input.action_release(action)
	Input.action_release("run")
	_direction = ""
	for tick in range(60):
		await physics_frame
	_check(axes_ok, action + " preserves screen right on every sample")
	_check(_captured_blend, action + " exposes intermediate rendered framing")
	await _capture(action + "_end")

func _sample_blend() -> void:
	if _direction.is_empty() or _captured_blend:
		return
	var camera: Camera3D = _scene.get_node("CameraRig/Camera3D")
	var director: CameraDirector = _scene.get_node("CameraDirector")
	if director.is_blending() and camera.fov > 38.05 and camera.fov < 41.95:
		var error: Error = root.get_texture().get_image().save_png("res://reports/tasks/T-020203/" + _direction + "_blend.png")
		_check(error == OK, "capture intermediate " + _direction)
		_captured_blend = true
		samples.append({"direction": _direction, "fov": camera.fov, "zone": str(director.current_zone_id)})

func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var scene: Node3D = load("res://scenes/tests/camera_corridor.tscn").instantiate()
	_scene = scene
	root.add_child(scene)
	RenderingServer.frame_post_draw.connect(_sample_blend)
	for tick in range(60):
		await physics_frame
	await _capture("west_start")
	var director: CameraDirector = scene.get_node("CameraDirector")
	var player: CharacterBody3D = scene.get_node("Player")
	await _walk(scene, "move_right")
	_check(player.position.x > 2 and director.current_zone_id == &"EAST", "physical entry east")
	await _walk(scene, "move_left")
	_check(player.position.x < -2 and director.current_zone_id == &"WEST", "physical entry west")
	_check(player.is_on_floor(), "roundtrip remains grounded")
	_check(not director.enter_zone(&"UNKNOWN"), "invalid zone rejected")
	_check(director.restore(&"WEST") and not director.is_blending(), "restore cancels transient state")
	_check(RenderingServer.get_current_rendering_method() == "forward_plus", "actual Forward+ renderer")
	var report: Dictionary = {"result": "PASS" if failures.is_empty() else "FAIL", "assertions": checks,
		"failures": failures, "blend_samples": samples, "position": str(player.position),
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(),
		"input_mode": "synthetic_actions_actual_Area3D_signals", "software": true}
	var file := FileAccess.open("res://reports/tasks/T-020203/runtime.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "  "))
	file.close()
	print("CAMERA_ZONES_REPLAY ", JSON.stringify(report))
	quit(0 if failures.is_empty() else 1)
