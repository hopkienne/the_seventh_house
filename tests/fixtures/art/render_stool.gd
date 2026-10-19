extends SceneTree


func _init() -> void:
	call_deferred("_render")


func _render() -> void:
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	scene.get_node("ScaleReference").visible = false
	var model: Node3D = load("res://tests/fixtures/art/stool_spike.glb").instantiate()
	scene.add_child(model)
	var camera: Camera3D = scene.get_node("Camera3D")
	camera.position = Vector3(1.2, 0.9, 1.5)
	camera.look_at(Vector3(0, 0.24, 0))
	for frame in range(8):
		await process_frame
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var error: Error = image.save_png("res://reports/tasks/T-010402/stool.png")
	var passed: bool = error == OK and RenderingServer.get_current_rendering_method() == "forward_plus"
	print("ART_RENDER ", JSON.stringify({"result": "PASS" if passed else "FAIL", "error": error,
		"renderer": RenderingServer.get_current_rendering_method(), "driver": RenderingServer.get_current_rendering_driver_name(),
		"adapter": RenderingServer.get_video_adapter_name(), "software": true,
		"width": image.get_width(), "height": image.get_height(), "quality_state": "BLOCKOUT"}))
	quit(0 if passed else 1)
