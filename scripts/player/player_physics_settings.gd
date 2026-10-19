class_name PlayerPhysicsSettings
extends Resource

@export_range(0.1, 4.0, 0.05) var gravity_scale: float = 1.0
@export_range(0.1, 10.0, 0.1) var walk_speed: float = 2.2
@export_range(0.1, 15.0, 0.1) var run_speed: float = 3.4
@export_range(0.1, 50.0, 0.1) var acceleration: float = 12.0
@export_range(0.1, 50.0, 0.1) var deceleration: float = 16.0
@export_range(0.0, 0.2, 0.01) var idle_speed_threshold: float = 0.05


func is_valid() -> bool:
	for value: float in [gravity_scale, walk_speed, run_speed, acceleration, deceleration]:
		if not is_finite(value) or value <= 0.0:
			return false
	return gravity_scale <= 4.0 and run_speed >= walk_speed and is_finite(idle_speed_threshold) and idle_speed_threshold >= 0.0 and idle_speed_threshold <= 0.2
