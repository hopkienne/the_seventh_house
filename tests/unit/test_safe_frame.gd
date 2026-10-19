extends RefCounted

func get_cases(runner: SceneTree) -> Dictionary:
	return {"aspect_policy": _policy.bind(runner), "safe_ui_and_rejection": _ui.bind(runner)}

func _policy(runner: SceneTree) -> void:
	runner.check(ProjectSettings.get_setting("display/window/stretch/aspect", "UNSET") == "keep", "explicit keep-aspect cinematic policy")
	runner.check(ProjectSettings.get_setting("display/window/stretch/mode") == "canvas_items", "canvas-items scaling retained")

func _ui(runner: SceneTree) -> void:
	if not ResourceLoader.exists("res://scenes/ui/safe_frame.tscn"):
		runner.check(false, "reusable safe-frame container exists")
		return
	var frame: Control = load("res://scenes/ui/safe_frame.tscn").instantiate()
	runner.root.add_child(frame)
	var probe := Label.new()
	probe.text = "TƯƠNG TÁC / INTERACT"
	frame.add_child(probe)
	await runner.process_frame
	await runner.process_frame
	var inner: Rect2 = frame.call("get_safe_rect")
	runner.check(inner.has_area() and inner.size.x < frame.size.x and inner.size.y < frame.size.y, "safe frame reserves all four edges")
	runner.check(inner.encloses(probe.get_global_rect()), "child UI lays out inside safe frame")
	var initial: Rect2 = inner
	var settings: Resource = load("res://config/tuning/ui_safe_frame.tres").duplicate()
	settings.set("margin_fraction", Vector2(0.6, 0.05))
	runner.check(not frame.call("configure", settings), "unsafe margin fraction rejected")
	runner.check(not frame.call("configure", null), "null safe-frame settings rejected")
	runner.check(frame.call("get_safe_rect").is_equal_approx(initial), "invalid settings retain accepted layout")
	frame.queue_free()
	await runner.process_frame
