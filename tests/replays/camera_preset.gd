extends SceneTree

func _init() -> void:
	call_deferred("_replay")

func _capture(name: String) -> Error:
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image().save_png("res://reports/tasks/T-020201/" + name + ".png")

func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	for frame in range(8):
		await process_frame
	var rig: CameraRig = scene.get_node("CameraRig")
	var camera: Camera3D = rig.get_node("Camera3D")
	var default_error: Error = await _capture("default")
	var custom: CameraPreset = rig.preset.duplicate()
	custom.fov_degrees = 45.0
	custom.offset = Vector3(4, 3.5, 9)
	var applied: bool = rig.apply_preset(custom)
	var tuned_error: Error = await _capture("tuned")
	var before: Transform3D = camera.transform
	var invalid: CameraPreset = custom.duplicate()
	invalid.offset.z = -9.0
	var rejected: bool = not rig.apply_preset(invalid)
	var mouse := InputEventMouseMotion.new()
	mouse.relative = Vector2(500, -300)
	Input.parse_input_event(mouse)
	await process_frame
	var stable: bool = camera.transform.is_equal_approx(before)
	var valid_renderer: bool = RenderingServer.get_current_rendering_method() == "forward_plus"
	var passed: bool = default_error == OK and tuned_error == OK and applied and rejected and stable and valid_renderer
	var report: Dictionary = {"result": "PASS" if passed else "FAIL", "assertions": 6,
		"captures_ok": default_error == OK and tuned_error == OK, "custom_applied": applied,
		"opposite_side_rejected": rejected, "rejection_and_mouse_preserve_transform": stable,
		"perspective": camera.projection == Camera3D.PROJECTION_PERSPECTIVE,
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(),
		"fov": camera.fov, "offset": str(camera.position), "input_mode": "synthetic_mouse_motion"}
	passed = passed and report.perspective
	report.result = "PASS" if passed else "FAIL"
	var file := FileAccess.open("res://reports/tasks/T-020201/runtime.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "  "))
	file.close()
	print("CAMERA_REPLAY ", JSON.stringify(report))
	quit(0 if passed else 1)
