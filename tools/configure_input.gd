extends SceneTree
## Reproducible authoring operation; runtime does not rewrite project settings.


func _init() -> void:
	var definitions: Dictionary = {
		"move_left": [KEY_A, JOY_BUTTON_DPAD_LEFT, JOY_AXIS_LEFT_X, -1.0],
		"move_right": [KEY_D, JOY_BUTTON_DPAD_RIGHT, JOY_AXIS_LEFT_X, 1.0],
		"move_forward": [KEY_W, JOY_BUTTON_DPAD_UP, JOY_AXIS_LEFT_Y, -1.0],
		"move_back": [KEY_S, JOY_BUTTON_DPAD_DOWN, JOY_AXIS_LEFT_Y, 1.0],
		"run": [KEY_SHIFT, JOY_BUTTON_LEFT_SHOULDER],
		"interact": [KEY_E, JOY_BUTTON_A], "toggle_lantern": [KEY_Q, JOY_BUTTON_Y],
		"journal": [KEY_J, JOY_BUTTON_BACK], "pause": [KEY_ESCAPE, JOY_BUTTON_START],
		"hint": [KEY_H, JOY_BUTTON_RIGHT_SHOULDER], "debug_overlay": [KEY_F3],
	}
	for action: String in definitions:
		var definition: Array = definitions[action]
		var key: InputEventKey = InputEventKey.new()
		key.physical_keycode = definition[0]
		var events: Array[InputEvent] = [key]
		if definition.size() >= 2:
			var button: InputEventJoypadButton = InputEventJoypadButton.new()
			button.button_index = definition[1]
			events.append(button)
		if definition.size() == 4:
			var motion: InputEventJoypadMotion = InputEventJoypadMotion.new()
			motion.axis = definition[2]
			motion.axis_value = definition[3]
			events.append(motion)
		ProjectSettings.set_setting("input/" + action, {"deadzone": 0.2, "events": events})
	ProjectSettings.set_setting("application/run/main_scene", "res://scenes/main.tscn")
	var error: Error = ProjectSettings.save()
	print("INPUT_CONFIGURE ", JSON.stringify({"actions": definitions.size(), "save_error": error}))
	quit(0 if error == OK else 1)
