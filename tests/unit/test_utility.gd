extends RefCounted

const Reader = preload("res://scripts/core/json_reader.gd")


func get_cases(runner: SceneTree) -> Dictionary:
	return {"valid_runtime_json": func() -> void:
		var result: Dictionary = Reader.read_object("res://data/runtime/product.json")
		runner.check(result.ok, "actual runtime JSON readable")
		runner.check(result.get("value", {}).get("product_id") == "the_seventh_house", "runtime ID preserved"),
		"malformed_json": func() -> void:
			var result: Dictionary = Reader.read_object("res://tests/fixtures/malformed_json.txt")
			runner.check(not result.ok, "malformed JSON rejected")
			runner.check(result.error == "INVALID_JSON", "malformed failure reason"),
		"non_object_json": func() -> void:
			var result: Dictionary = Reader.read_object("res://tests/fixtures/array_json.txt")
			runner.check(not result.ok and result.error == "EXPECTED_OBJECT", "array cannot masquerade as object"),
		"missing_json": func() -> void:
			var result: Dictionary = Reader.read_object("res://tests/fixtures/does_not_exist.json")
			runner.check(not result.ok and result.error == "NOT_FOUND", "missing file explicit failure")}
