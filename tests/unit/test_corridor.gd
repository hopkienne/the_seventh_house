extends RefCounted

const ACTIONS: Array[String] = ["move_left", "move_right", "move_forward", "move_back", "run"]


func get_cases(runner: SceneTree) -> Dictionary:
	return {"idle_walk_run_locked": _states.bind(runner), "four_physical_bounds": _bounds.bind(runner)}


func _tick(runner: SceneTree, count: int) -> void:
	for frame in range(count):
		await runner.physics_frame


func _scene(runner: SceneTree) -> Node3D:
	for action in ACTIONS:
		Input.action_release(action)
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	runner.root.add_child(scene)
	return scene


func _cleanup(runner: SceneTree, scene: Node3D) -> void:
	for action in ACTIONS:
		Input.action_release(action)
	scene.queue_free()
	await runner.process_frame


func _states(runner: SceneTree) -> void:
	var scene: Node3D = _scene(runner)
	var player: CharacterBody3D = scene.get_node("Player")
	runner.check(player.has_method("get_locomotion_state"), "locomotion state is observable")
	if not player.has_method("get_locomotion_state"):
		await _cleanup(runner, scene)
		return
	var transitions: Array[StringName] = []
	player.connect("locomotion_changed", func(_from: StringName, to: StringName) -> void: transitions.append(to))
	await _tick(runner, 30)
	runner.check(player.call("get_locomotion_state") == &"IDLE", "standing state is Idle")
	Input.action_press("move_right")
	await _tick(runner, 20)
	runner.check(player.call("get_locomotion_state") == &"WALK", "motion state is Walk")
	Input.action_press("run")
	await _tick(runner, 10)
	runner.check(player.call("get_locomotion_state") == &"RUN", "run intent has distinct moving state")
	player.call("set_control_enabled", false)
	runner.check(player.call("get_locomotion_state") == &"LOCKED", "local input gate changes state immediately")
	for action in ACTIONS:
		Input.action_release(action)
	await _tick(runner, 30)
	runner.check(player.call("get_locomotion_state") == &"LOCKED", "state stays Locked while disabled")
	player.call("set_control_enabled", true)
	runner.check(player.call("get_locomotion_state") == &"IDLE", "release returns to Idle")
	runner.check(transitions == [&"WALK", &"RUN", &"LOCKED", &"IDLE"], "one signal per actual state change")
	runner.check(not InputMap.has_action("jump") and not InputMap.has_action("attack"), "no jump/combat action added")
	await _cleanup(runner, scene)


func _bounds(runner: SceneTree) -> void:
	var scene: Node3D = _scene(runner)
	var player: CharacterBody3D = scene.get_node("Player")
	runner.check(scene.has_node("CorridorBounds"), "main corridor has physical boundary nodes")
	if not scene.has_node("CorridorBounds"):
		await _cleanup(runner, scene)
		return
	await _tick(runner, 30)
	Input.action_press("run")
	var points: Array[Vector3] = []
	for action in ["move_right", "move_forward", "move_left", "move_back"]:
		Input.action_press(action)
		await _tick(runner, 180)
		Input.action_release(action)
		runner.check(absf(player.position.x) < 4.75 and absf(player.position.z) < 1.75, "actual collision confines X/Z for " + action)
		runner.check(absf(player.position.y) < 0.002 and player.is_on_floor(), "cannot walk off floor at " + action)
		points.append(player.position)
	Input.action_press("move_left")
	Input.action_press("move_back")
	await _tick(runner, 120)
	runner.check(absf(player.position.x) < 4.75 and absf(player.position.z) < 1.75 and player.is_on_floor(), "diagonal corner cannot escape bounds")
	print("CORRIDOR_METRICS ", JSON.stringify({"boundary_positions": points, "corner_position": player.position,
		"input_mode": "synthetic_actions", "bounds_mode": "StaticBody3D_collisions_no_coordinate_clamp"}))
	await _cleanup(runner, scene)
