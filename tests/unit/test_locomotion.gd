extends RefCounted

const ACTIONS: Array[String] = ["move_left", "move_right", "move_forward", "move_back", "run"]


func get_cases(runner: SceneTree) -> Dictionary:
	return {"five_second_straight_diagonal": _normalization.bind(runner),
		"acceleration_deceleration_run_lock": _motion.bind(runner)}


func _tick(runner: SceneTree, count: int) -> void:
	for frame in range(count):
		await runner.physics_frame


func _fixture(runner: SceneTree) -> Dictionary:
	for action in ACTIONS:
		Input.action_release(action)
	var environment: Node3D = Node3D.new()
	var floor_body: StaticBody3D = StaticBody3D.new()
	floor_body.position.y = -0.25
	floor_body.collision_layer = 1
	floor_body.collision_mask = 8
	var collider: CollisionShape3D = CollisionShape3D.new()
	var shape: BoxShape3D = BoxShape3D.new()
	shape.size = Vector3(60, 0.5, 60)
	collider.shape = shape
	floor_body.add_child(collider)
	environment.add_child(floor_body)
	var player: CharacterBody3D = load("res://scenes/player/player.tscn").instantiate()
	environment.add_child(player)
	runner.root.add_child(environment)
	return {"environment": environment, "player": player}


func _measure(runner: SceneTree, actions: Array[String]) -> float:
	var fixture: Dictionary = _fixture(runner)
	var player: CharacterBody3D = fixture.player
	await _tick(runner, 30)
	var start: Vector3 = player.position
	for action in actions:
		Input.action_press(action)
	await _tick(runner, 300)
	var distance: float = Vector2(player.position.x-start.x, player.position.z-start.z).length()
	for action in ACTIONS:
		Input.action_release(action)
	fixture.environment.queue_free()
	await runner.process_frame
	return distance


func _normalization(runner: SceneTree) -> void:
	var straight: float = await _measure(runner, ["move_right"])
	var diagonal: float = await _measure(runner, ["move_right", "move_forward"])
	var error_ratio: float = absf(diagonal-straight)/maxf(straight, 0.001)
	runner.check(straight > 10.5 and straight < 11.1, "five-second walk distance reflects2.2m/s with acceleration")
	runner.check(diagonal > 10.5 and diagonal < 11.1, "diagonal moves real body over five seconds")
	runner.check(error_ratio <= 0.05, "straight/diagonal five-second distance differs at most5percent")
	print("LOCOMOTION_METRICS ", JSON.stringify({"straight_m": straight, "diagonal_m": diagonal,
		"relative_error": error_ratio, "duration_seconds": 5.0, "physics_ticks": 300,
		"tick_rate": Engine.physics_ticks_per_second, "input_mode": "synthetic_actions"}))


func _motion(runner: SceneTree) -> void:
	var fixture: Dictionary = _fixture(runner)
	var player: CharacterBody3D = fixture.player
	await _tick(runner, 30)
	Input.action_press("move_right")
	await _tick(runner, 1)
	var first_speed: float = Vector2(player.velocity.x, player.velocity.z).length()
	runner.check(first_speed > 0.0 and first_speed < 2.2, "accelerates rather than instantly reaching walk speed")
	await _tick(runner, 20)
	runner.check(is_equal_approx(player.velocity.x, 2.2), "reaches authored walk speed")
	Input.action_release("move_right")
	await _tick(runner, 1)
	runner.check(player.velocity.x > 0.0 and player.velocity.x < 2.2, "decelerates on release")
	await _tick(runner, 20)
	runner.check(Vector2(player.velocity.x, player.velocity.z).length() < 0.001, "comes to rest")
	Input.action_press("move_right")
	Input.action_press("run")
	await _tick(runner, 30)
	runner.check(is_equal_approx(player.velocity.x, 3.4), "run reaches authored3.4m/s")
	runner.check(player.has_method("set_control_enabled"), "local control gate exists")
	if player.has_method("set_control_enabled"):
		player.call("set_control_enabled", false)
		await _tick(runner, 30)
		var locked: Vector3 = player.position
		await _tick(runner, 30)
		runner.check(player.position.distance_to(locked) < 0.001, "held input cannot move a control-disabled body")
		player.call("set_control_enabled", true)
		await _tick(runner, 30)
		runner.check(player.position.x > locked.x, "control resumes without teleport")
	for action in ACTIONS:
		Input.action_release(action)
	fixture.environment.queue_free()
	await runner.process_frame
