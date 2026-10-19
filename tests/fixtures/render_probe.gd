extends SceneTree
## Bounded capability probe, not a game or a final art acceptance scene.


func _init() -> void:
	call_deferred("_probe")


func _probe() -> void:
	if DisplayServer.get_name() == "headless":
		printerr("Rendered probe refuses headless display")
		quit(2)
		return
	var scene: Node3D = Node3D.new()
	root.add_child(scene)
	var mesh: MeshInstance3D = MeshInstance3D.new()
	mesh.mesh = BoxMesh.new()
	scene.add_child(mesh)
	var camera: Camera3D = Camera3D.new()
	scene.add_child(camera)
	camera.position = Vector3(3, 2, 4)
	camera.look_at(Vector3.ZERO)
	camera.current = true
	var light: DirectionalLight3D = DirectionalLight3D.new()
	scene.add_child(light)
	light.rotation_degrees = Vector3(-45, -30, 0)
	for frame in range(5):
		await process_frame
	await RenderingServer.frame_post_draw
	var capture: Image = root.get_texture().get_image()
	var software: bool = RenderingServer.get_video_adapter_name().contains("SwiftShader")
	var path: String = "res://reports/tasks/T-010301/render_capability_software.png" if software else "res://reports/tasks/T-010301/render_capability_native.png"
	var error: Error = capture.save_png(path)
	print("RENDER_PROBE ", JSON.stringify({"display": DisplayServer.get_name(),
		"method": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(),
		"adapter": RenderingServer.get_video_adapter_name(), "capture_error": error,
		"width": capture.get_width(), "height": capture.get_height(), "capture_path": path,
		"software": software}))
	var correct_renderer: bool = RenderingServer.get_current_rendering_method() == "forward_plus"
	if not correct_renderer:
		printerr("Required Forward+ renderer unavailable; automatic fallback is not a passing capability probe")
	quit(0 if error == OK and correct_renderer else 1)
