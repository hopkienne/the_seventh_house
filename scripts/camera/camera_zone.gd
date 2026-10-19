class_name CameraZone
extends Resource
## Bounds describe the rig anchor in its parent space, never player bounds.

@export var zone_id: StringName = &"CORRIDOR"
@export var framing: CameraPreset = preload("res://config/tuning/camera_corridor.tres")
@export var dead_zone: Vector2 = Vector2(0.6, 0.3)
@export var minimum: Vector2 = Vector2(-1, -0.25)
@export var maximum: Vector2 = Vector2(1, 0.25)
@export var smoothing_speed: float = 8.0
@export var blend_duration: float = 0.6

func is_valid() -> bool:
	return not zone_id.is_empty() and framing != null and framing.is_valid() \
		and dead_zone.is_finite() and dead_zone.x >= 0 and dead_zone.y >= 0 \
		and minimum.is_finite() and maximum.is_finite() \
		and minimum.x <= maximum.x and minimum.y <= maximum.y \
		and is_finite(smoothing_speed) and smoothing_speed > 0 \
		and is_finite(blend_duration) and blend_duration >= 0

func clamp_anchor(value: Vector3) -> Vector3:
	return Vector3(clampf(value.x, minimum.x, maximum.x), value.y, clampf(value.z, minimum.y, maximum.y))

func desired_anchor(target: Vector3, current: Vector3) -> Vector3:
	var wanted: Vector3 = current
	var difference: Vector2 = Vector2(target.x - current.x, target.z - current.z)
	if absf(difference.x) > dead_zone.x:
		wanted.x = target.x - signf(difference.x) * dead_zone.x
	if absf(difference.y) > dead_zone.y:
		wanted.z = target.z - signf(difference.y) * dead_zone.y
	return clamp_anchor(wanted)
