from pathlib import Path
import re
from typing import Optional, Tuple
import warnings

from PIL import Image, ImageDraw, ImageFont

from src.utils import CoverConfig

# Converts a title to a safe filename by replacing non-alphanumeric characters with underscores
def _slugify_filename(text: str) -> str:
	cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower())
	return cleaned.strip("_") or "blog_cover"

# Load a font with fallback options
def _load_font(font_path: str, size: int) -> ImageFont.ImageFont:
	if font_path:
		path = Path(font_path)
		if path.exists():
			return ImageFont.truetype(str(path), size=size)
		warnings.warn(f"Font file not found: {font_path!r}. Falling back to system fonts.")

	fallback_candidates = [
		"Arial.ttf",
		"Helvetica.ttc",
		"/System/Library/Fonts/Supplemental/Arial.ttf",
		"/System/Library/Fonts/Supplemental/Helvetica.ttc",
		"/Library/Fonts/Arial.ttf",
	]
	for candidate in fallback_candidates:
		try:
			return ImageFont.truetype(candidate, size=size)
		except OSError:
			continue

	warnings.warn(
		"No suitable system font found. Falling back to PIL default bitmap font, "
		"which may produce low-quality output."
	)
	return ImageFont.load_default()

# Calculate centered text positions for title and subtitle (with multi-line support)
def _centered_text_position(
	draw: ImageDraw.ImageDraw,
	canvas_size: Tuple[int, int],
	title: str,
	subtitle: str,
	title_font: ImageFont.ImageFont,
	subtitle_font: ImageFont.ImageFont,
	vertical_margin: int,
	line_gap: int,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
	width, height = canvas_size

	# Handle multi-line titles
	title_lines = title.split('\n')
	title_bboxes = [draw.textbbox((0, 0), line, font=title_font) for line in title_lines]

	# Calculate total title dimensions
	title_widths = [bbox[2] - bbox[0] for bbox in title_bboxes]
	title_line_height = title_bboxes[0][3] - title_bboxes[0][1]
	title_width = max(title_widths)
	title_height = title_line_height * len(title_lines) + line_gap * (len(title_lines) - 1)

	# Calculate subtitle dimensions
	subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
	subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
	subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]

	# Calculate total height and centered positions
	total_height = title_height + line_gap + subtitle_height + vertical_margin
	title_x = (width - title_width) / 2
	title_y = (height - total_height) / 2
	subtitle_x = (width - subtitle_width) / 2
	subtitle_y = title_y + title_height + line_gap + vertical_margin

	return (title_x, title_y), (subtitle_x, subtitle_y)

# Main function to generate the blog cover
def generate_blog_cover(
	title: str,
	subtitle: str,
	config: CoverConfig,
	title_font_path: str = "",
	subtitle_font_path: str = "",
	logo_path: str = "",
	output_name: Optional[str] = None,
) -> Path:
	"""Generate a blog cover image and return the output file path."""

	if not title or not title.strip():
		raise ValueError("title must be a non-empty string")
	if not subtitle or not subtitle.strip():
		raise ValueError("subtitle must be a non-empty string")

	title_stripped = title.strip()
	resolved_subtitle = subtitle.strip()

	image = Image.new("RGBA", (config.width, config.height), config.background_color)
	draw = ImageDraw.Draw(image)

	title_font = _load_font(title_font_path, config.font_size_title)
	subtitle_font = _load_font(subtitle_font_path, config.font_size_subtitle)

	(title_x, title_y), (subtitle_x, subtitle_y) = _centered_text_position(
		draw=draw,
		canvas_size=(config.width, config.height),
		title=title_stripped,
		subtitle=resolved_subtitle,
		title_font=title_font,
		subtitle_font=subtitle_font,
		vertical_margin=config.vertical_margin,
		line_gap=config.line_gap,
	)

	# Draw multi-line title
	title_lines = title_stripped.split('\n')
	_ref_bbox = draw.textbbox((0, 0), "A", font=title_font)
	line_height = _ref_bbox[3] - _ref_bbox[1]
	for i, line in enumerate(title_lines):
		line_y = title_y + i * (line_height + config.line_gap)
		# Center each line horizontally
		line_bbox = draw.textbbox((0, 0), line, font=title_font)
		line_width = line_bbox[2] - line_bbox[0]
		line_x = (config.width - line_width) / 2
		draw.text((line_x, line_y), line, font=title_font, fill=config.text_color)

	draw.text(
		(subtitle_x, subtitle_y),
		resolved_subtitle,
		font=subtitle_font,
		fill=config.text_color,
	)

	# Add logo if provided
	if logo_path:
		logo_image_path = Path(logo_path)
		if logo_image_path.exists():
			logo_img = Image.open(logo_image_path).convert("RGBA")
			logo_img.thumbnail((config.logo_size, config.logo_size), Image.Resampling.LANCZOS)
			logo_position = (config.logo_margin, config.logo_margin)
			image.paste(logo_img, logo_position, logo_img)
		else:
			warnings.warn(f"Logo file not found: {logo_path!r}. Skipping logo.")

	output_dir = Path(config.output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)

	# Determine output file name and format
	file_stem = output_name.strip() if output_name else _slugify_filename(title)
	save_format = "JPEG" if config.output_format in {"JPG", "JPEG"} else config.output_format
	extension = "jpg" if save_format == "JPEG" else save_format.lower()
	output_path = output_dir / f"{file_stem}.{extension}"

	save_format = "JPEG" if config.output_format == "JPG" else config.output_format
	if save_format == "JPEG":
		image.convert("RGB").save(output_path, format=save_format)
	else:
		image.save(output_path, format=save_format)

	return output_path

__all__ = ["generate_blog_cover"]
