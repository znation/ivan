#!/usr/bin/env python3
"""
outline_util.py — Add a white border outline to sprite sheets for the *-outlined.png variants.

IVAN uses outlined versions of Char.png, Humanoid.png, and Item.png for display.
The outlined version adds a 1-pixel white border around every non-transparent pixel,
creating a glow/outline effect that makes sprites readable on dark dungeon backgrounds.

Usage:
    python tools/asset_gen/outline_util.py --input Graphics/Char.png --output Graphics/Char-outlined.png
    python tools/asset_gen/outline_util.py --batch  # process all *-outlined pairs
"""

import argparse
from pathlib import Path


OUTLINED_PAIRS = [
    ("Graphics/Char.png", "Graphics/Char-outlined.png"),
    ("Graphics/Humanoid.png", "Graphics/Humanoid-outlined.png"),
    ("Graphics/Item.png", "Graphics/Item-outlined.png"),
]


def add_outline(input_path: Path, output_path: Path, color=(255, 255, 255, 255)):
    """
    Add a 1-pixel outline in `color` around all non-transparent pixels.
    Input must be RGBA. Output is saved as RGBA PNG.
    """
    from PIL import Image
    import numpy as np

    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)

    alpha = data[:, :, 3]
    # Build outline mask: dilate alpha channel by 1 pixel in 4 directions
    outline_mask = np.zeros_like(alpha, dtype=bool)
    outline_mask[:-1, :] |= alpha[1:, :] > 0    # up
    outline_mask[1:, :]  |= alpha[:-1, :] > 0   # down
    outline_mask[:, :-1] |= alpha[:, 1:] > 0    # left
    outline_mask[:, 1:]  |= alpha[:, :-1] > 0   # right
    # Only apply outline where original pixel is transparent
    outline_mask &= alpha == 0

    result = data.copy()
    result[outline_mask] = color

    out_img = Image.fromarray(result, "RGBA")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(str(output_path))
    print(f"Outlined: {input_path.name} → {output_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Add white outline to IVAN sprite sheets.")
    parser.add_argument("--input", help="Input PNG path")
    parser.add_argument("--output", help="Output PNG path")
    parser.add_argument("--batch", action="store_true",
                        help="Process all standard outlined pairs (Char, Humanoid, Item)")
    parser.add_argument("--color", default="255,255,255,255",
                        help="Outline color as R,G,B,A (default: 255,255,255,255 = white)")
    args = parser.parse_args()

    r, g, b, a = [int(x) for x in args.color.split(",")]
    color = (r, g, b, a)

    repo_root = Path(__file__).parent.parent.parent

    if args.batch:
        for src, dst in OUTLINED_PAIRS:
            src_path = repo_root / src
            dst_path = repo_root / dst
            if not src_path.exists():
                print(f"SKIP (missing): {src}")
                continue
            add_outline(src_path, dst_path, color)
        return

    if not args.input or not args.output:
        parser.error("--input and --output are required (or use --batch)")

    add_outline(Path(args.input), Path(args.output), color)


if __name__ == "__main__":
    main()
