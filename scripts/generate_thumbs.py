#!/usr/bin/env python3
"""
Generate responsive thumbnail images with 16:9 aspect ratio.

This script takes a source image and generates multiple smaller sizes,
preserving aspect ratio by center-cropping to 16:9 and resizing.
Only generates sizes smaller than or equal to the source image width.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image


# Standard widths for responsive thumbnails
DEFAULT_WIDTHS = [320, 640, 960, 1280, 1920]


def center_crop_16_9(img):
    """
    Center-crop an image to 16:9 aspect ratio.
    
    Args:
        img: PIL Image object
        
    Returns:
        PIL Image object cropped to 16:9
    """
    target_ratio = 16 / 9
    width, height = img.size
    current_ratio = width / height
    
    if abs(current_ratio - target_ratio) < 0.01:
        # Already close to 16:9
        return img
    
    if current_ratio > target_ratio:
        # Image is wider than 16:9, crop width
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        # Image is taller than 16:9, crop height
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))
    
    return img


def generate_thumbnails(source_path, out_dir=None, widths=None, quality=100, dry_run=False, prefix=None):
    """
    Generate responsive thumbnail images.
    
    Args:
        source_path: Path to source image
        out_dir: Output directory (defaults to same as source)
        widths: List of target widths (defaults to standard sizes)
        quality: JPEG quality (1-100, default 100)
        dry_run: If True, print actions without executing
        prefix: Output filename prefix (defaults to source stem)
        
    Returns:
        List of generated file paths
    """
    source_path = Path(source_path)
    
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}", file=sys.stderr)
        sys.exit(1)
    
    # Load source image
    try:
        img = Image.open(source_path)
    except Exception as e:
        print(f"Error: Could not open image: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Center-crop to 16:9
    img = center_crop_16_9(img)
    source_width = img.size[0]
    
    # Determine output directory
    if out_dir is None:
        out_dir = source_path.parent
    else:
        out_dir = Path(out_dir)
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine output prefix
    if prefix is None:
        prefix = source_path.stem
    
    # Use default widths if not specified
    if widths is None:
        widths = DEFAULT_WIDTHS
    
    # Filter widths to only those <= source width
    valid_widths = sorted([w for w in widths if w <= source_width])
    
    if not valid_widths:
        print(f"Warning: Source image width ({source_width}px) is smaller than all target widths", file=sys.stderr)
        print(f"No thumbnails generated.", file=sys.stderr)
        return []
    
    print(f"Source: {source_path}")
    print(f"Source dimensions after 16:9 crop: {img.size[0]}x{img.size[1]}px")
    print(f"Output directory: {out_dir}")
    print(f"Target widths: {valid_widths}")
    print(f"Quality: {quality}")
    print()
    
    generated = []
    
    for width in valid_widths:
        # Calculate height maintaining 16:9
        height = int(width / (16/9))
        
        output_name = f"{prefix}-{width}.jpg"
        output_path = out_dir / output_name
        
        # Skip if output would overwrite the source file
        if output_path.resolve() == source_path.resolve():
            print(f"⊘ Skipping: {output_path} (source file, will not overwrite)")
            continue
        
        if dry_run:
            print(f"[DRY RUN] Would generate: {output_path} ({width}x{height}px)")
        else:
            # Resize image
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Save with specified quality
            resized.save(output_path, "JPEG", quality=quality, optimize=True)
            
            file_size = output_path.stat().st_size / 1024  # KB
            print(f"✓ Generated: {output_path} ({width}x{height}px, {file_size:.1f} KB)")
            
            generated.append(output_path)
    
    return generated


def main():
    parser = argparse.ArgumentParser(
        description="Generate responsive thumbnail images with 16:9 aspect ratio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate standard sizes (320, 640, 960, etc.) from a 640px source
  python generate_thumbs.py public/images/projects/fluid-sim/thumb-640.jpg
  
  # Generate with 95% quality
  python generate_thumbs.py thumb-640.jpg --quality 95
  
  # Custom widths
  python generate_thumbs.py thumb-640.jpg --widths 320 640 1280
  
  # Specify output directory and prefix
  python generate_thumbs.py source.jpg --out-dir output/ --prefix my-thumb
  
  # Dry run to preview without generating
  python generate_thumbs.py thumb-640.jpg --dry-run
        """
    )
    
    parser.add_argument(
        "source",
        help="Source image file path"
    )
    
    parser.add_argument(
        "--out-dir",
        help="Output directory (default: same as source)"
    )
    
    parser.add_argument(
        "--widths",
        type=int,
        nargs="+",
        help=f"Target widths in pixels (default: {DEFAULT_WIDTHS})"
    )
    
    parser.add_argument(
        "--quality",
        type=int,
        default=100,
        help="JPEG quality 1-100 (default: 100)"
    )
    
    parser.add_argument(
        "--prefix",
        help="Output filename prefix (default: source filename stem)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without generating files"
    )
    
    args = parser.parse_args()
    
    # Validate quality
    if not 1 <= args.quality <= 100:
        print("Error: Quality must be between 1 and 100", file=sys.stderr)
        sys.exit(1)
    
    try:
        generated = generate_thumbnails(
            source_path=args.source,
            out_dir=args.out_dir,
            widths=args.widths,
            quality=args.quality,
            dry_run=args.dry_run,
            prefix=args.prefix
        )
        
        if not args.dry_run:
            print(f"\n✓ Successfully generated {len(generated)} thumbnail(s)")
        
    except KeyboardInterrupt:
        print("\nAborted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
