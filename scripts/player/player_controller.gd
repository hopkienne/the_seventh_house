class_name PlayerController
extends CharacterBody3D
## Locomotion body owns pose/velocity only, never world/story/save authority.

signal locomotion_changed(previous: StringName, current: StringName)

@export var physics_settings: PlayerPhysicsSettings = preload("res://config/tuning/player_physics.tres")
var initialization_error: StringName = &""
var _control_enabled: bool = true
var _locomotion_mode: LocomotionState.Mode = LocomotionState.Mode.IDLE


func _ready() -> void:
	if not configure(physics_settings):
		initialization_error = &"INVALID_SETTINGS"
		set_physics_process(false)
		printerr("PlayerController: INVALID_SETTINGS")


func configure(settings: PlayerPhysicsSettings) -> bool:
	if settings == null or not settings.is_valid():
		return false
	physics_settings = settings
	return true


func _physics_process(delta: float) -> void:
	var move_input: Vector2 = Vector2.ZERO
	if _control_enabled:
		move_input = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var speed: float = physics_settings.run_speed if Input.is_action_pressed("run") else physics_settings.walk_speed
	var target: Vector2 = move_input * speed
	var horizontal: Vector2 = Vector2(velocity.x, velocity.z)
	var slowing: bool = target.is_zero_approx() or horizontal.length_squared() > target.length_squared()
	var rate: float = physics_settings.deceleration if slowing else physics_settings.acceleration
	horizontal = horizontal.move_toward(target, rate * delta)
	velocity.x = horizontal.x
	velocity.z = horizontal.y
	if not is_on_floor():
		velocity += get_gravity() * physics_settings.gravity_scale * delta
	else:
		velocity.y = 0.0
	move_and_slide()
	_update_locomotion_state()


func set_control_enabled(enabled: bool) -> void:
	# InputRouter owns global lock tokens; this is only the body's local input gate.
	_control_enabled = enabled
	_update_locomotion_state()


func get_locomotion_state() -> StringName:
	return LocomotionState.label(_locomotion_mode)


func _update_locomotion_state() -> void:
	var next: LocomotionState.Mode = LocomotionState.resolve(get_real_velocity(), _control_enabled,
		Input.is_action_pressed("run"), physics_settings.idle_speed_threshold)
	if next == _locomotion_mode:
		return
	var previous: StringName = LocomotionState.label(_locomotion_mode)
	_locomotion_mode = next
	locomotion_changed.emit(previous, get_locomotion_state())
