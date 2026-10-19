extends SceneTree


func _init() -> void:
	call_deferred("_build")


func _build() -> void:
	var config: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tools/art/stool_spike.json"))
	var model: Node3D = Node3D.new()
	model.name = "SkillSpikeStool"
	root.add_child(model)
	var material: StandardMaterial3D = StandardMaterial3D.new()
	var color: Array = config.albedo
	material.albedo_color = Color(color[0], color[1], color[2], color[3])
	material.roughness = config.roughness
	var seat: Array = config.seat_size
	_box(model, "Seat", Vector3(seat[0], seat[1], seat[2]), Vector3(0, config.seat_y, 0), material)
	var leg: Array = config.leg_size
	var offset: Array = config.leg_offset
	var index: int = 0
	for x in [-1, 1]:
		for z in [-1, 1]:
			index += 1
			_box(model, "Leg_%02d" % index, Vector3(leg[0], leg[1], leg[2]),
				Vector3(x * offset[0], leg[1] / 2.0, z * offset[1]), material)
	var document: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	var error: Error = document.append_from_scene(model, state)
	if error == OK:
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(str(config.output).get_base_dir()))
		error = document.write_to_filesystem(state, config.output)
	print("ART_EXPORT ", JSON.stringify({"asset_id": config.asset_id, "error": error,
		"path": config.output, "meshes": 5, "quality_state": config.quality_state,
		"engine": Engine.get_version_info().string}))
	model.free()
	quit(0 if error == OK else 1)


func _box(model: Node3D, label: String, size: Vector3, pose: Vector3, material: Material) -> void:
	var node: MeshInstance3D = MeshInstance3D.new()
	var mesh: BoxMesh = BoxMesh.new()
	mesh.size = size
	mesh.material = material
	node.mesh = mesh
	node.name = label
	node.position = pose
	model.add_child(node)
	node.owner = model
