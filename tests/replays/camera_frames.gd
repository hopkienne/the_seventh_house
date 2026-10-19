extends SceneTree

var failures: Array[String] = []
var checks: int = 0
var profiles: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_replay")

func _check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures.append(label)

func _tick(count: int) -> void:
	for tick in range(count):
		await physics_frame

func _walk(action: String) -> void:
	Input.action_press(action)
	Input.action_press("run")
	await _tick(110)
	Input.action_release(action)
	Input.action_release("run")
	await _tick(60)

func _sample(scene: Node3D, frame: SafeFrame, label: Label, name: String) -> Dictionary:
	await process_frame
	await RenderingServer.frame_post_draw
	var camera: Camera3D = scene.get_node("CameraRig/Camera3D")
	var player: Node3D = scene.get_node("Player")
	var safe: Rect2 = frame.get_safe_rect()
	var targets: Array[Vector3] = [player.global_position, player.global_position + Vector3(0, 1.7, 0),
		Vector3(-0.175, 0.75, -1), Vector3(0.175, 1.25, -1)]
	var points: Array[Vector2] = []
	for target in targets:
		var point: Vector2 = camera.unproject_position(target)
		points.append(point)
		_check(not camera.is_position_behind(target) and safe.has_point(point), name + " target inside safe frame")
	_check(safe.encloses(label.get_global_rect()), name + " UI contained")
	var image: Image = root.get_texture().get_image()
	var error: Error = image.save_png("res://reports/tasks/T-020204/" + name + ".png")
	_check(error == OK, name + " image saved")
	return {"name": name, "window_size": str(root.size), "image_size": str(image.get_size()),
		"viewport_rect": str(root.get_visible_rect()), "safe_rect": str(safe), "ui_rect": str(label.get_global_rect()),
		"target_points": points, "zone": str(scene.get_node("CameraDirector").current_zone_id),
		"content_scale_aspect": root.content_scale_aspect, "content_scale_size": str(root.content_scale_size)}

func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var scene: Node3D = load("res://scenes/tests/camera_corridor.tscn").instantiate()
	root.add_child(scene)
	var layer := CanvasLayer.new()
	scene.add_child(layer)
	var frame: SafeFrame = load("res://scenes/ui/safe_frame.tscn").instantiate()
	layer.add_child(frame)
	var label := Label.new()
	label.text = "KHẢO SÁT HÀNH LANG / INSPECT CORRIDOR\nE • TƯƠNG TÁC / INTERACT"
	label.add_theme_font_size_override("font_size", 32)
	label.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	frame.add_child(label)
	await _tick(60)
	for size in [Vector2i(1280, 720), Vector2i(1280, 800), Vector2i(1680, 720), Vector2i(1280, 720)]:
		root.size = size
		for rendered in range(8):
			await process_frame
		var prefix: String = "%dx%d_%d" % [size.x, size.y, profiles.size()]
		profiles.append(await _sample(scene, frame, label, prefix + "_west"))
		await _walk("move_right")
		profiles.append(await _sample(scene, frame, label, prefix + "_east"))
		await _walk("move_left")
	_check(root.content_scale_aspect == Window.CONTENT_SCALE_ASPECT_KEEP, "engine keep-aspect policy applied")
	_check(RenderingServer.get_current_rendering_method() == "forward_plus", "actual Forward+ renderer")
	var report: Dictionary = {"result": "PASS" if failures.is_empty() else "FAIL", "assertions": checks,
		"failures": failures, "profiles": profiles, "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "input_mode": "synthetic_actions_actual_triggers",
		"ui_scope": "reusable_safe_frame_with_QA_labels_not_full_menu_or_localization_acceptance"}
	var file := FileAccess.open("res://reports/tasks/T-020204/runtime.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "  "))
	file.close()
	print("CAMERA_FRAMES_REPLAY ", JSON.stringify(report))
	quit(0 if failures.is_empty() else 1)
