class_name CameraZoneTrigger
extends Area3D
## Filtering by target identity prevents props/enemies from selecting a camera.

@export var zone_id: StringName
@export var fallback_zone_id: StringName
@export var director_path: NodePath = ^"../CameraDirector"
@export var target_path: NodePath = ^"../Player"

func _ready() -> void:
	body_entered.connect(_on_entered)
	body_exited.connect(_on_exited)

func _on_entered(body: Node3D) -> void:
	var director: CameraDirector = get_node_or_null(director_path) as CameraDirector
	if director != null and body == get_node_or_null(target_path):
		director.enter_zone(zone_id)

func _on_exited(body: Node3D) -> void:
	var director: CameraDirector = get_node_or_null(director_path) as CameraDirector
	if director != null and body == get_node_or_null(target_path) \
		and director.current_zone_id == zone_id and not fallback_zone_id.is_empty():
		# Handles reversing while the capsule still overlaps both adjacent zones.
		director.enter_zone(fallback_zone_id)
