class_name CameraPreset
extends Resource
## Zone-authored framing. Same-side camera preserves X direction on screen.

@export_range(5.0, 90.0) var fov_degrees: float = 38.0
@export var offset: Vector3 = Vector3(6, 4, 8)
@export var look_offset: Vector3 = Vector3(0, 0.85, 0)
@export var near_distance: float = 0.05
@export var far_distance: float = 200.0

func is_valid() -> bool:
	return is_finite(fov_degrees) and fov_degrees >= 5.0 and fov_degrees <= 90.0 \
		and offset.is_finite() and look_offset.is_finite() \
		and offset.z - look_offset.z >= 1.0 \
		and is_finite(near_distance) and is_finite(far_distance) \
		and near_distance > 0.0 and far_distance > near_distance
