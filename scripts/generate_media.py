#!/usr/bin/env python3
"""
Generate video and animated GIF thumbnails from a sequence of numbered PNG frames.

Requires ffmpeg on PATH and Pillow (PIL).

Usage:
  python scripts/generate_media.py public/images/projects/raytracer --fps 8

Outputs (inside the same directory):
  hero.mp4            – 1920×1080 h264 video, web-optimized
  thumb-320.gif       – animated GIF at 320px wide (16:9)
  thumb-640.gif       – animated GIF at 640px wide (16:9)
  thumb-960.gif       – animated GIF at 960px wide (16:9)
  thumb-1280.gif      – animated GIF at 1280px wide (16:9)
  thumb-1920.gif      – animated GIF at 1920px wide (16:9)
"""

import argparse
import subprocess
import sys
import re
from pathlib import Path

DEFAULT_GIF_WIDTHS = [320, 640, 960, 1280, 1920]


def natural_sort_key(p: Path):
    """Sort filenames with embedded numbers naturally (image2 before image10)."""
    return [
        int(c) if c.isdigit() else c.lower()
        for c in re.split(r"(\d+)", p.name)
    ]


def find_frames(directory: Path):
    """Discover PNG frames in the directory, sorted naturally."""
    frames = sorted(directory.glob("image*.png"), key=natural_sort_key)
    if not frames:
        print(f"Error: No image*.png files found in {directory}", file=sys.stderr)
        sys.exit(1)
    print(f"Found {len(frames)} frames in {directory}")
    return frames


def create_concat_file(frames: list[Path], out_path: Path, fps: int):
    """Write an ffmpeg concat-demuxer file listing each frame with duration."""
    duration = 1.0 / fps
    with open(out_path, "w") as f:
        for frame in frames:
            escaped = str(frame.resolve()).replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{escaped}'\n")
            f.write(f"duration {duration:.6f}\n")
        # Repeat last frame to avoid duration truncation
        escaped = str(frames[-1].resolve()).replace("\\", "/").replace("'", "'\\''")
        f.write(f"file '{escaped}'\n")
    return out_path


def generate_video(directory: Path, frames: list[Path], fps: int):
    """Generate a 1920×1080 h264 MP4 from PNG frames."""
    concat_file = directory / "_concat.txt"
    output = directory / "hero.mp4"

    create_concat_file(frames, concat_file, fps)

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-vf", "scale=1920:1080:flags=lanczos",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-r", str(fps),
        str(output),
    ]

    print(f"\nGenerating video: {output}")
    print(f"  Resolution: 1920x1080, FPS: {fps}, Codec: h264, CRF: 18")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"  ✓ {output.name} ({size_mb:.2f} MB)")

    # Cleanup concat file
    concat_file.unlink(missing_ok=True)
    return output


def generate_gif(directory: Path, frames: list[Path], fps: int, width: int):
    """Generate an optimized animated GIF at the given width (16:9 aspect)."""
    concat_file = directory / "_concat.txt"
    output = directory / f"thumb-{width}.gif"
    palette = directory / f"_palette-{width}.png"

    height = int(width * 9 / 16)
    create_concat_file(frames, concat_file, fps)

    scale_filter = f"scale={width}:{height}:flags=lanczos"

    # Pass 1: generate palette
    cmd_palette = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-vf", f"{scale_filter},palettegen=stats_mode=diff",
        str(palette),
    ]

    # Pass 2: create GIF with palette
    cmd_gif = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-i", str(palette),
        "-lavfi", f"{scale_filter} [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        "-r", str(fps),
        str(output),
    ]

    print(f"\nGenerating GIF: {output.name} ({width}x{height})")

    result = subprocess.run(cmd_palette, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg palette error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(cmd_gif, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg gif error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    size_kb = output.stat().st_size / 1024
    unit = "KB" if size_kb < 1024 else "MB"
    size_display = size_kb if size_kb < 1024 else size_kb / 1024
    print(f"  ✓ {output.name} ({size_display:.1f} {unit})")

    # Cleanup temp files
    palette.unlink(missing_ok=True)
    concat_file.unlink(missing_ok=True)
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Generate hero video and animated GIF thumbnails from PNG frame sequences.",
    )
    parser.add_argument("directory", help="Directory containing image*.png frames")
    parser.add_argument("--fps", type=int, default=8, help="Frames per second (default: 8)")
    parser.add_argument("--gif-widths", type=int, nargs="+", default=DEFAULT_GIF_WIDTHS,
                        help=f"GIF output widths (default: {DEFAULT_GIF_WIDTHS})")
    parser.add_argument("--no-video", action="store_true", help="Skip video generation")
    parser.add_argument("--no-gif", action="store_true", help="Skip GIF generation")

    args = parser.parse_args()
    directory = Path(args.directory)

    if not directory.is_dir():
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    frames = find_frames(directory)

    if not args.no_video:
        generate_video(directory, frames, args.fps)

    if not args.no_gif:
        for width in sorted(args.gif_widths):
            generate_gif(directory, frames, args.fps, width)

    print("\n✓ All media generated successfully!")


if __name__ == "__main__":
    main()
