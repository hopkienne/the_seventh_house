extends RefCounted
## Explicit negative fixture; never registered in the default suite.


func get_cases(runner: SceneTree) -> Dictionary:
	return {"intentional_failure": func() -> void: runner.check(false, "negative fixture must fail")}
