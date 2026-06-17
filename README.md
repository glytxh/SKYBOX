# SKYBOX v1.2 — Render Modes

**SKYBOX** is a small terminal-based FITS viewer for public sky-survey data. It resolves an object name or ICRS coordinate, pulls a Pan-STARRS cutout, and renders it as coloured ASCII inside the terminal.

It is not a scientific reduction pipeline. It is a lightweight astronomical viewing instrument: part sky atlas, part terminal toy, part public-survey data window.

## New in v1.2

- Added live render-mode cycling with `r`
- Added `basic`, `rich`, and `block` render styles
- Improved colour handling for blend mode
- Updated title/menu presentation
- Updated internal versioning to `1.2`
- Added cleaner in-app help for render controls

## Render modes

| Mode | Description |
|---|---|
| `basic` | Original punctuation-style ASCII render |
| `rich` | Denser texture for more image detail |
| `block` | Shaded block mosaic using `░▒▓█` characters |

## Band modes

| Mode | Data | Use |
|---|---|---|
| `short` | Pan-STARRS `g` | Blue-green optical view |
| `mid` | Pan-STARRS `i` | Mid optical view |
| `long` | Pan-STARRS `y` | Red / near-infrared view |
| `blend` | Pan-STARRS DR1 colour | Composite colour/luminance view |

## Controls

| Key | Action |
|---|---|
| `z` | Cycle zoom |
| `b` | Cycle brightness |
| `c` | Cycle contrast |
| `r` | Cycle render mode |
| `m` | Toggle metadata |
| `h` | Toggle help |
| `k` | Show cache |
| `n` | New target |
| `q` | Quit |

## Good test targets

| Target | Suggested mode | Notes |
|---|---|---|
| `m101` | `blend` / `atlas` | Large spiral galaxy |
| `m51` | `blend` / `atlas` | Whirlpool galaxy |
| `m13` | `mid` / `field` | Globular cluster |
| `ngc 891` | `mid` / `field` | Edge-on galaxy |
| `m42` | `blend` / `survey` | Bright nebula region |
| `m31` | `blend` / `survey` | Large galaxy field |
| `pleiades` | `short` / `survey` | Bright star field |

## Install

```bash
git clone https://github.com/glytxh/SKYBOX.git
cd SKYBOX
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 doctor.py
python3 run.py
