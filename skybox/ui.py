from pathlib import Path
from rich import box
from astropy.coordinates import SkyCoord
import astropy.units as u
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.text import Text
from skybox.version import APP_NAME, APP_VERSION, APP_CODENAME

from skybox.config import SURVEYS


FRAME_WIDTH = 100
PANEL_WIDTH = 104

console = Console(soft_wrap=False)

def make_theme(name, primary, soft, accent, white, dim, logo):
    return {
        "name": name,
        "primary": primary,
        "primary_bold": f"bold {primary}",
        "soft": soft,
        "accent": accent,
        "white": white,
        "dim": f"dim {dim}",
        "border": f"bold {primary}",
        "table_border": primary,
        "logo": logo,
    }


BOOT_THEMES = [
    make_theme(
        "amber",
        "rgb(255,176,72)",
        "rgb(255,198,112)",
        "rgb(255,112,48)",
        "rgb(255,232,196)",
        "rgb(190,145,95)",
        [
            "rgb(255,220,150)",
            "rgb(255,198,112)",
            "rgb(255,176,72)",
            "rgb(255,146,54)",
            "rgb(255,112,48)",
            "rgb(210,74,32)",
        ],
    ),
    make_theme(
        "ember",
        "rgb(255,132,64)",
        "rgb(255,174,102)",
        "rgb(218,74,42)",
        "rgb(255,226,196)",
        "rgb(185,116,82)",
        [
            "rgb(255,214,166)",
            "rgb(255,174,102)",
            "rgb(255,132,64)",
            "rgb(238,96,50)",
            "rgb(200,62,38)",
            "rgb(135,42,32)",
        ],
    ),
    make_theme(
        "brass",
        "rgb(225,184,92)",
        "rgb(246,210,126)",
        "rgb(188,126,52)",
        "rgb(246,232,190)",
        "rgb(166,139,88)",
        [
            "rgb(250,232,172)",
            "rgb(246,210,126)",
            "rgb(225,184,92)",
            "rgb(196,146,66)",
            "rgb(154,104,45)",
            "rgb(112,76,36)",
        ],
    ),
    make_theme(
        "rose-gold",
        "rgb(255,168,132)",
        "rgb(255,202,178)",
        "rgb(226,104,92)",
        "rgb(255,232,218)",
        "rgb(190,128,116)",
        [
            "rgb(255,226,206)",
            "rgb(255,202,178)",
            "rgb(255,168,132)",
            "rgb(236,126,104)",
            "rgb(196,82,78)",
            "rgb(128,56,68)",
        ],
    ),
    make_theme(
        "dusk",
        "rgb(238,150,92)",
        "rgb(255,186,122)",
        "rgb(176,96,118)",
        "rgb(244,222,202)",
        "rgb(166,122,116)",
        [
            "rgb(255,214,162)",
            "rgb(255,186,122)",
            "rgb(238,150,92)",
            "rgb(206,112,94)",
            "rgb(176,96,118)",
            "rgb(112,72,112)",
        ],
    ),
    make_theme(
        "green",
        "rgb(126,220,128)",
        "rgb(172,246,168)",
        "rgb(78,176,116)",
        "rgb(220,255,218)",
        "rgb(118,168,126)",
        [
            "rgb(226,255,214)",
            "rgb(172,246,168)",
            "rgb(126,220,128)",
            "rgb(78,176,116)",
            "rgb(48,132,96)",
            "rgb(34,86,72)",
        ],
    ),
    make_theme(
        "blue",
        "rgb(100,178,255)",
        "rgb(156,214,255)",
        "rgb(92,118,230)",
        "rgb(220,238,255)",
        "rgb(112,142,184)",
        [
            "rgb(220,244,255)",
            "rgb(156,214,255)",
            "rgb(100,178,255)",
            "rgb(78,138,236)",
            "rgb(92,118,230)",
            "rgb(52,72,150)",
        ],
    ),
    make_theme(
        "purple",
        "rgb(186,136,255)",
        "rgb(218,188,255)",
        "rgb(226,104,220)",
        "rgb(240,224,255)",
        "rgb(156,126,184)",
        [
            "rgb(244,226,255)",
            "rgb(218,188,255)",
            "rgb(186,136,255)",
            "rgb(150,104,232)",
            "rgb(226,104,220)",
            "rgb(104,70,160)",
        ],
    ),
]


_BOOT_THEME = None

SKY_CYAN = BOOT_THEMES[0]["primary"]
SKY_CYAN_BOLD = BOOT_THEMES[0]["primary_bold"]
SKY_CYAN_SOFT = BOOT_THEMES[0]["soft"]
SKY_MAGENTA = BOOT_THEMES[0]["accent"]
SKY_WHITE = BOOT_THEMES[0]["white"]
SKY_DIM = BOOT_THEMES[0]["dim"]
SKY_BORDER = BOOT_THEMES[0]["border"]
SKY_TABLE_BORDER = BOOT_THEMES[0]["table_border"]
SKY_LOGO_GRADIENT = BOOT_THEMES[0]["logo"]


def activate_boot_theme():
    """
    Select one UI colour theme per app launch.

    The theme advances once when the title screen first opens, then stays
    fixed until SKYBOX quits. Viewer image rendering is not affected.
    """
    global _BOOT_THEME
    global SKY_CYAN, SKY_CYAN_BOLD, SKY_CYAN_SOFT, SKY_MAGENTA
    global SKY_WHITE, SKY_DIM, SKY_BORDER, SKY_TABLE_BORDER, SKY_LOGO_GRADIENT

    if _BOOT_THEME is not None:
        return _BOOT_THEME

    state_path = Path("cache/theme_cycle.txt")
    state_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        previous_index = int(state_path.read_text().strip())
    except Exception:
        previous_index = -1

    index = (previous_index + 1) % len(BOOT_THEMES)
    state_path.write_text(str(index))

    theme = BOOT_THEMES[index]
    _BOOT_THEME = theme

    SKY_CYAN = theme["primary"]
    SKY_CYAN_BOLD = theme["primary_bold"]
    SKY_CYAN_SOFT = theme["soft"]
    SKY_MAGENTA = theme["accent"]
    SKY_WHITE = theme["white"]
    SKY_DIM = theme["dim"]
    SKY_BORDER = theme["border"]
    SKY_TABLE_BORDER = theme["table_border"]
    SKY_LOGO_GRADIENT = theme["logo"]

    return theme


def theme_style(name):
    activate_boot_theme()
    return _BOOT_THEME.get(name, "")


def heavy_box_line(left, fill, right, width=FRAME_WIDTH):
    return left + (fill * width) + right


def show_title():
    theme = activate_boot_theme()
    console.clear()

    logo = [
        "███████╗██╗  ██╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗",
        "██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔═══██╗╚██╗██╔╝",
        "███████╗█████╔╝  ╚████╔╝ ██████╔╝██║   ██║ ╚███╔╝ ",
        "╚════██║██╔═██╗   ╚██╔╝  ██╔══██╗██║   ██║ ██╔██╗ ",
        "███████║██║  ██╗   ██║   ██████╔╝╚██████╔╝██╔╝ ██╗",
        "╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝",
    ]

    gradient = SKY_LOGO_GRADIENT

    body = Text()
    body.append("\n")

    for index, line in enumerate(logo):
        body.append(line, style=f"bold {gradient[index % len(gradient)]}")
        body.append("\n")

    body.append("\n")
    body.append(f"v{APP_VERSION}", style=SKY_WHITE)
    body.append(" · ", style="dim")
    body.append(APP_CODENAME, style=SKY_MAGENTA)
    body.append("\n\n")

    body.append("Object name", style=SKY_WHITE)
    body.append("  /  ", style=SKY_DIM)
    body.append("ICRS coordinates", style=SKY_WHITE)
    body.append("  /  ", style=SKY_DIM)
    body.append("catalog", style=SKY_CYAN_SOFT)
    body.append("  →  ", style=SKY_DIM)
    body.append("ASCII skybox", style=SKY_WHITE)
    body.append("\n")
    body.append("Type ", style=SKY_DIM)
    body.append("c", style=SKY_CYAN_SOFT)
    body.append(" or ", style=SKY_DIM)
    body.append("catalog", style=SKY_CYAN_SOFT)
    body.append(" to browse built-in targets", style=SKY_DIM)
    body.append("\n\n")

    body.append("Bands: ", style=SKY_DIM)
    body.append("short", style=SKY_CYAN_BOLD)
    body.append(" / ", style="dim")
    body.append("mid", style=SKY_WHITE)
    body.append(" / ", style="dim")
    body.append("long", style=SKY_MAGENTA)
    body.append(" / ", style="dim")
    body.append("blend", style=SKY_MAGENTA)

    body.append("\n")

    body.append("Render: ", style=SKY_DIM)
    body.append("basic", style=SKY_WHITE)
    body.append(" · ", style="dim")
    body.append("rich", style=SKY_CYAN_SOFT)
    body.append(" · ", style="dim")
    body.append("block", style=SKY_MAGENTA)

    body.append("      ", style="dim")

    body.append("View: ", style=SKY_DIM)
    body.append("small", style=SKY_WHITE)
    body.append(" · ", style="dim")
    body.append("wide", style=SKY_CYAN_SOFT)
    body.append("\n")

    panel = Panel(
        Align.center(body),
        title=Text("  SKYBOX  ", style=SKY_BORDER),
        subtitle=Text(f" public sky-survey terminal viewer · {theme['name']} ", style=SKY_DIM),
        border_style=SKY_BORDER,
        box=box.DOUBLE,
        padding=(1, 4),
        width=88,
    )

    console.print()
    console.print(Align.center(panel))
    console.print()

def choose_survey():
    ordered_keys = ["short", "mid", "long", "blend"]

    table = Table(
        title="Band mode",
        width=PANEL_WIDTH,
        show_lines=False,
        border_style=SKY_TABLE_BORDER,
    )

    table.add_column("#", justify="right", no_wrap=True, style="bold")
    table.add_column("Band", no_wrap=True, style="bold")
    table.add_column("Role", no_wrap=True)
    table.add_column("Data")

    for index, key in enumerate(ordered_keys, start=1):
        survey = SURVEYS[key]

        if survey.ps1_filter:
            band = f"Pan-STARRS {survey.ps1_filter}"
        else:
            band = "Pan-STARRS DR1 colour"

        table.add_row(str(index), key, survey.wavelength, band)

    console.print(table)

    console.print("[bold yellow]Note:[/bold yellow] blend mode only works with [bold]atlas[/bold] or [bold]survey[/bold] field scales.", style="dim")
    console.print("[dim]Pick a number, type a band name, or q to cancel. Default: 4 blend.[/dim]")

    choice = console.input("\n[bold cyan]Band[/bold cyan] › ").strip().lower()

    if choice in {"q", "quit", "exit"}:
        raise KeyboardInterrupt

    if choice == "":
        choice = "4"

    number_map = {
        "1": "short",
        "2": "mid",
        "3": "long",
        "4": "blend",
    }

    choice = number_map.get(choice, choice)

    if choice not in SURVEYS:
        raise ValueError(f"Unknown band mode: {choice}")

    return SURVEYS[choice]

def choose_field_preset():
    field_rows = [
        ("core", "0.062°", "native PS1 FITS", "close target / core"),
        ("field", "0.167°", "native PS1 FITS", "standard object field"),
        ("wide", "0.417°", "native PS1 FITS", "widest native cutout"),
        ("atlas", "0.800°", "Pan-STARRS HiPS", "large-object morphology"),
        ("survey", "2.400°", "Pan-STARRS HiPS", "broad context"),
    ]

    table = Table(
        title="Field size",
        width=PANEL_WIDTH,
        show_lines=False,
        border_style=SKY_TABLE_BORDER,
    )

    table.add_column("#", justify="right", no_wrap=True, style="bold")
    table.add_column("Field", no_wrap=True, style="bold")
    table.add_column("Width", no_wrap=True)
    table.add_column("Source")
    table.add_column("Use")

    for index, row in enumerate(field_rows, start=1):
        table.add_row(str(index), *row)

    console.print(table)

    console.print("[bold yellow]Note:[/bold yellow] blend requires [bold]atlas[/bold] or [bold]survey[/bold]. Use short/mid/long for core, field, or wide.", style="dim")
    console.print("[dim]Pick a number, type a field name, or q to cancel. Default: 4 atlas.[/dim]")

    choice = console.input("\n[bold cyan]Field[/bold cyan] › ").strip().lower()

    if choice in {"q", "quit", "exit"}:
        raise KeyboardInterrupt

    if choice == "":
        choice = "4"

    number_map = {
        "1": "core",
        "2": "field",
        "3": "wide",
        "4": "atlas",
        "5": "survey",
    }

    legacy = {
        "tight": "core",
        "normal": "field",
        "grand": "survey",
    }

    choice = number_map.get(choice, choice)
    choice = legacy.get(choice, choice)

    valid = {row[0] for row in field_rows}

    if choice not in valid:
        raise ValueError(f"Unknown field size: {choice}")

    return choice

def crop_or_pad_text_line(line, width):
    if isinstance(line, Text):
        plain = line.plain[:width]
        result = Text()

        for index, char in enumerate(plain):
            try:
                style = line.get_style_at_offset(console, index)
            except Exception:
                style = None
            result.append(char, style=style)

        visible_width = result.cell_len

        if visible_width < width:
            result.append(" " * (width - visible_width))

        return result

    text = str(line)[:width].ljust(width)
    return Text(text)



def show_ascii_frame(lines, frame_width=None):
    frame_width = frame_width or FRAME_WIDTH

    console.print("╔" + ("═" * frame_width) + "╗")

    for line in lines:
        safe_line = crop_or_pad_text_line(line, frame_width)
        console.print(Text("║") + safe_line + Text("║"))

    console.print("╚" + ("═" * frame_width) + "╝")

def compact_path(path):
    text = str(path)
    if len(text) <= 56:
        return text
    return "…" + text[-55:]


def clean_source_note(note):
    note = str(note)
    note = note.replace(" via CDS HiPS.", "")
    note = note.replace(" from cache.", " cache")
    return note


def show_metadata(target, survey, fetch_result, metadata):
    icrs = format_icrs(target)

    target_table = Table(show_header=False, box=None, width=49)
    target_table.add_column("Field", style="bold", no_wrap=True, width=10)
    target_table.add_column("Value", overflow="fold")

    target_table.add_row("Object", str(target.name))
    target_table.add_row("Type", str(metadata.get("object_type", "unknown")))
    target_table.add_row("ICRS", icrs["compact"])
    target_table.add_row("Degrees", f"{icrs['ra_deg']}  {icrs['dec_deg']}")

    survey_table = Table(show_header=False, box=None, width=49)
    survey_table.add_column("Field", style="bold", no_wrap=True, width=12)
    survey_table.add_column("Value", overflow="fold")

    if survey.ps1_filter:
        band_text = survey.ps1_filter
    else:
        band_text = "+".join(survey.ps1_filters)

    survey_table.add_row("Mode", survey.key)
    survey_table.add_row("Band", band_text)
    survey_table.add_row("Field", f"{fetch_result.requested_field} / {fetch_result.actual_fov_deg:.3f}°")
    survey_table.add_row("Source", clean_source_note(fetch_result.note))
    survey_table.add_row("File", compact_path(fetch_result.path))

    outer = Table.grid(expand=False)
    outer.add_column(width=51)
    outer.add_column(width=51)

    outer.add_row(
        Panel(target_table, title="Target", border_style=SKY_TABLE_BORDER, width=51),
        Panel(survey_table, title="Image", border_style=SKY_TABLE_BORDER, width=51),
    )

    console.print(outer)


def show_error(error):
    console.print(Panel(Text(str(error)), title="ERROR", border_style="red", width=PANEL_WIDTH))



def show_ascii_frame_with_overlay(lines, overlay_lines=None, overlay_x=3, overlay_y=3, frame_width=None):
    frame_width = frame_width or FRAME_WIDTH
    working = [crop_or_pad_text_line(line, frame_width) for line in lines]

    def stamp_segment(row_index, x_start, segment_text, style):
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

    if overlay_lines:
        card_h = len(overlay_lines)
        card_w = max(len(line) for line in overlay_lines)

        shadow_style = "white on grey7"

        for i in range(card_h):
            y = overlay_y + i + 1
            x = overlay_x + card_w
            stamp_segment(y, x, "  ", shadow_style)

        y = overlay_y + card_h
        x = overlay_x + 2
        stamp_segment(y, x, " " * max(0, card_w - 1), shadow_style)

        for i, overlay_line in enumerate(overlay_lines):
            y = overlay_y + i
            fragment = overlay_line[: max(0, frame_width - overlay_x)]
            stamp_segment(y, overlay_x, fragment, "bold white on grey11")

    console.print(Text("╔" + ("═" * frame_width) + "╗", style="bold cyan"))

    for line in working:
        console.print(Text("║", style="bold cyan") + line + Text("║", style="bold cyan"))

    console.print(Text("╚" + ("═" * frame_width) + "╝", style="bold cyan"))

def metadata_overlay_lines(target, survey, fetch_result, metadata):
    """
    Compact metadata card designed to be stamped over the image.
    Does not assume a specific Target object shape.
    """
    object_type = metadata.get("object_type") or "unknown"
    file_name = fetch_result.path.name

    ra_deg = getattr(target, "ra_deg", None)
    dec_deg = getattr(target, "dec_deg", None)

    if ra_deg is None:
        ra_deg = getattr(target, "ra", None)

    if dec_deg is None:
        dec_deg = getattr(target, "dec", None)

    if ra_deg is not None and dec_deg is not None:
        coord_text = f"RA {float(ra_deg):.5f}  Dec {float(dec_deg):+.5f}"
    else:
        coord_text = "unknown"

    fov = getattr(fetch_result, "actual_fov_deg", None)
    size_px = getattr(fetch_result, "size_px", None)

    if fov is not None and size_px is not None:
        fov_text = f"{float(fov):.3f} deg · {size_px}px"
    elif fov is not None:
        fov_text = f"{float(fov):.3f} deg"
    else:
        fov_text = fetch_result.requested_field

    rows = [
        "╔══════════════════════════════════════════════╗",
        "│ SKYBOX METADATA                              │",
        "╠══════════════════════════════════════════════╣",
        f"│ Object : {target.name[:35]:<35} │",
        f"│ Type   : {object_type[:35]:<35} │",
        f"│ ICRS   : {coord_text[:35]:<35} │",
        f"│ Band   : {survey.key[:35]:<35} │",
        f"│ Field  : {fetch_result.requested_field[:35]:<35} │",
        f"│ FOV    : {fov_text[:35]:<35} │",
        f"│ File   : {file_name[:35]:<35} │",
        "╚══════════════════════════════════════════════╝",
    ]

    return rows



def help_overlay_lines():
    """
    Compact framed help card for the image viewer.
    """
    rows = [
        "╔══════════════════════════════════════════════╗",
        "│ SKYBOX HELP                                  │",
        "╠══════════════════════════════════════════════╣",
        "│ z  zoom              b  brightness           │",
        "│ c  contrast          r  render mode          │",
        "│ w  view size         e  export PNG           │",
        "│ m  metadata          k  cache overlay        │",
        "│ o  open cache        n  new target           │",
        "│ h  help              q  quit                 │",
        "╠══════════════════════════════════════════════╣",
        "│ render: basic / rich / block                 │",
        "│ view:   small / wide                         │",
        "╚══════════════════════════════════════════════╝",
    ]

    return rows

def cache_overlay_lines(cache_rows):
    """
    Compact cache card for the image viewer.
    """
    rows = [
        "╔══════════════════════════════════════════════╗",
        "│ SKYBOX FITS CACHE  newest 15                 │",
        "╠══════════════════════════════════════════════╣",
    ]

    if not cache_rows:
        rows.append("│ Cache is empty.                              │")
    else:
        for index, item in enumerate(cache_rows, start=1):
            name = item["name"]
            size_mb = item["size_mb"]
            line = f"{index}. {name[:30]:<30} {size_mb:>5.1f}MB"
            rows.append(f"│ {line[:44]:<44} │")

    rows.extend(
        [
            "╠══════════════════════════════════════════════╣",
            "│ Type number to open · k hides cache.         │",
            "╚══════════════════════════════════════════════╝",
        ]
    )

    return rows
