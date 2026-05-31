#!/usr/bin/env python3
"""
audio_generator.py — Generate WAV sound effects using Bark (Suno) or MusicGen.

Uses Bark for short SFX/voice clips; MusicGen for music loops.
Runs on CPU or ROCm GPU (AMD Vega 48 — needs 'render' group membership).

Usage:
    # Short creature SFX (Bark):
    python tools/asset_gen/audio_generator.py \\
        --prompt "[SOUND] dark predator growl, deep bass" \\
        --output Sound/wraithstalker.wav --duration 1.0

    # Music loop (MusicGen):
    python tools/asset_gen/audio_generator.py \\
        --prompt "dark fantasy dungeon ambient music, slow ominous" \\
        --output Sound/dungeon_theme.wav --duration 10.0 --model musicgen
"""

import argparse
import sys
import os
import struct
import array
from pathlib import Path


def write_wav(path: Path, samples, sample_rate: int):
    """Write a mono float32 array to a PCM 16-bit WAV file."""
    # Convert to 16-bit PCM
    pcm = [max(-32768, min(32767, int(s * 32767))) for s in samples]
    data = array.array("h", pcm)
    num_samples = len(pcm)
    num_channels = 1
    bits_per_sample = 16
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_bytes = data.tobytes()

    with open(path, "wb") as f:
        # RIFF header
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + len(data_bytes)))
        f.write(b"WAVE")
        # fmt chunk
        f.write(b"fmt ")
        f.write(struct.pack("<I", 16))          # chunk size
        f.write(struct.pack("<H", 1))           # PCM
        f.write(struct.pack("<H", num_channels))
        f.write(struct.pack("<I", sample_rate))
        f.write(struct.pack("<I", byte_rate))
        f.write(struct.pack("<H", block_align))
        f.write(struct.pack("<H", bits_per_sample))
        # data chunk
        f.write(b"data")
        f.write(struct.pack("<I", len(data_bytes)))
        f.write(data_bytes)


def generate_bark(prompt: str, output: Path, duration: float):
    """Generate short SFX using Suno Bark."""
    from transformers import AutoProcessor, BarkModel
    import torch
    import numpy as np

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Bark: device={device}")

    processor = AutoProcessor.from_pretrained("suno/bark-small")
    model = BarkModel.from_pretrained("suno/bark-small").to(device)

    inputs = processor(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        audio_array = model.generate(**inputs, do_sample=True)

    audio_np = audio_array.cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate

    # Trim or pad to requested duration
    target_len = int(duration * sample_rate)
    if len(audio_np) > target_len:
        audio_np = audio_np[:target_len]
    elif len(audio_np) < target_len:
        audio_np = np.pad(audio_np, (0, target_len - len(audio_np)))

    output.parent.mkdir(parents=True, exist_ok=True)
    write_wav(output, audio_np.tolist(), sample_rate)
    print(f"Saved: {output}  ({duration:.1f}s @ {sample_rate}Hz)")


def generate_musicgen(prompt: str, output: Path, duration: float):
    """Generate ambient music using facebook/musicgen-small."""
    from transformers import pipeline
    import torch

    device = 0 if torch.cuda.is_available() else -1
    print(f"MusicGen: device={'cuda' if device == 0 else 'cpu'}")

    synthesiser = pipeline(
        "text-to-audio",
        model="facebook/musicgen-small",
        device=device,
    )
    music = synthesiser(prompt, forward_params={"do_sample": True, "max_new_tokens": int(duration * 50)})
    audio = music["audio"][0]  # shape: (channels, samples)
    sample_rate = music["sampling_rate"]

    # Mix to mono
    if len(audio.shape) > 1 and audio.shape[0] > 1:
        mono = audio.mean(axis=0).tolist()
    else:
        mono = audio.flatten().tolist()

    output.parent.mkdir(parents=True, exist_ok=True)
    write_wav(output, mono, sample_rate)
    print(f"Saved: {output}  ({duration:.1f}s @ {sample_rate}Hz)")


def main():
    parser = argparse.ArgumentParser(description="Generate WAV audio for IVAN replacement SFX.")
    parser.add_argument("--prompt", required=True, help="Text prompt describing the sound")
    parser.add_argument("--output", required=True, help="Output WAV path")
    parser.add_argument("--duration", type=float, default=2.0, help="Desired duration in seconds")
    parser.add_argument("--model", choices=["bark", "musicgen"], default="bark",
                        help="Model to use: bark (SFX/voice) or musicgen (music loops)")
    args = parser.parse_args()

    output = Path(args.output)

    if args.model == "bark":
        generate_bark(args.prompt, output, args.duration)
    else:
        generate_musicgen(args.prompt, output, args.duration)


if __name__ == "__main__":
    main()
