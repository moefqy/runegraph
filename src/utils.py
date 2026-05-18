from dataclasses import asdict, dataclass
import re


HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


@dataclass
class CoverConfig:
	"""Config values used to generate a blog cover image."""

	width: int = 1000
	height: int = 420
	background_color: str = "#0f172a"
	text_color: str = "#dedadc"
	font_size_title: int = 45
	font_size_subtitle: int = 15
	vertical_margin: int = 15
	line_gap: int = 15
	output_format: str = "PNG"
	output_dir: str = "./output"
	logo_size: int = 30
	logo_margin: int = 15


# _ensure_* functions for validating config values
def _ensure_positive_int(name: str, value: int) -> int:
	if not isinstance(value, int) or value <= 0:
		raise ValueError(f"{name} must be a positive integer")
	return value


def _ensure_non_negative_int(name: str, value: int) -> int:
	if not isinstance(value, int) or value < 0:
		raise ValueError(f"{name} must be a non-negative integer")
	return value


def _ensure_hex_color(name: str, value: str) -> str:
	if not isinstance(value, str) or not HEX_COLOR_PATTERN.match(value):
		raise ValueError(
			f"{name} must be a hex color like #fff or #fffb29"
		)
	return value

# Validate and construct a CoverConfig from user-provided style inputs.
def set_cover_config(
	width: int = 1000,
	height: int = 420,
	background_color: str = "#0f172a",
	text_color: str = "#dedadc",
	font_size_title: int = 45,
	font_size_subtitle: int = 15,
	vertical_margin: int = 15,
	line_gap: int = 15,
	output_format: str = "PNG",
	output_dir: str = "./output",
	logo_size: int = 30,
	logo_margin: int = 15,
) -> CoverConfig:
	"""Create validated cover config from editable inputs.

	This is intended to be used in a notebook cell where users can quickly
	adjust style values without touching generator internals.
	"""

	normalized_format = output_format.upper()
	if normalized_format not in {"PNG", "JPG", "JPEG", "WEBP"}:
		raise ValueError("output_format must be one of: PNG, JPG, JPEG, WEBP")

	if not isinstance(output_dir, str) or not output_dir.strip():
		raise ValueError("output_dir must be a non-empty string")

	return CoverConfig(
		width=_ensure_positive_int("width", width),
		height=_ensure_positive_int("height", height),
		background_color=_ensure_hex_color("background_color", background_color),
		text_color=_ensure_hex_color("text_color", text_color),
		font_size_title=_ensure_positive_int("font_size_title", font_size_title),
		font_size_subtitle=_ensure_positive_int(
			"font_size_subtitle", font_size_subtitle
		),
		vertical_margin=_ensure_non_negative_int("vertical_margin", vertical_margin),
		line_gap=_ensure_non_negative_int("line_gap", line_gap),
		output_format=normalized_format,
		output_dir=output_dir.strip(),
		logo_size=_ensure_positive_int("logo_size", logo_size),
		logo_margin=_ensure_non_negative_int("logo_margin", logo_margin),
	)


def config_to_dict(config: CoverConfig) -> dict:
	"""Convert config dataclass to plain dictionary for logging or JSON."""

	return asdict(config)


__all__ = ["CoverConfig", "set_cover_config", "config_to_dict"]
