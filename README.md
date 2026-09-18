# Bulk Image Resizer

A standalone desktop tool with a simple graphical interface that resizes every image in a folder to **125 x 125 px** and saves the results to a separate output folder.

## Features

- **Graphical interface** — pick folders with Browse buttons, no command-line arguments needed.
- **Bulk processing** — resizes every supported image in the input folder in one click.
- **Fixed 125x125 output** — every image is standardized to the same square size.
- **Keep aspect ratio option** — when enabled (default), images are scaled to fit inside 125x125 without distortion and centered on a background; when disabled, images are stretched to exactly fill 125x125.
- **Transparency preserved** — images with an alpha channel (e.g. PNGs with transparent backgrounds) keep their transparency; the padding added around a resized image is transparent, not a solid color. Images without transparency are saved as plain RGB.
- **EXIF rotation handling** — photos that store their rotation in EXIF metadata (common with phone cameras) are rotated correctly before resizing.
- **Progress bar and status log** — shows how many images have been processed and reports any files that failed to convert.
- **Originals untouched** — the tool only reads from the input folder and writes new files to the output folder; nothing in the input folder is modified or deleted.
- **Automatic setup** — the included launcher (`run.bat`) checks for Python and the required Pillow library, installing either one automatically if missing.
- **Remembers your folders** — the input folder, output folder, and "keep aspect ratio" choice are saved automatically and restored the next time you open the tool.

### Supported file types

`.png` `.jpg` `.jpeg` `.bmp` `.gif` `.tiff` `.tif` `.webp`

Output files are always saved as `.png` (using the original filename with a `.png` extension), so transparency is preserved regardless of the source format.

## Installation

The tool lives in this folder as three files:

- `bulk_resize.py` — the application itself
- `run.bat` — one-click launcher for Windows
- `input/` and `output/` — default folders you can use, or replace with your own

### Requirements

- Windows (the launcher uses `run.bat`; the Python script itself is cross-platform)
- Python 3.8 or later
- The `Pillow` Python package

You do not need to install these yourself — `run.bat` handles it:

1. Double-click **`run.bat`**.
2. If Python is not found, the launcher tries to install it automatically using `winget` (built into Windows 10/11). If `winget` isn't available, it will tell you to install Python manually from [python.org](https://www.python.org/downloads/) — make sure to tick **"Add python.exe to PATH"** during setup.
3. If Python was just installed, close the window and run `run.bat` again so the updated PATH takes effect.
4. If the `Pillow` package is missing, the launcher installs it automatically with `pip install --user Pillow`.
5. The tool window opens once everything is ready.

### Manual installation (optional)

If you prefer to install things yourself instead of using `run.bat`:

```
pip install Pillow
python bulk_resize.py
```

## Configuration

The tool is configured entirely through its window. Your last-used input folder, output folder, and "keep aspect ratio" setting are saved automatically to `bulk_resize_settings.json` (created next to `bulk_resize.py` the first time you browse to a folder or run a resize) and are loaded again the next time you open the tool, so you don't need to re-select them every time. There's nothing to edit in this file by hand — just delete it if you ever want to reset to a blank state.

| Setting | Description |
|---|---|
| **Input folder** | Folder containing the images you want to resize. Browse to select it, or type/paste a path. |
| **Output folder** | Folder where resized images will be saved. Created automatically if it doesn't already exist. |
| **Keep aspect ratio** | Checked (default): images are scaled proportionally to fit inside 125x125 and centered on a transparent (or white, for non-transparent sources) background. Unchecked: images are stretched to exactly 125x125, which may distort non-square images. |

### Changing the target size

125x125 is currently fixed. To use a different size, open `bulk_resize.py` in a text editor and change the `TARGET_SIZE` constant near the top of the file:

```python
TARGET_SIZE = (125, 125)
```

## Usage

1. Run `run.bat` (or `python bulk_resize.py`). If you've used the tool before, your input and output folders are already filled in from last time.
2. Click **Browse...** next to *Input folder* and select the folder containing your images (or use the included `input` folder).
3. Click **Browse...** next to *Output folder* and select where resized images should be saved (or use the included `output` folder).
4. Choose whether to keep the aspect ratio (recommended) or stretch images to fill the square.
5. Click **Resize Images**.
6. Watch the progress bar; a summary appears when finished, including any files that failed along with the reason.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'PIL'`** — Pillow isn't installed for the Python interpreter being used. Run `run.bat` again (it installs Pillow automatically), or run `pip install Pillow` manually.
- **Python not found / `run.bat` can't install it** — install Python manually from [python.org](https://www.python.org/downloads/), ticking "Add python.exe to PATH", then re-run `run.bat`.
- **Some images fail to resize** — the status log lists which files failed and why (e.g. a corrupted file or unsupported format variant). Other images in the batch are unaffected.
