extends SceneTree


func _init() -> void:
	call_deferred("_replay")


func _replay() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: CharacterBody3D = scene.get_node("Player")
	for tick in range(30):
		await physics_frame
	Input.action_press("move_right")
	Input.action_press("run")
	for tick in range(300):
		await physics_frame
	player.call("set_control_enabled", false)
	Input.action_release("move_right")
	Input.action_release("run")
	for tick in range(20):
		await physics_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var capture: Image = root.get_texture().get_image()
	var error: Error = capture.save_png("res://reports/tasks/T-020103/bounds.png")
	var passed: bool = player.position.x > 4.5 and player.position.x < 4.75 and absf(player.position.y) < 0.002
	passed = passed and player.is_on_floor() and player.call("get_locomotion_state") == &"LOCKED"
	passed = passed and error == OK and RenderingServer.get_current_rendering_method() == "forward_plus"
	print("BOUNDS_REPLAY ", JSON.stringify({"result": "PASS" if passed else "FAIL",
		"position": player.position, "locomotion": player.call("get_locomotion_state"), "grounded": player.is_on_floor(),
		"held_physics_ticks": 300, "capture_error": error, "renderer": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(), "adapter": RenderingServer.get_video_adapter_name(),
		"input_mode": "synthetic_actions", "software": RenderingServer.get_video_adapter_name().contains("SwiftShader"),
		"width": capture.get_width(), "height": capture.get_height()}))
	quit(0 if passed else 1)
