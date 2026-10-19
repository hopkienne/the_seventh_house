extends Node3D
## Engine bootstrap scene. Campaign/locomotion systems belong to later task cards.


func _ready() -> void:
	$Camera3D.look_at(Vector3(0, 0.85, 0))
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if not args.has("--qa-profile") and not args.has("--qa-report"):
		return
	if args.size() != 4 or args[0] != "--qa-profile" or args[1] != "BOOTSTRAP" or args[2] != "--qa-report":
		printerr("Unknown/malformed bootstrap QA arguments")
		get_tree().quit(2)
		return
	_smoke(args[3])


func _smoke(report_path: String) -> void:
	var tree: SceneTree = get_tree()
	var failures: Array[String] = []
	if DisplayServer.get_name() == "headless":
		printerr("Rendered smoke refuses headless display")
		tree.quit(2)
		return
	if not report_path.begins_with("res://reports/") and not report_path.begins_with("user://"):
		printerr("QA report path outside explicit report roots")
		tree.quit(2)
		return
	for frame in range(8):
		await tree.process_frame
	await RenderingServer.frame_post_draw
	var capture: Image = get_viewport().get_texture().get_image()
	var method: String = RenderingServer.get_current_rendering_method()
	if method != "forward_plus":
		failures.append("Required Forward+ renderer unavailable: " + method)
	if not $Camera3D.current:
		failures.append("Main camera is inactive")
	if capture.is_empty() or capture.get_width() < 640 or capture.get_height() < 360:
		failures.append("Viewport image missing/too small")
	var colors: Dictionary = {}
	if not capture.is_empty():
		for x in range(1, 10):
			for y in range(1, 10):
				colors[capture.get_pixel(capture.get_width() * x / 10, capture.get_height() * y / 10).to_html()] = true
	if colors.size() < 3:
		failures.append("Rendered scene lacks expected color variation")
	var absolute: String = ProjectSettings.globalize_path(report_path)
	var directory_error: Error = DirAccess.make_dir_recursive_absolute(absolute.get_base_dir())
	if directory_error != OK:
		printerr("Cannot create QA report directory: ", directory_error)
		tree.quit(1)
		return
	var capture_path: String = absolute.get_basename() + ".png"
	var capture_error: Error = capture.save_png(capture_path)
	if capture_error != OK:
		failures.append("Capture write failed: " + str(capture_error))
	var report: Dictionary = {"profile": "BOOTSTRAP", "result": "PASS" if failures.is_empty() else "FAIL",
		"assertions": 5, "failed": failures.size(), "skipped": 0, "failures": failures,
		"display": DisplayServer.get_name(), "renderer": method,
		"driver": RenderingServer.get_current_rendering_driver_name(),
		"adapter": RenderingServer.get_video_adapter_name(), "native_os": OS.get_name(),
		"input_mode": "scene_smoke_no_physical_input", "capture": capture_path,
		"width": capture.get_width(), "height": capture.get_height(), "sample_colors": colors.size(),
		"engine": Engine.get_version_info().string,
		"software": RenderingServer.get_video_adapter_name().contains("SwiftShader")}
	var file: FileAccess = FileAccess.open(absolute, FileAccess.WRITE)
	if file == null:
		printerr("Cannot open QA report: ", FileAccess.get_open_error())
		tree.quit(1)
		return
	file.store_string(JSON.stringify(report, "\t") + "\n")
	file.close()
	print("SMOKE_REPORT ", JSON.stringify(report))
	tree.quit(0 if failures.is_empty() else 1)
