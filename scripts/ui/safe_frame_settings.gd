class_name SafeFrameSettings
extends Resource

@export var margin_fraction: Vector2 = Vector2(0.05, 0.05)

func is_valid() -> bool:
	return margin_fraction.is_finite() and margin_fraction.x >= 0 and margin_fraction.y >= 0 \
		and margin_fraction.x <= 0.2 and margin_fraction.y <= 0.2
