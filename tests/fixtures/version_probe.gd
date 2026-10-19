extends SceneTree


func _init() -> void:
	print("VERSION_JSON ", JSON.stringify(Engine.get_version_info()))
	quit()
