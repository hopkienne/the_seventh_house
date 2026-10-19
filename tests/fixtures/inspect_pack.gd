extends SceneTree
## Run against a separate empty project so source files cannot mask pack exclusions.


func _init() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if args.size() != 1 or not ProjectSettings.load_resource_pack(args[0], false):
		printerr("Cannot mount requested pack")
		quit(1)
		return
	var files: Array[String] = []
	_walk("res://", files)
	var forbidden: Array[String] = []
	for path in files:
		for prefix in ["res://builds/", "res://build_manifest/", "res://PACKAGE_CHECK.json", "res://tests/", "res://tools/", "res://reports/", "res://plan/", "res://state/", "res://specs/", "res://art/source/", "res://audio/source/", "res://config/test_environment", "res://config/agent_capabilities", "res://config/permissions", "res://config/toolchain"]:
			if path.begins_with(prefix):
				forbidden.append(path)
	var runtime_data: bool = FileAccess.file_exists("res://data/runtime/product.json")
	var scene: bool = ResourceLoader.exists("res://scenes/main.tscn")
	var result: Dictionary = {"files": files, "forbidden": forbidden,
		"runtime_data_included": runtime_data, "main_scene_included": scene,
		"result": "PASS" if forbidden.is_empty() and runtime_data and scene else "FAIL"}
	print("PACK_REPORT ", JSON.stringify(result))
	quit(0 if result.result == "PASS" else 1)


func _walk(directory: String, files: Array[String]) -> void:
	var access: DirAccess = DirAccess.open(directory)
	if access == null:
		return
	for name in access.get_files():
		files.append(directory.path_join(name))
	for name in access.get_directories():
		_walk(directory.path_join(name), files)
