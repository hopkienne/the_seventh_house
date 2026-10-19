extends RefCounted
## QA geometry only: matching visible/collision surfaces, no player pose corrections.

static func box(parent: Node3D, size: Vector3, at: Vector3, angle: float = 0.0) -> void:
	var body := StaticBody3D.new()
	body.collision_layer = 1
	body.collision_mask = 8
	body.position = at
	body.rotation.z = angle
	var collision := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size
	collision.shape = shape
	body.add_child(collision)
	var visual := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = size
	visual.mesh = mesh
	body.add_child(visual)
	parent.add_child(body)


static func create(angle_degrees: float = 0.0) -> Node3D:
	var course := Node3D.new()
	if is_zero_approx(angle_degrees):
		box(course, Vector3(30, 0.2, 6), Vector3(0, -0.1, 0))
	else:
		var angle: float = deg_to_rad(angle_degrees)
		var rise: float = 6.0 * sin(angle)
		var edge: float = 3.0 * cos(angle)
		box(course, Vector3(10, 0.2, 6), Vector3(-edge - 5, -0.1, 0))
		box(course, Vector3(6, 0.2, 6), Vector3(0, rise / 2 - 0.1 * cos(angle), 0), angle)
		box(course, Vector3(10, 0.2, 6), Vector3(edge + 5, rise - 0.1, 0))
	var player: CharacterBody3D = load("res://scenes/player/player.tscn").instantiate()
	player.name = "Player"
	player.position = Vector3(-5, 0.1, 0)
	course.add_child(player)
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-55, -20, 0)
	course.add_child(light)
	var camera := Camera3D.new()
	camera.position = Vector3(1, 7, 16)
	camera.rotation_degrees = Vector3(-20, 0, 0)
	camera.fov = 60
	course.add_child(camera)
	return course
