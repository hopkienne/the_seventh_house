extends SceneTree
## Observe real frame-post-draw samples. Never use fixed-fps/movie timing as FPS evidence.

const Course = preload("res://tests/fixtures/movement_course.gd")
var drawn: int = 0

func _init() -> void:
	call_deferred("_replay")

func _on_draw() -> void:
	drawn += 1

func _tick(count: int) -> void:
	for frame in range(count):
		await physics_frame

func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		printerr("Rendered FPS evidence requires a window")
		quit(2)
		return
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	RenderingServer.frame_post_draw.connect(_on_draw)
	var samples: Array[Dictionary] = []
	var achieved: bool = true
	var capture_prefix: String = "res://reports/tasks/T-020104/fps_%dx%d" % [root.size.x, root.size.y]
	for requested in [30, 60, 120]:
		Engine.max_fps = requested
		var course: Node3D = Course.create()
		root.add_child(course)
		await _tick(120)
		var player: CharacterBody3D = course.get_node("Player")
		var origin: Vector3 = player.position
		var first: int = drawn
		var started: int = Time.get_ticks_usec()
		Input.action_press("move_right")
		await _tick(300)
		Input.action_release("move_right")
		var elapsed: float = (Time.get_ticks_usec() - started) / 1000000.0
		var frames: int = drawn - first
		var observed: float = frames / elapsed
		var distance: float = player.position.x - origin.x
		await _tick(30)
		await process_frame
		await RenderingServer.frame_post_draw
		var capture_error: Error = root.get_texture().get_image().save_png(capture_prefix + "_%d.png" % requested)
		var hit_target: bool = absf(observed - requested) / requested < 0.10
		achieved = achieved and hit_target
		samples.append({"requested_fps": requested, "observed_draw_fps": observed,
			"target_achieved": hit_target, "drawn_frames": frames, "elapsed_seconds": elapsed,
			"held_physics_ticks": 300, "distance_m": distance, "capture_error": capture_error,
			"grounded": player.is_on_floor(), "final_position": str(player.position)})
		course.queue_free()
		await process_frame
	var minimum: float = INF
	var maximum: float = 0.0
	var physical_ok: bool = true
	for sample in samples:
		minimum = minf(minimum, sample.distance_m)
		maximum = maxf(maximum, sample.distance_m)
		physical_ok = physical_ok and sample.grounded and sample.capture_error == OK and sample.distance_m > 10.0
	var relative_spread: float = (maximum - minimum) / minimum
	physical_ok = physical_ok and relative_spread < 0.05 and RenderingServer.get_current_rendering_method() == "forward_plus"
	var report: Dictionary = {"result": "FAIL" if not physical_ok else ("PASS" if achieved else "NOT_TESTED"),
		"samples": samples, "relative_distance_spread": relative_spread,
		"physics_ticks_per_second": Engine.physics_ticks_per_second,
		"renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "input_mode": "synthetic_actions",
		"resolution": str(root.size), "scope": "QA_course_only_not_campaign_or_hardware_benchmark"}
	var output := FileAccess.open(capture_prefix + ".json", FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "  "))
	output.close()
	print("FPS_REPLAY ", JSON.stringify(report))
	quit(1 if not physical_ok else (0 if achieved else 3))
