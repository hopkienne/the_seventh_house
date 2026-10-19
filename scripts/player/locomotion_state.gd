class_name LocomotionState
extends RefCounted

enum Mode { IDLE, WALK, RUN, LOCKED }


static func resolve(real_velocity: Vector3, enabled: bool, run_requested: bool, idle_threshold: float) -> Mode:
	if not enabled:
		return Mode.LOCKED
	if Vector2(real_velocity.x, real_velocity.z).length() <= idle_threshold:
		return Mode.IDLE
	return Mode.RUN if run_requested else Mode.WALK


static func label(mode: Mode) -> StringName:
	match mode:
		Mode.IDLE: return &"IDLE"
		Mode.WALK: return &"WALK"
		Mode.RUN: return &"RUN"
		Mode.LOCKED: return &"LOCKED"
	return &"INVALID"
