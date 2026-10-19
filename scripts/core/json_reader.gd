extends RefCounted
## Data reader with explicit failure results; callers decide recovery/UI policy.


static func read_object(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {"ok": false, "error": "NOT_FOUND"}
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {"ok": false, "error": "READ_FAILED"}
	var text: String = file.get_as_text()
	file.close()
	var parser: JSON = JSON.new()
	if parser.parse(text) != OK:
		return {"ok": false, "error": "INVALID_JSON", "line": parser.get_error_line()}
	if not parser.data is Dictionary:
		return {"ok": false, "error": "EXPECTED_OBJECT"}
	return {"ok": true, "value": parser.data}
