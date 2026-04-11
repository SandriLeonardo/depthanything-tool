"""
run_depth.py — Generate a depth map PNG from any input image using Depth Anything V2.

Supported formats: JPEG, PNG, WebP, BMP, TIFF, HEIC/HEIF (iPhone photos).

Usage:
    python run_depth.py --input input/photo.jpg --output output/depth.png
    python run_depth.py --input input/photo.heic --output output/depth.png --model large
"""

import argparse
from pathlib import Path
from PIL import Image
from transformers import pipeline
import numpy as np

# Register HEIC/HEIF support into Pillow (no-op if already registered)
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass  # pillow-heif not installed — HEIC files will raise a clear error below

MODELS = {
    "small":  "depth-anything/Depth-Anything-V2-Small-hf",
    "base":   "depth-anything/Depth-Anything-V2-Base-hf",
    "large":  "depth-anything/Depth-Anything-V2-Large-hf",
}


def run(input_path: str, output_path: str, model_size: str = "small") -> None:
    model_id = MODELS[model_size]
    print(f"[depth] Loading model: {model_id}")

    pipe = pipeline(task="depth-estimation", model=model_id)

    ext = Path(input_path).suffix.lower()
    if ext in (".heic", ".heif") and "pillow_heif" not in __import__("sys").modules:
        raise RuntimeError(
            "HEIC/HEIF support requires pillow-heif. "
            "It should be installed inside the container — rebuild the image."
        )

    image = Image.open(input_path).convert("RGB")
    print(f"[depth] Processing {input_path} ({image.size[0]}x{image.size[1]})")

    result = pipe(image)
    depth = result["depth"]  # PIL Image, mode "I" (32-bit int) or "F"

    # Normalise to 0–255 grayscale PNG
    depth_array = np.array(depth, dtype=np.float32)
    d_min, d_max = depth_array.min(), depth_array.max()
    if d_max > d_min:
        depth_norm = (depth_array - d_min) / (d_max - d_min) * 255.0
    else:
        depth_norm = np.zeros_like(depth_array)

    depth_uint8 = depth_norm.astype(np.uint8)
    out_img = Image.fromarray(depth_uint8, mode="L")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    out_img.save(output_path)
    print(f"[depth] Saved depth map → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Depth Anything V2 — image to depth PNG")
    parser.add_argument("--input",  required=True, help="Path to input image")
    parser.add_argument("--output", required=True, help="Path for output depth PNG")
    parser.add_argument(
        "--model",
        choices=["small", "base", "large"],
        default="small",
        help="Model size (default: small). Larger = slower but more accurate.",
    )
    args = parser.parse_args()
    run(args.input, args.output, args.model)
