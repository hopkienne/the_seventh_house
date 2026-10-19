extends SceneTree

func _init() -> void:
	call_deferred("_replay")

func _tick(count: int) -> void:
	for tick in range(count):
		await physics_frame

func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var rig: Node3D = scene.get_node("CameraRig")
	var camera: Camera3D = rig.get_node("Camera3D")
	var basis_before: Basis = camera.global_basis
	await _tick(30)
	Input.action_press("move_right")
	Input.action_press("run")
	await _tick(300)
	Input.action_release("move_right")
	Input.action_release("run")
	await _tick(120)
	var settled: Vector3 = rig.position
	var maximum_drift: float = 0.0
	for tick in range(120):
		await physics_frame
		maximum_drift = maxf(maximum_drift, rig.position.distance_to(settled))
	await process_frame
	await RenderingServer.frame_post_draw
	var error: Error = root.get_texture().get_image().save_png("res://reports/tasks/T-020202/bound.png")
	var player: CharacterBody3D = scene.get_node("Player")
	var passed: bool = absf(rig.position.x - 1.0) < 0.002 and absf(rig.position.z) < 0.002
	passed = passed and maximum_drift < 0.002 and player.is_on_floor() and player.position.x < 4.75
	passed = passed and basis_before.is_equal_approx(camera.global_basis) and error == OK
	passed = passed and RenderingServer.get_current_rendering_method() == "forward_plus"
	var report: Dictionary = {"result": "PASS" if passed else "FAIL", "assertions": 7,
		"anchor": str(rig.position), "player": str(player.position), "bound_idle_drift_m": maximum_drift,
		"axis_preserved": basis_before.is_equal_approx(camera.global_basis), "grounded": player.is_on_floor(),
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(),
		"input_mode": "synthetic_actions", "capture_error": error}
	var file := FileAccess.open("res://reports/tasks/T-020202/runtime.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "  "))
	file.close()
	print("CAMERA_FOLLOW_REPLAY ", JSON.stringify(report))
	quit(0 if passed else 1)
