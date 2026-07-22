#!/usr/bin/env python3
"""
Generate Tolkien-esque bitmap font sheets for the game's indexed-color rawbitmap format.

Format requirements (from FeLib/Source/rawbit.cpp):
  - 250x218 pixels, 8-bit indexed PNG, exactly 256-color palette
  - Glyph for ASCII c: X = ((c-0x20) & 0xF) << 4, Y = (c-0x20) & 0xF0
  - Each glyph occupies an 8x8 pixel cell
  - Palette inversion: game index N -> PNG palette[255-N], PNG pixel value = 255-N
  - TRANSPARENT_PALETTE_INDEX = 191 -> must map to RGB(255,0,255) = TRANSPARENT_COLOR 0xF81F
  - Font.png glyphs use material color index 207 (group 0, shade 15 = full brightness).
    This lets Printf's shadow pass use ShadeCol (dark) and the main pass use Color
    (caller-supplied), giving a proper drop shadow instead of a same-colored ghost.
  - Font2/Font3 use regular palette index 0 with fixed colors — they are alternate
    font choices where the color is baked in.

Glyph source: PSF1 Linux console fonts (8×8 pixel-perfect bitmaps).
TrueType fonts are unsuitable because 8px cells have too few pixels to represent
serif/complex strokes cleanly. The Tolkien-esque aesthetic comes from the color scheme.
"""

import gzip
import os
import shutil
import struct
import numpy as np
from PIL import Image

CANVAS_W, CANVAS_H = 250, 218
CELL_W, CELL_H = 8, 8
TRANSPARENT_IDX = 191
TRANSPARENT_RGB = (255, 0, 255)  # 0xF81F in RGB565

# PSF1 font candidates — prefer Lat2 (Latin-2, covers full ASCII)
PSF_CANDIDATES = [
    '/usr/share/consolefonts/Lat2-VGA8.psf.gz',
    '/usr/share/consolefonts/Lat15-VGA8.psf.gz',
    '/usr/share/consolefonts/Lat38-VGA8.psf.gz',
]

# (filename, fixed_color_or_None, glyph_game_index)
# Font.png uses material index 207 so Printf's shadow/color passes work correctly.
# Font2/Font3 bake in a fixed color via regular palette index 0.
VARIANTS = [
    ('Font.png',  None,                 207),  # material color — caller controls tint
    ('Font2.png', (0xD4, 0xA0, 0x20),    0),  # burnished gold  — elvish/regal
    ('Font3.png', (0x8C, 0xA8, 0xC8),    0),  # cold silver-blue — mystic/grey pilgrim
]


def load_psf_glyphs(path):
    """
    Parse a PSF1 console font and return a dict mapping char code -> 8×8 bool array.
    PSF1: 2-byte magic 0x0436, 1-byte mode, 1-byte charsize, then glyph data.
    Each glyph is charsize bytes; each byte is one row, MSB = leftmost pixel.
    """
    opener = gzip.open if path.endswith('.gz') else open
    with opener(path, 'rb') as f:
        data = f.read()

    magic = struct.unpack_from('<H', data, 0)[0]
    if magic != 0x0436:
        raise ValueError(f"Not a PSF1 font (magic=0x{magic:04x}): {path}")

    charsize = data[3]
    glyphs = {}
    offset = 4
    for code in range(256):
        rows = []
        for row in range(min(charsize, CELL_H)):
            byte = data[offset + code * charsize + row]
            rows.append([(byte >> (7 - col)) & 1 for col in range(CELL_W)])
        # Pad to CELL_H rows if charsize < CELL_H
        while len(rows) < CELL_H:
            rows.append([0] * CELL_W)
        glyphs[code] = np.array(rows, dtype=bool)
    return glyphs


def build_game_palette(glyph_color):
    palette = [(0, 0, 0)] * 256
    if glyph_color is not None:
        palette[0] = glyph_color  # regular-color fonts bake glyph color here
    palette[TRANSPARENT_IDX] = TRANSPARENT_RGB
    return palette


def game_to_png_palette(game_palette):
    """Invert: PNG palette entry [255-N] = game palette color N."""
    png_palette = [(0, 0, 0)] * 256
    for n, rgb in enumerate(game_palette):
        png_palette[255 - n] = rgb
    return png_palette


def find_psf():
    for path in PSF_CANDIDATES:
        if os.path.exists(path):
            print(f"  psf font: {path}")
            return path
    raise RuntimeError(
        "No suitable PSF console font found.\n"
        "  sudo apt install console-common"
    )


def generate_font(glyph_color, glyph_game_index, output_path):
    glyphs = load_psf_glyphs(find_psf())

    # Canvas in game-space indices; start fully transparent
    canvas = np.full((CANVAS_H, CANVAS_W), TRANSPARENT_IDX, dtype=np.uint8)

    for code in range(0x20, 0x7F):
        idx = code - 0x20
        cell_x = (idx & 0xF) << 4
        cell_y = idx & 0xF0

        if cell_y + CELL_H > CANVAS_H or cell_x + CELL_W > CANVAS_W:
            continue

        glyph = glyphs.get(code)
        if glyph is None:
            continue

        for y in range(CELL_H):
            for x in range(CELL_W):
                if glyph[y, x]:
                    canvas[cell_y + y, cell_x + x] = glyph_game_index

    game_palette = build_game_palette(glyph_color)
    png_palette = game_to_png_palette(game_palette)

    png_pixels = (255 - canvas).astype(np.uint8)
    img = Image.fromarray(png_pixels, mode='P')
    flat = []
    for rgb in png_palette:
        flat.extend(rgb)
    img.putpalette(flat)
    img.save(output_path)
    print(f"  wrote {output_path}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    graphics_dir = os.path.join(repo_root, 'Graphics')
    share_dir = os.path.join(repo_root, 'share', 'vale', 'Graphics')

    for filename, color, glyph_idx in VARIANTS:
        print(f"\nGenerating {filename} ...")
        out = os.path.join(graphics_dir, filename)
        generate_font(color, glyph_idx, out)
        if os.path.isdir(share_dir):
            dest = os.path.join(share_dir, filename)
            if not os.path.samefile(out, dest):
                shutil.copy2(out, dest)
                print(f"  -> share/vale/Graphics/{filename}")


if __name__ == '__main__':
    main()
