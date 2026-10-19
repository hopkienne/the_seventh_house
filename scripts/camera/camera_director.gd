class_name CameraDirector
extends Node
## Owns camera anchor only. No input remapping or player/world/save mutations.

@export var target_path: NodePath = ^"../Player"
@export var rig_path: NodePath = ^"../CameraRig"
@export var zones: Array[CameraZone] = [preload("res://config/tuning/camera_zone_corridor.tres")]
@export var initial_zone_id: StringName = &"CORRIDOR"
var current_zone_id: StringName = &""
var initialization_error: StringName = &""
var _target: Node3D
var _rig: CameraRig
var _zones: Dictionary = {}
var _active: CameraZone
var _height: float = 0.0
var _from_framing: CameraPreset
var _blend_frame: CameraPreset = CameraPreset.new()
var _blend_elapsed: float = 0.0
var _blending: bool = false
var _bounds_min: Vector2
var _bounds_max: Vector2
var _from_min: Vector2
var _from_max: Vector2

func _ready() -> void:
	_target = get_node_or_null(target_path) as Node3D
	_rig = get_node_or_null(rig_path) as CameraRig
	if _target == null or _rig == null:
		_fail(&"MISSING_TARGET_OR_RIG")
		return
	_height = _rig.position.y
	for zone in zones:
		if zone == null or not zone.is_valid() or _zones.has(zone.zone_id):
			_fail(&"INVALID_OR_DUPLICATE_CAMERA_ZONE")
			return
		_zones[zone.zone_id] = zone
	if not enter_zone(initial_zone_id):
		_fail(&"UNKNOWN_INITIAL_ZONE")

func _fail(reason: StringName) -> void:
	initialization_error = reason
	set_process(false)
	printerr("CameraDirector: ", reason)

func enter_zone(zone_id: StringName) -> bool:
	return _select_zone(zone_id, false)

func _select_zone(zone_id: StringName, immediate: bool) -> bool:
	if not _zones.has(zone_id) or not is_instance_valid(_rig):
		return false
	var zone: CameraZone = _zones[zone_id]
	if not zone.is_valid():
		return false
	if current_zone_id == zone_id and not immediate:
		return true
	var first: bool = _active == null
	_from_framing = _rig.snapshot_preset()
	_from_min = _bounds_min
	_from_max = _bounds_max
	# Freeze accepted tuning for the active update loop. Invalid edits to an
	# authored Resource are rejected on entry, never leaked into live smoothing.
	_active = zone.duplicate_deep(Resource.DEEP_DUPLICATE_ALL)
	current_zone_id = zone_id
	_blend_elapsed = 0.0
	_blending = not first and not immediate and _active.blend_duration > 0.0
	if not _blending:
		_rig.apply_preset(_active.framing)
		_bounds_min = _active.minimum
		_bounds_max = _active.maximum
		_rig.position = _clamp_anchor(_rig.position)
	return true

func restore(zone_id: StringName) -> bool:
	if not is_instance_valid(_target) or not _select_zone(zone_id, true):
		return false
	_rig.position = _desired()
	return true

func is_blending() -> bool:
	return _blending

func _clamp_anchor(value: Vector3) -> Vector3:
	return Vector3(clampf(value.x, _bounds_min.x, _bounds_max.x), value.y,
		clampf(value.z, _bounds_min.y, _bounds_max.y))

func _advance_blend(delta: float) -> void:
	if not _blending:
		return
	_blend_elapsed = minf(_blend_elapsed + delta, _active.blend_duration)
	var weight: float = smoothstep(0.0, 1.0, _blend_elapsed / _active.blend_duration)
	var target: CameraPreset = _active.framing
	_blend_frame.fov_degrees = lerpf(_from_framing.fov_degrees, target.fov_degrees, weight)
	_blend_frame.offset = _from_framing.offset.lerp(target.offset, weight)
	_blend_frame.look_offset = _from_framing.look_offset.lerp(target.look_offset, weight)
	_blend_frame.near_distance = lerpf(_from_framing.near_distance, target.near_distance, weight)
	_blend_frame.far_distance = lerpf(_from_framing.far_distance, target.far_distance, weight)
	_rig.apply_preset(_blend_frame)
	_bounds_min = _from_min.lerp(_active.minimum, weight)
	_bounds_max = _from_max.lerp(_active.maximum, weight)
	if _blend_elapsed >= _active.blend_duration:
		_blending = false

func _process(delta: float) -> void:
	advance(delta)

func _desired() -> Vector3:
	var target_local: Vector3 = (_rig.get_parent() as Node3D).to_local(_target.global_position)
	var wanted: Vector3 = _active.desired_anchor(target_local, _rig.position)
	wanted.y = _height
	return wanted

func advance(delta: float) -> void:
	if not is_finite(delta) or delta <= 0 or _active == null:
		return
	if not is_instance_valid(_rig) or not is_instance_valid(_target):
		return
	_advance_blend(delta)
	var weight: float = 1.0 - exp(-_active.smoothing_speed * delta)
	_rig.position = _clamp_anchor(_rig.position.lerp(_desired(), weight))
