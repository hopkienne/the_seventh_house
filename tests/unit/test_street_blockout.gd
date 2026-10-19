extends RefCounted

func get_cases(runner: SceneTree) -> Dictionary:
	return {"import_scale_materials": _assets.bind(runner), "physical_door_clearance": _door.bind(runner),
		"four_metre_clear_lanes": _lanes.bind(runner)}

func _assets(runner: SceneTree) -> void:
	runner.check(ResourceLoader.exists("res://art/export/blockout_street.glb"), "actual street GLB imported")
	if not ResourceLoader.exists("res://art/export/blockout_street.glb"):
		return
	var metrics: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://art/export/blockout_street.metrics.json"))
	var kit: Node3D = load("res://scenes/environment/street_blockout.tscn").instantiate()
	runner.root.add_child(kit)
	runner.check(kit.get("initialization_error") == &"", "every authored collision ID resolves after import")
	var meshes: Array[Node] = kit.get_node("Visuals").find_children("*", "MeshInstance3D", true, false)
	runner.check(meshes.size() == metrics.meshes.size(), "all authored mesh IDs survive GLB import")
	for node: MeshInstance3D in meshes:
		var arrays: Array = node.mesh.surface_get_arrays(0)
		runner.check(arrays[Mesh.ARRAY_NORMAL].size() == arrays[Mesh.ARRAY_VERTEX].size(), str(node.name) + " imported normals complete")
		runner.check(arrays[Mesh.ARRAY_TEX_UV].size() == arrays[Mesh.ARRAY_VERTEX].size(), str(node.name) + " imported UVs complete")
		runner.check(node.mesh.surface_get_material(0) != null, str(node.name) + " PBR material imported")
	var street: MeshInstance3D = kit.find_child("StreetSlab", true, false)
	var bounds: AABB = street.global_transform * street.mesh.get_aabb()
	runner.check(absf(bounds.size.z - 4.0) < 0.0001 and absf(bounds.size.x - 18) < 0.0001, "imported street has18m length and4m clear width")
	runner.check(absf(bounds.end.y) < 0.0001, "walkable surface top at metre zero")
	var colliders: Array[Node] = kit.find_children("*", "StaticBody3D", true, false)
	var expected_colliders: int = 0
	for record: Dictionary in metrics.meshes:
		if record.collision:
			expected_colliders += 1
	runner.check(colliders.size() == expected_colliders, "all authored collision bodies produced")
	for collider: StaticBody3D in colliders:
		runner.check(collider.collision_layer == 1 and collider.collision_mask == 8, "authored collision uses Shared layer")
	kit.call("apply_preview_palette", true)
	runner.check(kit.find_children("*", "StaticBody3D", true, false).size() == colliders.size(), "ERASED art preview retains same queryable Shared collision")
	kit.queue_free()
	await runner.process_frame

func _door(runner: SceneTree) -> void:
	if not ResourceLoader.exists("res://scenes/environment/street_blockout.tscn"):
		runner.check(false, "integrated street prefab exists")
		return
	for x in [0.0, 0.85]:
		var kit: Node3D = load("res://scenes/environment/street_blockout.tscn").instantiate()
		runner.root.add_child(kit)
		var player: CharacterBody3D = load("res://scenes/player/player.tscn").instantiate()
		player.position = Vector3(x, 0.1, 0)
		runner.root.add_child(player)
		for tick in range(40):
			await runner.physics_frame
		Input.action_press("move_forward")
		for tick in range(120):
			await runner.physics_frame
		Input.action_release("move_forward")
		for tick in range(30):
			await runner.physics_frame
		runner.check(player.position.z < -3.5 if is_zero_approx(x) else player.position.z > -2.2, "center passes open door; jamb blocks capsule atx" + str(x))
		runner.check(player.is_on_floor() and absf(player.position.y) < 0.003, "door/house floor supports real capsule")
		print("STREET_DOOR_METRICS ", JSON.stringify({"spawn_x": x, "position": str(player.position), "grounded": player.is_on_floor()}))
		player.queue_free()
		kit.queue_free()
		await runner.process_frame

func _lanes(runner: SceneTree) -> void:
	var kit: Node3D = load("res://scenes/environment/street_blockout.tscn").instantiate()
	runner.root.add_child(kit)
	var players: Array[CharacterBody3D] = []
	for z in [-1.65, 0.0, 1.65]:
		var player: CharacterBody3D = load("res://scenes/player/player.tscn").instantiate()
		player.position = Vector3(-7, 0.1, z)
		kit.add_child(player)
		players.append(player)
	for tick in range(40):
		await runner.physics_frame
	Input.action_press("move_right")
	for tick in range(120):
		await runner.physics_frame
	Input.action_release("move_right")
	for tick in range(30):
		await runner.physics_frame
	for player in players:
		runner.check(player.position.x > -3 and player.is_on_floor(), "capsule traverses clear lane atz" + str(player.position.z))
	print("STREET_LANE_METRICS ", JSON.stringify({"positions": players.map(func(p: CharacterBody3D) -> String: return str(p.position))}))
	kit.queue_free()
	await runner.process_frame
