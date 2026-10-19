extends RefCounted

const PLAYER_PATH: String = "res://scenes/player/player.tscn"


func get_cases(runner: SceneTree) -> Dictionary:
	return {"feet_and_capsule": _structure.bind(runner),
		"gravity_and_idle": _gravity.bind(runner), "invalid_settings": _invalid.bind(runner)}


func _structure(runner: SceneTree) -> void:
	runner.check(ResourceLoader.exists(PLAYER_PATH), "player scene exists")
	if not ResourceLoader.exists(PLAYER_PATH):
		return
	var player: CharacterBody3D = load(PLAYER_PATH).instantiate()
	var collision: CollisionShape3D = player.get_node("Collision")
	var visual: MeshInstance3D = player.get_node("PrototypeBody")
	runner.check(collision.shape is CapsuleShape3D, "player collider is capsule")
	runner.check(is_equal_approx(collision.shape.height, 1.7), "capsule height1.70m")
	runner.check(is_equal_approx(collision.shape.radius, 0.28), "capsule radius0.28m")
	runner.check(is_zero_approx(collision.position.y-collision.shape.height/2.0), "collider bottom matches feet pivot")
	runner.check(is_equal_approx(visual.mesh.height, collision.shape.height), "blockout visual height matches collider")
	runner.check(is_equal_approx(visual.position.y, collision.position.y), "visual and collider centers match")
	runner.check(player.collision_layer == 8 and player.collision_mask == 19, "Player layer and initial REAL mask")
	player.free()


func _gravity(runner: SceneTree) -> void:
	runner.check(ResourceLoader.exists(PLAYER_PATH), "gravity fixture has real player scene")
	if not ResourceLoader.exists(PLAYER_PATH):
		return
	var environment: Node3D = Node3D.new()
	var floor_body: StaticBody3D = StaticBody3D.new()
	floor_body.collision_layer = 1
	floor_body.collision_mask = 8
	floor_body.position.y = -0.25
	var shape: CollisionShape3D = CollisionShape3D.new()
	var box: BoxShape3D = BoxShape3D.new()
	box.size = Vector3(12, 0.5, 6)
	shape.shape = box
	floor_body.add_child(shape)
	environment.add_child(floor_body)
	var player: CharacterBody3D = load(PLAYER_PATH).instantiate()
	player.position.y = 2.0
	environment.add_child(player)
	runner.root.add_child(environment)
	for frame in range(90):
		await runner.physics_frame
	runner.check(player.is_on_floor(), "gravity drops capsule onto actual physics floor")
	runner.check(absf(player.position.y) < 0.002, "feet settle within2mm of floor rather than capsule center")
	var start: Vector3 = player.position
	var max_vertical_drift: float = 0.0
	var max_horizontal_drift: float = 0.0
	for frame in range(180):
		await runner.physics_frame
		var difference: Vector3 = player.position-start
		max_vertical_drift = maxf(max_vertical_drift, absf(difference.y))
		max_horizontal_drift = maxf(max_horizontal_drift, Vector2(difference.x, difference.z).length())
	runner.check(player.is_on_floor(), "idle remains grounded")
	runner.check(max_vertical_drift < 0.002, "idle vertical drift under2mm over3seconds")
	runner.check(max_horizontal_drift < 0.0001, "idle X/Z drift under0.1mm over3seconds")
	print("PHYSICS_METRICS ", JSON.stringify({"feet_y": player.position.y,
		"vertical_drift": max_vertical_drift, "horizontal_drift": max_horizontal_drift,
		"physics_ticks_per_second": Engine.physics_ticks_per_second}))
	environment.queue_free()
	await runner.process_frame


func _invalid(runner: SceneTree) -> void:
	runner.check(ResourceLoader.exists(PLAYER_PATH), "settings fixture has real player")
	if not ResourceLoader.exists(PLAYER_PATH):
		return
	var player: CharacterBody3D = load(PLAYER_PATH).instantiate()
	var before: Resource = player.get("physics_settings")
	var invalid: Resource = load("res://scripts/player/player_physics_settings.gd").new()
	invalid.set("gravity_scale", -1.0)
	runner.check(not player.call("configure", invalid), "negative gravity rejected")
	runner.check(player.get("physics_settings") == before, "rejected tuning preserves valid settings")
	runner.check(not player.call("configure", null), "missing tuning rejected")
	player.free()
