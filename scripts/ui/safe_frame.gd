class_name SafeFrame
extends MarginContainer
## Children use a stable interior region of the authored16:9 content viewport.

@export var settings: SafeFrameSettings = preload("res://config/tuning/ui_safe_frame.tres")

func _ready() -> void:
	resized.connect(_refresh)
	if not configure(settings):
		printerr("SafeFrame: INVALID_SETTINGS")

func configure(next: SafeFrameSettings) -> bool:
	if next == null or not next.is_valid():
		return false
	settings = next.duplicate()
	_refresh()
	return true

func _refresh() -> void:
	var horizontal: int = roundi(size.x * settings.margin_fraction.x)
	var vertical: int = roundi(size.y * settings.margin_fraction.y)
	add_theme_constant_override("margin_left", horizontal)
	add_theme_constant_override("margin_right", horizontal)
	add_theme_constant_override("margin_top", vertical)
	add_theme_constant_override("margin_bottom", vertical)

func get_safe_rect() -> Rect2:
	var margins := Vector2(get_theme_constant("margin_left"), get_theme_constant("margin_top"))
	return Rect2(global_position + margins, size - margins * 2.0)
