#!/usr/bin/env python3
"""
image_generator.py — Generate PNG sprites/textures using Flux diffusion model.

Attempts ROCm/CUDA GPU first, falls back to CPU if unavailable.
The Vega 48 GPU requires: sudo usermod -aG render $USER (then re-login).

Usage:
    python tools/asset_gen/image_generator.py \\
        --prompt "dark fantasy roguelike monster sprite, ..." \\
        --width 800 --height 600 --output Graphics/Wraithstalker.png

    # Run all must-replace items from asset_catalog.json:
    python tools/asset_gen/image_generator.py --from-catalog tools/asset_gen/asset_catalog.json
"""

import argparse
import json
import sys
import os
from pathlib import Path


def get_device():
    import torch
    # Try ROCm GPU (AMD Vega 48) — requires user in 'render' group
    if torch.cuda.is_available():
        return "cuda"
    # Check for ROCm KFD device even when cuda.is_available() says False
    if os.path.exists("/dev/kfd"):
        # Force ROCm device 0
        try:
            os.environ.setdefault("HSA_OVERRIDE_GFX_VERSION", "9.0.0")
            torch.cuda.device_count()  # trigger HIP init
            if torch.cuda.is_available():
                return "cuda"
        except Exception:
            pass
    return "cpu"


def load_pipeline(model_id: str, device: str):
    from diffusers import FluxPipeline, AutoPipelineForText2Image
    import torch

    dtype = torch.float16 if device != "cpu" else torch.float32

    try:
        pipe = FluxPipeline.from_pretrained(model_id, torch_dtype=dtype)
    except Exception:
        # Fallback to generic pipeline (works with SDXL, SD, etc.)
        pipe = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=dtype)

    pipe = pipe.to(device)
    if device != "cpu":
        pipe.enable_attention_slicing()
    return pipe


def generate_image(prompt: str, width: int, height: int, output: Path, model_id: str, steps: int):
    import torch
    device = get_device()
    print(f"Device: {device}  Model: {model_id}")
    pipe = load_pipeline(model_id, device)

    result = pipe(
        prompt=prompt,
        width=width,
        height=height,
        num_inference_steps=steps,
        generator=torch.Generator(device=device).manual_seed(42),
    )
    img = result.images[0]
    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output))
    print(f"Saved: {output}  ({width}x{height})")


def main():
    parser = argparse.ArgumentParser(description="Generate IVAN replacement sprites via Flux.")
    parser.add_argument("--prompt", help="Image generation prompt")
    parser.add_argument("--width", type=int, default=800)
    parser.add_argument("--height", type=int, default=600)
    parser.add_argument("--output", help="Output PNG path")
    parser.add_argument("--model", default="black-forest-labs/FLUX.1-schnell",
                        help="HuggingFace model ID (default: FLUX.1-schnell)")
    parser.add_argument("--steps", type=int, default=4,
                        help="Inference steps (default: 4 for schnell)")
    parser.add_argument("--from-catalog", metavar="CATALOG_JSON",
                        help="Generate all must-replace items from asset_catalog.json")
    args = parser.parse_args()

    if args.from_catalog:
        catalog_path = Path(args.from_catalog)
        catalog = json.loads(catalog_path.read_text())
        repo_root = Path(__file__).parent.parent.parent
        for entry in catalog:
            if entry.get("priority") != "must-replace":
                continue
            out_path = repo_root / entry.get("new_filename", entry["filename"])
            if out_path.exists():
                print(f"SKIP (exists): {out_path.name}")
                continue
            generate_image(
                prompt=entry["prompt"],
                width=entry["width"],
                height=entry["height"],
                output=out_path,
                model_id=args.model,
                steps=args.steps,
            )
        return

    if not args.prompt or not args.output:
        parser.error("--prompt and --output are required (or use --from-catalog)")

    generate_image(
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        output=Path(args.output),
        model_id=args.model,
        steps=args.steps,
    )


if __name__ == "__main__":
    main()
