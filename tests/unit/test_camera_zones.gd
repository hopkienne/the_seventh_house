extends RefCounted

func get_cases(runner: SceneTree) -> Dictionary:
	return {"blend_interruption_and_restore": _blend.bind(runner), "physical_zone_traversal": _traverse.bind(runner),
		"blend_delta_schedules": _delta.bind(runner), "reverse_inside_overlap": _overlap.bind(runner)}

func _blend(runner: SceneTree) -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	var director: Node = scene.get_node("CameraDirector")
	var zone: Resource = load("res://config/tuning/camera_zone_corridor.tres").duplicate(true)
	zone.zone_id = &"EAST"
	zone.framing = zone.framing.duplicate()
	zone.framing.offset = Vector3(4, 4.5, 10)
	zone.framing.fov_degrees = 42.0
	director.zones.append(zone)
	runner.root.add_child(scene)
	director.set_process(false)
	var rig: Node3D = scene.get_node("CameraRig")
	var camera: Camera3D = rig.get_node("Camera3D")
	var initial: Transform3D = camera.transform
	runner.check(director.enter_zone(&"EAST"), "second zone accepted")
	runner.check(camera.transform.is_equal_approx(initial) and is_equal_approx(camera.fov, 38), "zone entry begins continuous blend without cut")
	director.advance(0.15)
	runner.check(camera.fov > 38 and camera.fov < 42, "mid blend FOV is strictly between presets")
	runner.check(camera.global_basis.x.dot(Vector3.RIGHT) > 0.5, "blend preserves screen right")
	var halfway: Transform3D = camera.transform
	var halfway_fov: float = camera.fov
	runner.check(not director.enter_zone(&"MISSING") and camera.transform.is_equal_approx(halfway), "invalid zone leaves in-flight blend intact")
	runner.check(director.enter_zone(&"CORRIDOR"), "reverse request interrupts blend")
	runner.check(camera.transform.is_equal_approx(halfway) and is_equal_approx(camera.fov, halfway_fov), "interruption starts from currently displayed framing")
	director.advance(1.0)
	runner.check(camera.transform.is_equal_approx(initial) and is_equal_approx(camera.fov, 38), "reverse blend settles exactly at original preset")
	director.enter_zone(&"EAST")
	director.advance(0.1)
	runner.check(director.restore(&"EAST") and is_equal_approx(camera.fov, 42), "restore cancels transient blend and applies saved zone immediately")
	director.advance(2.0)
	runner.check(is_equal_approx(camera.fov, 42), "restore cannot be overwritten by old blend")
	scene.free()

func _traverse(runner: SceneTree) -> void:
	if not ResourceLoader.exists("res://scenes/tests/camera_corridor.tscn"):
		runner.check(false, "two-zone playable fixture exists")
		return
	var scene: Node3D = load("res://scenes/tests/camera_corridor.tscn").instantiate()
	runner.root.add_child(scene)
	var director: Node = scene.get_node("CameraDirector")
	var player: CharacterBody3D = scene.get_node("Player")
	var camera: Camera3D = scene.get_node("CameraRig/Camera3D")
	for tick in range(30):
		await runner.physics_frame
	runner.check(director.current_zone_id == &"WEST", "spawn enters west physical area")
	Input.action_press("move_right")
	Input.action_press("run")
	var axes_ok: bool = true
	for tick in range(110):
		await runner.physics_frame
		axes_ok = axes_ok and camera.global_basis.x.dot(Vector3.RIGHT) > 0.5
	Input.action_release("move_right")
	Input.action_release("run")
	for tick in range(60):
		await runner.physics_frame
	runner.check(player.position.x > 2 and director.current_zone_id == &"EAST", "real movement enters east trigger")
	runner.check(axes_ok, "forward crossing never flips X")
	Input.action_press("move_left")
	Input.action_press("run")
	for tick in range(110):
		await runner.physics_frame
		axes_ok = axes_ok and camera.global_basis.x.dot(Vector3.RIGHT) > 0.5
	Input.action_release("move_left")
	Input.action_release("run")
	for tick in range(60):
		await runner.physics_frame
	runner.check(player.position.x < -2 and director.current_zone_id == &"WEST", "return movement enters west trigger")
	runner.check(axes_ok and player.is_on_floor(), "reverse crossing preserves axes and player support")
	var outsider := CharacterBody3D.new()
	scene.add_child(outsider)
	scene.get_node("EastTrigger").call("_on_entered", outsider)
	runner.check(director.current_zone_id == &"WEST", "unrelated body cannot select zone")
	scene.queue_free()
	await runner.process_frame

func _delta(runner: SceneTree) -> void:
	var fovs: Array[float] = []
	for rate in [30, 60, 120]:
		var scene: Node3D = load("res://scenes/tests/camera_corridor.tscn").instantiate()
		runner.root.add_child(scene)
		var director: Node = scene.get_node("CameraDirector")
		director.set_process(false)
		var camera: Camera3D = scene.get_node("CameraRig/Camera3D")
		director.enter_zone(&"EAST")
		for frame in range(rate / 5):
			director.advance(1.0 / rate)
		fovs.append(camera.fov)
		var before: Transform3D = camera.transform
		director.enter_zone(&"EAST")
		runner.check(camera.transform.is_equal_approx(before), "repeated zone entry does not cut/restart framing")
		director.advance(0.4)
		runner.check(not director.is_blending() and is_equal_approx(camera.fov, 42), "blend finishes at authored duration")
		scene.free()
	runner.check(absf(fovs[0] - fovs[1]) < 0.00001 and absf(fovs[1] - fovs[2]) < 0.00001, "blend fraction independent of30/60/120 delta schedule")
	print("ZONE_BLEND_METRICS ", JSON.stringify({"fovs_at_0_2_seconds": fovs, "scope": "delta_schedules_not_actual_renderFPS"}))

func _overlap(runner: SceneTree) -> void:
	var scene: Node3D = load("res://scenes/tests/camera_corridor.tscn").instantiate()
	runner.root.add_child(scene)
	for tick in range(30):
		await runner.physics_frame
	Input.action_press("move_right")
	Input.action_press("run")
	for tick in range(57):
		await runner.physics_frame
	Input.action_release("move_right")
	Input.action_release("run")
	for tick in range(40):
		await runner.physics_frame
	var player: CharacterBody3D = scene.get_node("Player")
	var director: Node = scene.get_node("CameraDirector")
	var overlapping: bool = scene.get_node("WestTrigger").get_overlapping_bodies().has(player) and scene.get_node("EastTrigger").get_overlapping_bodies().has(player)
	runner.check(overlapping and director.current_zone_id == &"EAST", "capsule can stop inside both volumes after east entry")
	print("ZONE_OVERLAP_METRICS ", JSON.stringify({"position": str(player.position), "overlaps_both": overlapping}))
	Input.action_press("move_left")
	for tick in range(40):
		await runner.physics_frame
	Input.action_release("move_left")
	for tick in range(30):
		await runner.physics_frame
	runner.check(player.position.x < -0.3 and director.current_zone_id == &"WEST", "exiting east restores west even when west never exited")
	scene.queue_free()
	await runner.process_frame
