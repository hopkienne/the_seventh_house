extends RefCounted


func get_cases(runner: SceneTree) -> Dictionary:
	return {"import_generated_glb": _import_glb.bind(runner),
		"missing_glb_rejected": func() -> void:
			runner.check(not ResourceLoader.exists("res://tests/fixtures/art/not_produced.glb"), "missing model is unavailable")}


func _import_glb(runner: SceneTree) -> void:
	var packed: PackedScene = load("res://tests/fixtures/art/stool_spike.glb")
	runner.check(packed != null, "generated GLB imported as real PackedScene")
	if packed == null:
		return
	var model: Node = packed.instantiate()
	var meshes: Array[Node] = model.find_children("*", "MeshInstance3D", true, false)
	runner.check(meshes.size() == 5, "seat and four legs preserved")
	for node: MeshInstance3D in meshes:
		runner.check(node.mesh.get_surface_count() == 1, "one surface per generated primitive")
		runner.check(node.mesh.surface_get_material(0) != null, "material survives import")
		var arrays: Array = node.mesh.surface_get_arrays(0)
		runner.check(arrays[Mesh.ARRAY_VERTEX].size() > 0, "vertices survive import")
		runner.check(arrays[Mesh.ARRAY_NORMAL].size() == arrays[Mesh.ARRAY_VERTEX].size(), "normals match vertices")
		runner.check(arrays[Mesh.ARRAY_TEX_UV].size() == arrays[Mesh.ARRAY_VERTEX].size(), "primitive UVs survive import")
	var seat: Node3D = model.find_child("Seat", true, false)
	runner.check(seat != null and is_equal_approx(seat.position.y, 0.45), "meter-scale seat pivot preserved")
	model.free()
