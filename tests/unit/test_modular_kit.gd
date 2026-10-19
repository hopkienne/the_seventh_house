extends RefCounted

const IDS: Array[String] = ["fence_2m", "wall_2m", "door_open_2m", "door_closed_2m"]

func get_cases(runner: SceneTree) -> Dictionary:
	return {"imports_and_grid": _imports.bind(runner), "rotated_collision": _rotation.bind(runner),
		"joined_seams": _seams.bind(runner), "capsule_open_closed": _doors.bind(runner)}

func _kit(id: String) -> Node3D:
	return load("res://scenes/environment/modules/" + id + ".tscn").instantiate()

func _imports(runner: SceneTree) -> void:
	for id in IDS:
		var path: String = "res://art/export/blockout/" + id + ".glb"
		runner.check(ResourceLoader.exists(path), id + " real GLB imported")
		if not ResourceLoader.exists(path):
			continue
		var kit: Node3D = _kit(id)
		runner.root.add_child(kit)
		runner.check(kit.get("initialization_error") == &"", id + " all authored collision IDs resolved")
		runner.check(kit.position == Vector3.ZERO and kit.scale == Vector3.ONE, id + " ground grid origin and unit root scale")
		runner.check(kit.get_node("SocketStart").position == Vector3.ZERO and kit.get_node("SocketEnd").position == Vector3(2, 0, 0), id + " endpoints on 0.25m grid")
		var min_x: float = INF
		var max_x: float = -INF
		var min_y: float = INF
		for node: MeshInstance3D in kit.get_node("Visuals").find_children("*", "MeshInstance3D", true, false):
			var bounds: AABB = node.global_transform * node.mesh.get_aabb()
			min_x = minf(min_x, bounds.position.x)
			max_x = maxf(max_x, bounds.end.x)
			min_y = minf(min_y, bounds.position.y)
			runner.check(node.global_basis.determinant() > 0.999, id + "/" + str(node.name) + " no reflected or collapsed mesh transform")
			var arrays: Array = node.mesh.surface_get_arrays(0)
			runner.check(arrays[Mesh.ARRAY_NORMAL].size() == arrays[Mesh.ARRAY_VERTEX].size() and arrays[Mesh.ARRAY_TEX_UV].size() == arrays[Mesh.ARRAY_VERTEX].size(), id + " normals and UV complete")
			runner.check(node.mesh.surface_get_material(0) != null, id + " material survives import")
		runner.check(absf(min_x) < 0.0001 and absf(max_x - 2) < 0.0001 and absf(min_y) < 0.0001, id + " mesh spans exactly 2m from ground pivot")
		for body: StaticBody3D in kit.find_children("*", "StaticBody3D", true, false):
			runner.check(body.collision_layer == 1 and body.collision_mask == 8 and body.global_basis.determinant() > 0.999, id + " Shared static body has positive scale")
		kit.queue_free()
		await runner.process_frame

func _ray(kit: Node3D, x: float, y: float) -> Dictionary:
	return kit.get_world_3d().direct_space_state.intersect_ray(PhysicsRayQueryParameters3D.create(
		kit.to_global(Vector3(x, y, 1)), kit.to_global(Vector3(x, y, -1)), 1))

func _rotation(runner: SceneTree) -> void:
	for id in IDS:
		for angle in [0, 90, 180, 270]:
			var kit: Node3D = _kit(id)
			kit.position = Vector3(4, 0, -2)
			kit.rotation_degrees.y = angle
			runner.root.add_child(kit)
			await runner.physics_frame
			await runner.physics_frame
			var solid: bool = id != "door_open_2m"
			var hit: Dictionary = _ray(kit, 1, 0.6 if id == "fence_2m" else 1.0)
			runner.check(not hit.is_empty() if solid else hit.is_empty(), id + " collision at rotation" + str(angle))
			if solid and not hit.is_empty():
				runner.check(hit.collider.get_parent() == kit, "ray hits rotated module, not another fixture")
			else:
				runner.check(not _ray(kit, 0.15, 1).is_empty(), "open door jamb still queryable when rotated")
			kit.queue_free()
			await runner.process_frame

func _seams(runner: SceneTree) -> void:
	for id in ["wall_2m", "fence_2m"]:
		var a: Node3D = _kit(id)
		var b: Node3D = _kit(id)
		b.position.x = 2
		runner.root.add_child(a)
		runner.root.add_child(b)
		await runner.physics_frame
		await runner.physics_frame
		runner.check(a.get_node("SocketEnd").global_position.is_equal_approx(b.get_node("SocketStart").global_position), id + " adjacent sockets meet without scale")
		for x in [1.99, 2.0, 2.01]:
			runner.check(not _ray(a, x, 0.6).is_empty(), id + " joint has no collision slit atx" + str(x))
		# A right angle joins by rotation, never a mirrored scale.
		b.rotation_degrees.y = 90
		await runner.physics_frame
		await runner.physics_frame
		runner.check(a.get_node("SocketEnd").global_position.is_equal_approx(b.get_node("SocketStart").global_position), id + " corner sockets meet")
		runner.check(not _ray(b, 1, 0.6).is_empty(), id + " corner collision remains present")
		a.queue_free()
		b.queue_free()
		await runner.process_frame

func _doors(runner: SceneTree) -> void:
	for id in ["door_open_2m", "door_closed_2m"]:
		var fixture := Node3D.new()
		runner.root.add_child(fixture)
		var floor_body := StaticBody3D.new()
		floor_body.collision_layer = 1
		fixture.add_child(floor_body)
		var shape := CollisionShape3D.new()
		var box := BoxShape3D.new()
		box.size = Vector3(8, 0.2, 8)
		shape.shape = box
		shape.position.y = -0.1
		floor_body.add_child(shape)
		var kit: Node3D = _kit(id)
		kit.position = Vector3(-1, 0, -1)
		fixture.add_child(kit)
		var player: CharacterBody3D = load("res://scenes/player/player.tscn").instantiate()
		player.position = Vector3(0, 0.1, 1)
		fixture.add_child(player)
		for tick in range(40): await runner.physics_frame
		Input.action_press("move_forward")
		for tick in range(120): await runner.physics_frame
		Input.action_release("move_forward")
		for tick in range(30): await runner.physics_frame
		runner.check(player.position.z < -2.5 if id == "door_open_2m" else player.position.z > -0.7, id + " real capsule clearance/block")
		runner.check(player.is_on_floor() and absf(player.position.y) < 0.003, id + " grounded without teleport")
		print("MODULE_DOOR_METRICS ", JSON.stringify({"id": id, "position": str(player.position), "grounded": player.is_on_floor()}))
		fixture.queue_free()
		await runner.process_frame
