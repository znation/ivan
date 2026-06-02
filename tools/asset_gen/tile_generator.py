#!/usr/bin/env python3
"""
tile_generator.py — AI per-tile sprite sheet regeneration for IVAN.

Loads a tile registry (built by tile_registry_builder.py), generates each
registered tile with SDXL-turbo at 1024x1024, downscales to 16x16, and
assembles back into the full sprite sheet.

Unregistered tile positions are left unchanged (original pixels preserved).

Usage:
    # Build registries first:
    ~/venv/bin/python tools/asset_gen/tile_registry_builder.py

    # Regenerate a sheet (default model: sdxl-turbo):
    ~/venv/bin/python tools/asset_gen/tile_generator.py --sheet GLTerra

    # Test a single tile before running the full sheet:
    ~/venv/bin/python tools/asset_gen/tile_generator.py --sheet GLTerra --tile 0,0

    # Regenerate all sheets (slow!):
    ~/venv/bin/python tools/asset_gen/tile_generator.py --all
"""

import argparse, json, sys, os, time
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
REGISTRY_DIR = Path(__file__).parent / "tile_registries"
GRAPHICS_DIR = REPO / "Graphics"

# Sheet name → PNG filename
SHEET_FILES = {
    "GLTerra":  "GLTerra.png",
    "OLTerra":  "OLTerra.png",
    "WTerra":   "WTerra.png",
    "Item":     "Item.png",
    "Char":     "Char.png",
    "Humanoid": "Humanoid.png",
    "Symbol":   "Symbol.png",
    "Effect":   "Effect.png",
    "Smiley":   "Smiley.png",
}

# Sheets that have derived -outlined variants to regenerate after
OUTLINED_SHEETS = {"Char", "Humanoid", "Item"}

# Special: Smiley faces are 48×48 (3×3 tiles), generated as a unit
SMILEY_FACE_SIZE = 48


def load_registry(sheet):
    path = REGISTRY_DIR / f"{sheet.lower()}_tiles.json"
    if not path.exists():
        print(f"Registry not found: {path}")
        print("Run tile_registry_builder.py first.")
        sys.exit(1)
    return json.loads(path.read_text())


def load_sheet_rgba(sheet_path):
    from PIL import Image
    img = Image.open(sheet_path)
    return img.convert("RGBA"), img


def get_original_palette(img_p):
    """Return the 256-entry palette as a flat list of 768 ints (R,G,B per entry)."""
    if img_p.mode != "P":
        return None
    return img_p.getpalette()


def save_as_indexed(rgba_img, original_palette, output_path):
    """
    Convert RGBA image back to indexed color (P mode) with 256-color palette.

    Strategy:
    - Quantize to 191 colors (indices 0–190) for visual content
    - Force index 191 = magenta (255, 0, 255) as transparent
    - Restore indices 192–255 from original palette (engine material-color zone)
    """
    from PIL import Image
    import numpy as np

    # Quantize visual content to 191 colors
    rgb_img = rgba_img.convert("RGB")
    quantized = rgb_img.quantize(colors=191, dither=0)

    # Build final 256-entry palette (flat RGB list, 768 ints)
    q_palette = list(quantized.getpalette() or [])
    # Ensure it is padded to exactly 768 entries
    q_palette = (q_palette + [0] * 768)[:768]

    if original_palette:
        orig = list(original_palette) + [0] * 768
        # Preserve original material-color zone (entries 192–255)
        for i in range(192, 256):
            q_palette[i * 3]     = orig[i * 3]
            q_palette[i * 3 + 1] = orig[i * 3 + 1]
            q_palette[i * 3 + 2] = orig[i * 3 + 2]

    # Set index 191 = magenta (transparent)
    q_palette[191 * 3]     = 255
    q_palette[191 * 3 + 1] = 0
    q_palette[191 * 3 + 2] = 255

    quantized.putpalette(q_palette)

    # Convert RGBA transparent pixels → index 191
    alpha = np.array(rgba_img)[:, :, 3]
    pix = np.array(quantized)
    pix[alpha < 128] = 191
    result = Image.fromarray(pix, mode="P")
    result.putpalette(q_palette)

    result.save(str(output_path))
    print(f"Saved: {output_path}")


def generate_tile(pipe, prompt, tile_size=16, gen_size=1024):
    """Generate one tile using the loaded pipeline. Returns a PIL Image (RGBA, tile_size×tile_size)."""
    import torch
    from PIL import Image

    result = pipe(
        prompt=prompt,
        width=gen_size,
        height=gen_size,
        num_inference_steps=1,
        guidance_scale=0.0,
        generator=torch.Generator(device="cpu").manual_seed(42),
    )
    img = result.images[0].convert("RGBA")
    # Two-step downscale: 1024 → 256 → 16 preserves more structure than one-shot
    img = img.resize((256, 256), Image.LANCZOS)
    img = img.resize((tile_size, tile_size), Image.LANCZOS)
    return img


def generate_face(pipe, prompt, face_size=48, gen_size=1024):
    """Generate a Smiley face (48×48) using the loaded pipeline."""
    import torch
    from PIL import Image

    result = pipe(
        prompt=prompt,
        width=gen_size,
        height=gen_size,
        num_inference_steps=1,
        guidance_scale=0.0,
        generator=torch.Generator(device="cpu").manual_seed(42),
    )
    img = result.images[0].convert("RGBA")
    img = img.resize((face_size, face_size), Image.LANCZOS)
    return img


def load_sdxl_pipeline(model_id="stabilityai/sdxl-turbo"):
    """Load SDXL-turbo pipeline once; reuse for all tiles."""
    # Import device detection from sibling module
    sys.path.insert(0, str(Path(__file__).parent))
    from image_generator import get_device, load_pipeline
    device = get_device()
    print(f"Loading {model_id} on {device} ...")
    pipe = load_pipeline(model_id, device)
    print("Model loaded.")
    return pipe


def process_sheet(sheet, tile_key=None, model_id="stabilityai/sdxl-turbo", dry_run=False):
    """
    Regenerate registered tiles in a sprite sheet.

    Args:
        sheet:     Sheet name (e.g. "GLTerra")
        tile_key:  If set, only regenerate this single tile ("col,row")
        model_id:  HuggingFace model ID
        dry_run:   If True, print prompts without generating
    """
    from PIL import Image

    registry = load_registry(sheet)
    sheet_file = GRAPHICS_DIR / SHEET_FILES[sheet]

    if not sheet_file.exists():
        print(f"Sheet not found: {sheet_file}")
        sys.exit(1)

    rgba_img, orig_img = load_sheet_rgba(sheet_file)
    orig_palette = get_original_palette(orig_img)
    w, h = rgba_img.size

    # Filter to requested tile or all registered tiles
    targets = {}
    if tile_key:
        if tile_key not in registry:
            print(f"Tile {tile_key} not in registry for {sheet}.")
            print(f"Available: {sorted(registry.keys())[:20]} ...")
            sys.exit(1)
        targets = {tile_key: registry[tile_key]}
    else:
        targets = registry

    print(f"Sheet: {sheet}  ({w}x{h})  Tiles to generate: {len(targets)}")

    if dry_run:
        for key, entry in sorted(targets.items()):
            print(f"  [{key}] {entry.get('name','')} — {entry.get('prompt','')[:80]}...")
        return

    pipe = load_sdxl_pipeline(model_id)

    # Special handling for Smiley: generate whole 48×48 faces, not 16×16 sub-tiles
    if sheet == "Smiley":
        _process_smiley(pipe, targets, rgba_img, orig_palette, sheet_file)
        return

    total = len(targets)
    for idx, (key, entry) in enumerate(sorted(targets.items()), 1):
        px, py = entry["pixel_x"], entry["pixel_y"]
        prompt = entry["prompt"]
        name = entry.get("name", key)

        print(f"[{idx}/{total}] ({key}) {name[:50]}")
        t0 = time.time()
        tile_img = generate_tile(pipe, prompt)
        elapsed = time.time() - t0
        print(f"  → {elapsed:.1f}s  prompt: {prompt[:60]}...")

        rgba_img.paste(tile_img, (px, py))

    save_as_indexed(rgba_img, orig_palette, sheet_file)

    # Regenerate outlined variants for Char/Humanoid/Item
    if sheet in OUTLINED_SHEETS:
        _regenerate_outlined(sheet)


def _process_smiley(pipe, targets, rgba_img, orig_palette, sheet_file):
    """
    Smiley faces are 48×48 each (3 tiles wide × 3 tiles tall).
    Generate each face once at 48×48 and paste across its 9 tile sub-regions.
    """
    from PIL import Image

    # Group tiles by face index
    faces = {}
    for key, entry in targets.items():
        fi = entry.get("_face_idx", 0)
        faces.setdefault(fi, entry)

    for face_idx in sorted(faces.keys()):
        entry = faces[face_idx]
        prompt = entry["prompt"]
        name = entry.get("name", f"face {face_idx}")
        print(f"[face {face_idx}] {name}")
        face_img = generate_face(pipe, prompt, face_size=SMILEY_FACE_SIZE)
        # Paste at face origin
        face_x = face_idx * SMILEY_FACE_SIZE
        rgba_img.paste(face_img, (face_x, 0))

    save_as_indexed(rgba_img, orig_palette, sheet_file)


def _regenerate_outlined(sheet):
    """Run outline_util.py to regenerate the -outlined variant."""
    import subprocess
    outline_script = Path(__file__).parent / "outline_util.py"
    input_file = GRAPHICS_DIR / SHEET_FILES[sheet]
    output_file = GRAPHICS_DIR / SHEET_FILES[sheet].replace(".png", "-outlined.png")
    print(f"Regenerating outlined: {output_file.name} ...")
    result = subprocess.run(
        [sys.executable, str(outline_script),
         "--input", str(input_file),
         "--output", str(output_file)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  outline_util.py error: {result.stderr[:200]}")
    else:
        print(f"  Done: {output_file.name}")


ALL_SHEETS_ORDERED = [
    "GLTerra", "WTerra", "OLTerra",
    "Symbol", "Effect", "Smiley",
    "Item", "Char", "Humanoid",
]


def main():
    parser = argparse.ArgumentParser(description="AI per-tile sprite sheet regeneration.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sheet", choices=list(SHEET_FILES.keys()),
                       help="Regenerate a single sheet")
    group.add_argument("--all", action="store_true",
                       help="Regenerate all sheets in priority order")
    parser.add_argument("--tile", metavar="COL,ROW",
                        help="Regenerate only this tile (e.g. --tile 0,0)")
    parser.add_argument("--model", default="stabilityai/sdxl-turbo",
                        help="HuggingFace model ID")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print prompts without generating")
    args = parser.parse_args()

    if args.all:
        for sheet in ALL_SHEETS_ORDERED:
            print(f"\n{'='*60}")
            print(f"Processing sheet: {sheet}")
            print(f"{'='*60}")
            process_sheet(sheet, model_id=args.model, dry_run=args.dry_run)
    else:
        process_sheet(args.sheet, tile_key=args.tile, model_id=args.model, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
