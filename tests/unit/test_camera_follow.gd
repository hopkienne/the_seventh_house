extends RefCounted

func get_cases(runner: SceneTree) -> Dictionary:
	return {"deadzone_bounds_stability": _bounds.bind(runner), "delta_and_rejection": _delta.bind(runner),
		"malformed_zone": _invalid.bind(runner), "live_resource_edit_rejected": _live_edit.bind(runner)}

func _bounds(runner: SceneTree) -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	runner.root.add_child(scene)
	runner.check(scene.has_node("CameraDirector"), "main scene integrates camera director")
	if not scene.has_node("CameraDirector"):
		scene.free()
		return
	var director: Node = scene.get_node("CameraDirector")
	director.set_process(false)
	var player: Node3D = scene.get_node("Player")
	var rig: Node3D = scene.get_node("CameraRig")
	var camera: Camera3D = rig.get_node("Camera3D")
	var facing: Basis = camera.global_basis
	player.position = Vector3(0.2, 0, 0.1)
	director.call("advance", 1.0)
	runner.check(rig.position.is_zero_approx(), "target within dead zone does not move anchor")
	player.position = Vector3(20, 8, 10)
	for frame in range(300):
		director.call("advance", 1.0 / 60)
	runner.check(rig.position.is_equal_approx(Vector3(1, 0, 0.25)), "XZ anchor clamps to authored volume and ignores target Y")
	var stopped: Vector3 = rig.position
	for frame in range(300):
		director.call("advance", 1.0 / 60)
	runner.check(rig.position.distance_to(stopped) < 0.00001, "sustained bound contact does not jitter")
	runner.check(camera.global_basis.is_equal_approx(facing), "following never rotates screen axes")
	player.position = Vector3(-20, 0, -10)
	for frame in range(300):
		director.call("advance", 1.0 / 60)
	runner.check(rig.position.is_equal_approx(Vector3(-1, 0, -0.25)), "reverse movement stays within opposite volume bound")
	runner.check(not director.call("enter_zone", &"MISSING"), "unknown zone rejected")
	var before: Vector3 = rig.position
	runner.check(not director.call("restore", &"MISSING") and rig.position.is_equal_approx(before), "invalid restore leaves camera intact")
	scene.free()

func _delta(runner: SceneTree) -> void:
	if not ResourceLoader.exists("res://scripts/camera/camera_director.gd"):
		runner.check(false, "camera director implementation exists")
		return
	var positions: Array[Vector3] = []
	for fps in [30, 60, 120]:
		var scene: Node3D = load("res://scenes/main.tscn").instantiate()
		runner.root.add_child(scene)
		var director: Node = scene.get_node("CameraDirector")
		director.set_process(false)
		var rig: Node3D = scene.get_node("CameraRig")
		var player: Node3D = scene.get_node("Player")
		player.position = Vector3(10, 0, 0)
		for frame in range(fps):
			director.call("advance", 1.0 / fps)
		positions.append(rig.position)
		var before: Vector3 = rig.position
		director.call("advance", NAN)
		director.call("advance", -1.0)
		director.call("advance", 0.0)
		runner.check(rig.position.is_equal_approx(before), "invalid/zero deltas do not mutate camera")
		runner.check(director.call("restore", &"CORRIDOR") and rig.position.is_equal_approx(Vector3(1, 0, 0)), "valid restore clamps immediately without stale smoothing")
		scene.free()
	runner.check(positions[0].distance_to(positions[1]) < 0.00001 and positions[1].distance_to(positions[2]) < 0.00001, "30/60/120 delta schedules converge equally")
	print("CAMERA_DELTA_METRICS ", JSON.stringify({"positions_after_one_second": positions, "scope": "deterministic_delta_schedules_not_measured_render_FPS"}))

func _invalid(runner: SceneTree) -> void:
	if not ResourceLoader.exists("res://config/tuning/camera_zone_corridor.tres"):
		runner.check(false, "zone tuning resource exists")
		return
	var zone: Resource = load("res://config/tuning/camera_zone_corridor.tres").duplicate(true)
	zone.set("dead_zone", Vector2(-1, 0))
	runner.check(not zone.call("is_valid"), "negative deadzone rejected")
	zone.set("dead_zone", Vector2(0.6, 0.3))
	zone.set("minimum", Vector2(3, 0))
	runner.check(not zone.call("is_valid"), "reversed volume rejected")
	zone.set("minimum", Vector2(-1, -0.25))
	zone.set("smoothing_speed", NAN)
	runner.check(not zone.call("is_valid"), "nonfinite smoothing rejected")

func _live_edit(runner: SceneTree) -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	var director: Node = scene.get_node("CameraDirector")
	var zone: Resource = load("res://config/tuning/camera_zone_corridor.tres").duplicate(true)
	var zones: Array = director.get("zones")
	zones[0] = zone
	runner.root.add_child(scene)
	director.set_process(false)
	zone.set("smoothing_speed", NAN)
	runner.check(not director.call("enter_zone", &"CORRIDOR"), "malformed authored zone cannot be re-entered")
	var rig: Node3D = scene.get_node("CameraRig")
	runner.check(rig.position.is_zero_approx(), "rejected re-entry leaves anchor intact")
	scene.get_node("Player").position = Vector3(10, 0, 0)
	director.call("advance", 1.0)
	runner.check(rig.position.is_finite() and rig.position.x > 0.99, "accepted tuning snapshot survives invalid source edits")
	scene.free()
