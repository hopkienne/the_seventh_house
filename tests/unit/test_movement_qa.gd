extends RefCounted

const Course = preload("res://tests/fixtures/movement_course.gd")

func get_cases(runner: SceneTree) -> Dictionary:
	return {"slope_20_up_down_idle": _slope.bind(runner, 20.0),
		"slope_40_up_down_idle": _slope.bind(runner, 40.0),
		"interrupted_scene_reload": _reload.bind(runner)}


func _tick(runner: SceneTree, count: int) -> void:
	for frame in range(count):
		await runner.physics_frame


func _slope(runner: SceneTree, degrees: float) -> void:
	var course: Node3D = Course.create(degrees)
	runner.root.add_child(course)
	var player: CharacterBody3D = course.get_node("Player")
	await _tick(runner, 40)
	runner.check(player.is_on_floor(), "slope approach starts grounded")
	Input.action_press("move_right")
	Input.action_press("run")
	await _tick(runner, 200)
	Input.action_release("move_right")
	Input.action_release("run")
	await _tick(runner, 40)
	var top: Vector3 = player.position
	var expected_height: float = 6.0 * sin(deg_to_rad(degrees))
	runner.check(top.x > 3.0 * cos(deg_to_rad(degrees)) + 0.28, "climbs supported slope without sticking")
	runner.check(absf(top.y - expected_height) < 0.003 and player.is_on_floor(), "reaches upper floor at authored height")
	await _tick(runner, 120)
	runner.check(player.position.distance_to(top) < 0.002, "idle on upper landing does not drift")
	Input.action_press("move_left")
	Input.action_press("run")
	await _tick(runner, 60)
	Input.action_release("move_left")
	Input.action_release("run")
	await _tick(runner, 30)
	var slope_stop: Vector3 = player.position
	runner.check(slope_stop.y > 0.1 and slope_stop.y < expected_height - 0.1, "idle probe is on slope, not landing")
	await _tick(runner, 120)
	runner.check(player.position.distance_to(slope_stop) < 0.002 and player.is_on_floor(), "idle capsule does not slide on supported slope")
	Input.action_press("move_left")
	Input.action_press("run")
	await _tick(runner, 140)
	Input.action_release("move_left")
	Input.action_release("run")
	await _tick(runner, 40)
	runner.check(player.position.x < -3.1 and absf(player.position.y) < 0.003, "descends back to lower floor")
	runner.check(player.is_on_floor(), "descent remains supported at stop")
	print("SLOPE_METRICS ", JSON.stringify({"degrees": degrees, "top": top, "bottom": player.position}))
	course.queue_free()
	await runner.process_frame


func _reload(runner: SceneTree) -> void:
	var course: Node3D = Course.create()
	runner.root.add_child(course)
	await _tick(runner, 30)
	Input.action_press("move_right")
	await _tick(runner, 30)
	var player: CharacterBody3D = course.get_node("Player")
	player.set_control_enabled(false)
	Input.action_release("move_right")
	await _tick(runner, 30)
	var stopped: Vector3 = player.position
	await _tick(runner, 60)
	runner.check(player.position.distance_to(stopped) < 0.002, "interrupted input gate stops motion")
	course.queue_free()
	await runner.process_frame
	course = Course.create()
	runner.root.add_child(course)
	await _tick(runner, 40)
	player = course.get_node("Player")
	runner.check(player.get_locomotion_state() == &"IDLE", "fresh scene has no stale lock")
	Input.action_press("move_right")
	await _tick(runner, 30)
	Input.action_release("move_right")
	runner.check(player.position.x > -4.5, "fresh scene responds after interruption")
	course.queue_free()
	await runner.process_frame
