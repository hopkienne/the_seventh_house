extends SceneTree
## Deterministic diagnostic movie; fixed movie time is never a live FPS benchmark.

const Course = preload("res://tests/fixtures/movement_course.gd")

func _init() -> void:
	call_deferred("_replay")

func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var course: Node3D = Course.create(20.0)
	root.add_child(course)
	for tick in range(30):
		await physics_frame
	Input.action_press("move_right")
	Input.action_press("run")
	for tick in range(200):
		await physics_frame
	Input.action_release("move_right")
	Input.action_release("run")
	for tick in range(30):
		await physics_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var player: CharacterBody3D = course.get_node("Player")
	var error: Error = root.get_texture().get_image().save_png("res://reports/tasks/T-020104/slope_render.png")
	var passed: bool = player.position.x > 5.0 and absf(player.position.y - 6.0 * sin(deg_to_rad(20.0))) < 0.003
	passed = passed and player.is_on_floor() and error == OK and RenderingServer.get_current_rendering_method() == "forward_plus"
	print("MOVEMENT_CLIP ", JSON.stringify({"result": "PASS" if passed else "FAIL", "held_ticks": 200,
		"position": str(player.position), "grounded": player.is_on_floor(), "capture_error": error,
		"renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(),
		"scope": "fixed_time_diagnostic_NOT_observed_FPS", "input_mode": "synthetic_actions"}))
	quit(0 if passed else 1)
