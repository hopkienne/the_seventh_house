class_name StreetBlockout
extends Node3D
## Shared geometry only. Palette preview does not implement/change world phase.

@export var collision_ids: PackedStringArray
var initialization_error: StringName = &""

func _ready() -> void:
	var found: PackedStringArray = []
	for mesh_node: MeshInstance3D in $Visuals.find_children("*", "MeshInstance3D", true, false):
		if not collision_ids.has(str(mesh_node.name)):
			continue
		found.append(str(mesh_node.name))
		var body := StaticBody3D.new()
		body.name = "Body_" + str(mesh_node.name)
		body.collision_layer = 1
		body.collision_mask = 8
		add_child(body)
		body.transform = global_transform.affine_inverse() * mesh_node.global_transform
		var shape := CollisionShape3D.new()
		shape.shape = mesh_node.mesh.create_trimesh_shape()
		body.add_child(shape)
	if found.size() != collision_ids.size():
		initialization_error = &"COLLISION_ID_MISMATCH"
		push_error("StreetBlockout: COLLISION_ID_MISMATCH %d/%d" % [found.size(), collision_ids.size()])

func apply_preview_palette(erased: bool) -> void:
	# Art review adapter only; all Shared colliders stay queryable in both views.
	for node: MeshInstance3D in $Visuals.find_children("*", "MeshInstance3D", true, false):
		var material: StandardMaterial3D = node.mesh.surface_get_material(0).duplicate()
		if erased:
			var color: Color = material.albedo_color
			var gray: float = color.r * 0.2126 + color.g * 0.7152 + color.b * 0.0722
			material.albedo_color = Color(gray * 0.55, gray * 0.75, gray * 0.95, color.a)
		node.material_override = material
