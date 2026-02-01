# Scripts

Utility scripts for image processing and site maintenance.

---

## `generate_thumbs.py`

Generates responsive thumbnail images with 16:9 aspect ratio from source images.

### Features
- **Center-crops** images to 16:9 before resizing
- **Auto-detects** source width and only generates smaller sizes
- **Skips** regenerating the source file to preserve your original quality settings
- Outputs JPEG with configurable quality (default 100)

### Quick Start

```bash
# Generate standard sizes (320, 640, 960, 1280, 1920) from your source
python scripts/generate_thumbs.py public/images/projects/my-project/thumb-640.jpg --prefix thumb

# Preview without generating (dry run)
python scripts/generate_thumbs.py path/to/source.jpg --dry-run
```

### Usage

```bash
python scripts/generate_thumbs.py <source> [options]
```

**Arguments:**
- `source` — Path to source image file

**Options:**
- `--out-dir DIR` — Output directory (default: same as source)
- `--widths W [W ...]` — Custom target widths (default: 320, 640, 960, 1280, 1920)
- `--quality N` — JPEG quality 1–100 (default: 100)
- `--prefix NAME` — Output filename prefix (default: source filename stem)
- `--dry-run` — Preview actions without generating files

### Examples

```bash
# Generate from a 640px source (produces thumb-320.jpg only, skips thumb-640.jpg)
python scripts/generate_thumbs.py public/images/projects/fluid-sim/thumb-640.jpg --prefix thumb

# Custom quality for smaller file sizes
python scripts/generate_thumbs.py source.jpg --quality 95 --prefix thumb

# Generate specific widths
python scripts/generate_thumbs.py source.jpg --widths 320 640 1280 --prefix thumb

# Custom output location and prefix
python scripts/generate_thumbs.py assets/photo.jpg --out-dir public/images/gallery --prefix gallery-thumb
```

### Quality Settings

**Default: 100** (lossless from source)
- Use when your source was already optimized (e.g., saved at 95%)
- Preserves exact quality of source without recompression artifacts

**Recommended: 95** (balanced)
- Good visual quality with ~30–40% smaller file sizes
- Minimal perceptible quality loss
- Use when generating from unoptimized sources (100% quality originals)

**Target file sizes:**
- 320px: 20–40 KB
- 640px: 50–100 KB
- 1280px: 100–200 KB

### How It Works

1. **Load** source image
2. **Center-crop** to 16:9 aspect ratio
3. **Filter** widths to only those ≤ source width
4. **Skip** any output that would overwrite the source file
5. **Resize** using LANCZOS resampling (high quality)
6. **Save** with specified JPEG quality and optimization

### Integration with Card Component

The site's `Card.astro` component automatically discovers generated thumbnail variants:

- Looks for files matching pattern: `{base}-{width}.jpg` (e.g., `thumb-320.jpg`, `thumb-640.jpg`)
- Generates `srcset` with all available widths
- Uses `sizes` attribute: `(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw`
- Browsers load optimal size based on viewport and device pixel ratio

### Requirements

```bash
pip install Pillow
```

### Troubleshooting

**"No thumbnails generated"**
- Source image is smaller than all target widths
- Solution: Use `--widths` to specify smaller sizes or upscale your source

**"ModuleNotFoundError: No module named 'PIL'"**
- Install Pillow: `pip install Pillow`

**Output file size too large**
- Try lower quality: `--quality 85` or `--quality 75`
- Check source dimensions — oversized sources produce larger outputs

**404 errors on site**
- Ensure generated files follow naming pattern: `{prefix}-{width}.jpg`
- Verify files exist in `public/images/...` directory
- Check content frontmatter uses correct thumb path
