extends RefCounted


func get_cases(runner: SceneTree) -> Dictionary:
	return {"scene_structure": func() -> void: _scene(runner),
		"input_mapping": func() -> void: _input(runner),
		"scene_reload": func() -> void: _reload(runner)}


func _scene(runner: SceneTree) -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	runner.check(packed != null, "main scene loads")
	if packed == null:
		return
	var scene: Node = packed.instantiate()
	runner.root.add_child(scene)
	runner.check(scene is Node3D, "main root is 3D")
	runner.check(scene.get_node("CameraRig/Camera3D") is Camera3D, "perspective camera exists")
	runner.check(scene.get_node("CameraRig/Camera3D").projection == Camera3D.PROJECTION_PERSPECTIVE, "camera perspective projection")
	runner.check(is_equal_approx(scene.get_node("CameraRig/Camera3D").fov, 38.0), "initial cinematic FOV")
	runner.check(scene.get_node("KeyLight") is DirectionalLight3D, "light exists")
	runner.check(scene.get_node("WorldEnvironment").environment != null, "environment exists")
	runner.check(scene.get_node("Floor/Collision").shape is BoxShape3D, "floor has 3D collision")
	runner.check(scene.get_node("Floor").collision_layer == 1, "floor uses Shared layer")
	runner.check(ProjectSettings.get_setting("application/run/main_scene") == "res://scenes/main.tscn", "F5 points to main")
	scene.free()


func _input(runner: SceneTree) -> void:
	var keys: Dictionary = {"move_left": KEY_A, "move_right": KEY_D, "move_forward": KEY_W,
		"move_back": KEY_S, "run": KEY_SHIFT, "interact": KEY_E, "toggle_lantern": KEY_Q,
		"journal": KEY_J, "pause": KEY_ESCAPE, "hint": KEY_H, "debug_overlay": KEY_F3}
	for action: String in keys:
		runner.check(InputMap.has_action(action), "action exists: " + action)
		var event: InputEventKey = InputEventKey.new()
		event.physical_keycode = keys[action]
		event.pressed = true
		runner.check(InputMap.event_is_action(event, action), "physical key matches: " + action)
		if action != "debug_overlay":
			var has_pad: bool = false
			for binding: InputEvent in InputMap.action_get_events(action):
				if binding is InputEventJoypadButton:
					has_pad = true
			runner.check(has_pad, "pad binding exists: " + action)
	var unrelated: InputEventKey = InputEventKey.new()
	unrelated.physical_keycode = KEY_Z
	runner.check(not InputMap.event_is_action(unrelated, "interact"), "unmapped key does not interact")
	for action in ["ui_accept", "ui_cancel", "ui_left", "ui_right", "ui_up", "ui_down"]:
		runner.check(InputMap.has_action(action), "built-in UI action retained: " + action)
	var button: InputEventJoypadButton = InputEventJoypadButton.new()
	button.button_index = JOY_BUTTON_A
	button.pressed = true
	runner.check(InputMap.event_is_action(button, "interact"), "pad south maps to interact")
	button.button_index = JOY_BUTTON_B
	runner.check(not InputMap.event_is_action(button, "interact"), "unmapped pad button does not interact")


func _reload(runner: SceneTree) -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	var initial_children: int = runner.root.get_child_count()
	for cycle in range(2):
		var instance: Node = packed.instantiate()
		runner.root.add_child(instance)
		runner.check(instance.get_node("CameraRig/Camera3D").current, "camera active after scene instantiation")
		runner.check(instance.get_node("KeyLight").visible, "light active after scene instantiation")
		instance.free()
		runner.check(runner.root.get_child_count() == initial_children, "scene cleanup does not leak nodes")
