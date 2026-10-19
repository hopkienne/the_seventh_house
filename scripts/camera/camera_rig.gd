class_name CameraRig
extends Node3D
## Framing only. No mouse orbit/input handlers or world/story/save writes.

@export var preset: CameraPreset = preload("res://config/tuning/camera_corridor.tres")
var initialization_error: StringName = &""
var _look_offset: Vector3 = Vector3(0, 0.85, 0)

func _ready() -> void:
	if not apply_preset(preset):
		initialization_error = &"INVALID_CAMERA_PRESET"
		$Camera3D.current = false
		printerr("CameraRig: INVALID_CAMERA_PRESET")

func apply_preset(next: CameraPreset) -> bool:
	if next == null or not next.is_valid() or not is_inside_tree():
		return false
	var camera: Camera3D = $Camera3D
	# All inputs validated before any state changes; rejected presets are atomic.
	camera.set_perspective(next.fov_degrees, next.near_distance, next.far_distance)
	camera.position = next.offset
	camera.look_at(to_global(next.look_offset), Vector3.UP)
	_look_offset = next.look_offset
	preset = next
	initialization_error = &""
	return true

func snapshot_preset() -> CameraPreset:
	var camera: Camera3D = $Camera3D
	var snapshot := CameraPreset.new()
	snapshot.fov_degrees = camera.fov
	snapshot.offset = camera.position
	snapshot.look_offset = _look_offset
	snapshot.near_distance = camera.near
	snapshot.far_distance = camera.far
	return snapshot
