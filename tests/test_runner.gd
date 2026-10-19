extends SceneTree
## Project test entrypoint. Engine's --test flag is deliberately not used.

var assertions: int = 0
var failures: Array[String] = []
var cases_run: int = 0
const SUITES: Dictionary = {"bootstrap": "", "scene": "res://tests/unit/test_scene.gd",
	"utilities": "res://tests/unit/test_utility.gd", "asset_import": "res://tests/unit/test_asset_import.gd"}


func _init() -> void:
	call_deferred("_run")


func check(condition: bool, message: String) -> void:
	assertions += 1
	if not condition:
		failures.append(message)
		printerr("ASSERTION FAILED: ", message)


func _run() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if args == PackedStringArray(["--list-suites"]):
		print("SUITE_REGISTRY ", JSON.stringify(SUITES.keys()))
		quit(0)
		return
	var suite: String = ""
	var filter: String = ""
	var fixture: String = ""
	var index: int = 0
	while index < args.size():
		var option: String = args[index]
		if option not in ["--suite", "--filter", "--fixture"] or index + 1 >= args.size():
			failures.append("Invalid runner argument: " + option)
			_finish(suite, 2)
			return
		index += 1
		match option:
			"--suite": suite = args[index]
			"--filter": filter = args[index]
			"--fixture": fixture = args[index]
		index += 1
	if not SUITES.has(suite):
		failures.append("Unknown suite: " + suite)
		_finish(suite, 2)
		return
	var cases: Dictionary = {"project_contract": _test_project, "toolchain_contract": _test_toolchain}
	# Callables hold weak object references. Keep providers alive through execution.
	var providers: Array[RefCounted] = []
	if not str(SUITES[suite]).is_empty():
		var provider: RefCounted = load(SUITES[suite]).new()
		providers.append(provider)
		cases = provider.get_cases(self)
	if not fixture.is_empty():
		if not fixture.begins_with("res://tests/fixtures/") or not ResourceLoader.exists(fixture):
			failures.append("Invalid fixture path: " + fixture)
			_finish(suite, 2)
			return
		var script: Script = load(fixture)
		var provider: RefCounted = script.new()
		providers.append(provider)
		cases = provider.get_cases(self)
	for case_id: String in cases:
		if not filter.is_empty() and case_id != filter:
			continue
		cases_run += 1
		print("CASE ", suite, "/", case_id)
		var execute: Callable = cases[case_id]
		if not execute.is_valid():
			failures.append("Invalid case callable: " + case_id)
			continue
		execute.call()
	if cases_run == 0 or assertions == 0:
		failures.append("Zero tests/assertions cannot pass")
	_finish(suite, 0 if failures.is_empty() else 1)


func _test_project() -> void:
	check(FileAccess.file_exists("res://project.godot"), "project config exists")
	check(ProjectSettings.get_setting("rendering/renderer/rendering_method") == "forward_plus", "Forward+ baseline")
	check(ProjectSettings.get_setting("physics/common/physics_ticks_per_second") == 60, "fixed 60 Hz physics")
	check(is_equal_approx(float(ProjectSettings.get_setting("physics/3d/default_gravity")), 9.8), "3D gravity")
	check(ProjectSettings.get_setting("display/window/size/viewport_width") == 1920, "1920 viewport width")
	check(ProjectSettings.get_setting("display/window/size/viewport_height") == 1080, "1080 viewport height")


func _test_toolchain() -> void:
	var text: String = FileAccess.get_file_as_string("res://config/toolchain.lock.json")
	var parsed: Variant = JSON.parse_string(text)
	check(parsed is Dictionary, "toolchain lock parses as object")
	if not parsed is Dictionary:
		return
	var lock: Dictionary = parsed
	var actual: Dictionary = Engine.get_version_info()
	check(lock.get("godot_version") == "4.7.2", "lock exact pin")
	check(str(actual.get("major")) + "." + str(actual.get("minor")) + "." + str(actual.get("patch")) == lock.get("godot_version"), "runtime matches lock")
	check(actual.get("status") == "stable", "stable channel")
	check(actual.get("hash") == lock.get("engine_commit"), "engine commit matches verified binary")
	check(lock.get("renderer") == "forward_plus", "renderer lock")
	check(lock.get("release_target") == "windows_x86_64", "Windows x64 target")
	check(lock.get("export_templates_version") == "4.7.2.stable", "matching templates lock")
	check(str(lock.get("editor_sha256", "")).length() == 64, "editor checksum recorded")
	check(str(lock.get("templates_archive_sha256", "")).length() == 64, "templates checksum recorded")
	check(lock.get("templates_verified", false) == true, "templates download verified")
	check(lock.get("templates_archive_sha256") == lock.get("templates_expected_sha256"), "templates archive matches official digest")
	var template_root: String = "res://" + str(lock.get("templates_root", "missing"))
	check(FileAccess.get_file_as_string(template_root + "/version.txt").strip_edges() == "4.7.2.stable", "actual templates version")
	check(FileAccess.file_exists(template_root + "/windows_debug_x86_64.exe"), "Windows x64 debug template exists")
	check(FileAccess.file_exists(template_root + "/windows_release_x86_64.exe"), "Windows x64 release template exists")


func _finish(suite: String, code: int) -> void:
	print("TEST_REPORT ", JSON.stringify({"suite": suite, "tests": cases_run,
		"registered_suites": SUITES.keys(), "executed": cases_run,
		"assertions": assertions, "failed": failures.size(), "skipped": 0,
		"failures": failures, "result": "PASS" if code == 0 else "FAIL"}))
	quit(code)
