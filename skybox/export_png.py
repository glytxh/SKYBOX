from datetime import datetime
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont
from rich.console import Console
from rich.style import Style
from rich.text import Text


EXPORT_DIR = Path("exports/png")
BORDER_STYLE = "bold cyan"
OVERLAY_STYLE = "bold white on grey11"
SHADOW_STYLE = "white on grey7"

CELL_W = 9
CELL_H = 18
PADDING_X = 14
PADDING_Y = 14


def safe_filename(text):
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "skybox"


def load_export_font():
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/Library/Fonts/Menlo.ttc",
    ]

    for path in candidates:
        try:
            return ImageFont.truetype(path, 15)
        except Exception:
            pass

    return ImageFont.load_default()


def normalise_style(style):
    if isinstance(style, Style):
        return style

    try:
        return Style.parse(str(style))
    except Exception:
        return Style()


def colour_to_rgb(colour, fallback):
    if colour is None:
        return fallback

    try:
        true = colour.get_truecolor()
        return (true.red, true.green, true.blue)
    except Exception:
        return fallback


def style_at(line, index, console):
    if isinstance(line, Text):
        try:
            return normalise_style(line.get_style_at_offset(console, index))
        except Exception:
            return Style()

    return Style()


def plain_text(line):
    if isinstance(line, Text):
        return line.plain
    return str(line)


def crop_or_pad_text_line(line, width):
    if isinstance(line, Text):
        result = line[:width]
        visible_width = len(result.plain)

        if visible_width < width:
            result.append(" " * (width - visible_width))

        return result

    return Text(str(line)[:width].ljust(width))


def stamp_segment(working, row_index, x_start, segment_text, style, frame_width):
    if not (0 <= row_index < len(working)):
        return

    if x_start >= frame_width:
        return

    segment_text = segment_text[: max(0, frame_width - x_start)]

    if not segment_text:
        return

    base_text = working[row_index]
    x_end = x_start + len(segment_text)

    before = base_text[:x_start]
    after = base_text[x_end:]

    new_line = Text()
    new_line.append_text(before)
    new_line.append(segment_text, style=style)
    new_line.append_text(after)

    working[row_index] = crop_or_pad_text_line(new_line, frame_width)


def apply_overlay(lines, overlay_lines, frame_width, overlay_x=3, overlay_y=3):
    working = [crop_or_pad_text_line(line, frame_width) for line in lines]

    if not overlay_lines:
        return working

    card_h = len(overlay_lines)
    card_w = max(len(line) for line in overlay_lines)

    for i in range(card_h):
        y = overlay_y + i + 1
        x = overlay_x + card_w
        stamp_segment(working, y, x, "  ", SHADOW_STYLE, frame_width)

    y = overlay_y + card_h
    x = overlay_x + 2
    stamp_segment(working, y, x, " " * max(0, card_w - 1), SHADOW_STYLE, frame_width)

    for i, overlay_line in enumerate(overlay_lines):
        y = overlay_y + i
        fragment = overlay_line[: max(0, frame_width - overlay_x)]
        stamp_segment(working, y, overlay_x, fragment, OVERLAY_STYLE, frame_width)

    return working


def framed_lines(lines, frame_width):
    top = Text("╔" + ("═" * frame_width) + "╗", style=BORDER_STYLE)
    bottom = Text("╚" + ("═" * frame_width) + "╝", style=BORDER_STYLE)

    rows = [top]

    for line in lines:
        row = Text("║", style=BORDER_STYLE)
        row.append_text(crop_or_pad_text_line(line, frame_width))
        row.append("║", style=BORDER_STYLE)
        rows.append(row)

    rows.append(bottom)

    return rows


def draw_text_rows(rows, output_path):
    console = Console(color_system="truecolor")
    font = load_export_font()

    char_cols = max(len(plain_text(row)) for row in rows)
    char_rows = len(rows)

    image_w = PADDING_X * 2 + char_cols * CELL_W
    image_h = PADDING_Y * 2 + char_rows * CELL_H

    image = Image.new("RGB", (image_w, image_h), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    default_fg = (220, 235, 245)
    default_bg = (0, 0, 0)

    for y, row in enumerate(rows):
        plain = plain_text(row)

        for x, char in enumerate(plain):
            style = style_at(row, x, console)
            fg = colour_to_rgb(style.color, default_fg)
            bg = colour_to_rgb(style.bgcolor, default_bg)

            px = PADDING_X + x * CELL_W
            py = PADDING_Y + y * CELL_H

            if bg != default_bg:
                draw.rectangle(
                    (px, py, px + CELL_W, py + CELL_H),
                    fill=bg,
                )

            if char != " ":
                draw.text((px, py), char, fill=fg, font=font)

    image.save(output_path)


def export_view_png(
    ascii_lines,
    target,
    survey,
    fetch_result,
    metadata,
    render_mode,
    viewport_mode,
    frame_width,
    include_metadata=False,
    overlay_lines=None,
):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    working = [crop_or_pad_text_line(line, frame_width) for line in ascii_lines]

    if include_metadata and overlay_lines:
        working = apply_overlay(working, overlay_lines, frame_width)

    rows = framed_lines(working, frame_width)

    metadata_label = "metadata" if include_metadata else "clean"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    filename = (
        f"{safe_filename(getattr(target, 'name', 'target'))}_"
        f"{safe_filename(getattr(survey, 'key', 'band'))}_"
        f"{safe_filename(getattr(fetch_result, 'requested_field', 'field'))}_"
        f"{safe_filename(viewport_mode)}_"
        f"{safe_filename(render_mode)}_"
        f"{metadata_label}_"
        f"{timestamp}.png"
    )

    output_path = EXPORT_DIR / filename
    draw_text_rows(rows, output_path)

    return output_path
