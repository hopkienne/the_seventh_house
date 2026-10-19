extends RefCounted

func get_cases(runner: SceneTree) -> Dictionary:
	return {"integrated_perspective": _integrated.bind(runner), "tuning_rejection_and_mouse": _tuning.bind(runner)}

func _integrated(runner: SceneTree) -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	runner.root.add_child(scene)
	runner.check(scene.has_node("CameraRig/Camera3D"), "main scene integrates reusable camera rig")
	if not scene.has_node("CameraRig/Camera3D"):
		scene.free()
		return
	var camera: Camera3D = scene.get_node("CameraRig/Camera3D")
	runner.check(camera.current and camera.projection == Camera3D.PROJECTION_PERSPECTIVE, "integrated perspective camera is current")
	runner.check(is_equal_approx(camera.fov, 38.0), "default FOV38 from preset")
	runner.check(camera.position.is_equal_approx(Vector3(6, 4, 8)), "default camera offset preserved")
	runner.check(camera.global_basis.x.dot(Vector3.RIGHT) > 0.5, "camera screen-right preserves world right")
	scene.free()

func _tuning(runner: SceneTree) -> void:
	if not ResourceLoader.exists("res://scenes/camera/camera_rig.tscn"):
		runner.check(false, "reusable camera rig scene exists")
		return
	var rig: Node3D = load("res://scenes/camera/camera_rig.tscn").instantiate()
	runner.root.add_child(rig)
	var camera: Camera3D = rig.get_node("Camera3D")
	var preset: Resource = load("res://config/tuning/camera_corridor.tres").duplicate()
	preset.set("fov_degrees", 45.0)
	preset.set("offset", Vector3(4, 3.5, 9))
	runner.check(rig.call("apply_preset", preset), "valid custom preset accepted")
	runner.check(is_equal_approx(camera.fov, 45.0) and camera.position.is_equal_approx(Vector3(4, 3.5, 9)), "FOV and offset apply together")
	var before: Transform3D = camera.transform
	var invalid: Resource = preset.duplicate()
	invalid.set("fov_degrees", NAN)
	runner.check(not rig.call("apply_preset", invalid), "NaN FOV rejected")
	invalid = preset.duplicate()
	invalid.set("offset", Vector3(4, 3.5, -9))
	runner.check(not rig.call("apply_preset", invalid), "opposite-side camera rejected")
	invalid = preset.duplicate()
	invalid.set("far_distance", 0.01)
	runner.check(not rig.call("apply_preset", invalid), "invalid clipping interval rejected")
	runner.check(not rig.call("apply_preset", null), "null preset rejected")
	runner.check(camera.transform.is_equal_approx(before) and is_equal_approx(camera.fov, 45.0), "all rejections retain previous camera configuration")
	var mouse := InputEventMouseMotion.new()
	mouse.relative = Vector2(500, -300)
	Input.parse_input_event(mouse)
	await runner.process_frame
	runner.check(camera.transform.is_equal_approx(before), "mouse motion cannot rotate camera")
	rig.free()
