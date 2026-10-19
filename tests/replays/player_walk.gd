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
	var start: Vector3 = player.position
	Input.action_press("move_right")
	for tick in range(60):
		await physics_frame
	Input.action_release("move_right")
	for tick in range(20):
		await physics_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var capture: Image = root.get_texture().get_image()
	var error: Error = capture.save_png("res://reports/tasks/T-020102/walk.png")
	var distance: float = player.position.x-start.x
	var passed: bool = distance > 1.8 and distance < 2.5 and player.is_on_floor() and error == OK
	passed = passed and RenderingServer.get_current_rendering_method() == "forward_plus"
	print("WALK_REPLAY ", JSON.stringify({"result": "PASS" if passed else "FAIL",
		"distance_x": distance, "feet_y": player.position.y, "capture_error": error,
		"renderer": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(), "adapter": RenderingServer.get_video_adapter_name(),
		"input_mode": "synthetic_actions", "software": RenderingServer.get_video_adapter_name().contains("SwiftShader"),
		"width": capture.get_width(), "height": capture.get_height()}))
	quit(0 if passed else 1)
