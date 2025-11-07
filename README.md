# Music Metadata Fixer

A Python utility (with both CLI and GUI) to automatically detect, correct, and standardize MP3 metadata using audio fingerprints (Chromaprint/AcoustID) and MusicBrainz. Designed for power users and casual listeners alike, it helps clean up large libraries by fixing missing or incorrect tags and applying consistent metadata across your collection.

---

## Key features

- Accurate audio fingerprinting using Chromaprint (fpcalc)
- Metadata lookup and matching via MusicBrainz and AcoustID
- Command-line and graphical user interface
- Batch processing for folders of music files
- Manual review and selective updates
- Simple configuration through an .env file

---

## Requirements

- Python 3.11 or higher
- Chromaprint `fpcalc` (download from https://github.com/acoustid/chromaprint/releases)
- Optional: AcoustID API key (recommended for higher usage limits)
  - Obtain a free key at https://acoustid.org/api-key

Supported formats: MP3 (primary). Plans exist to extend support to FLAC, M4A, and other formats.

---

## Installation

1. Clone the repository and change into the project directory:

```bash
git clone https://github.com/BlueNexsus/music-metadata-fixer.git
cd music-metadata-fixer
```

2. Create and activate a virtual environment:

- On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- On macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Place `fpcalc` (Chromaprint) in your PATH or in the same folder as `fix_metadata.py`. On Windows, that may be `fpcalc.exe`.

---

## Configuration

Copy the example environment file and add your settings:

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:

```
ACOUSTID_API_KEY=your_acoustid_key_here
ROOT_FOLDER=/path/to/your/music
```

The ACOUSTID_API_KEY is optional but recommended for reliable service.

---

## Usage

Command-line

- Run the main fixer (uses ROOT_FOLDER from .env by default):

```bash
python fix_metadata.py
```

- Specify a folder explicitly:

```bash
python fix_metadata.py --folder "D:\My Music"
```

- Force refresh metadata for all files (ignore existing tags):

```bash
python fix_metadata.py --force
```

GUI

- Launch the graphical interface:

```bash
python gui_metadata_fixer.py
```

In GUI mode you can choose a folder, review detected matches, and apply changes selectively or in bulk.

---

## Project structure

Root layout (important files):

```
music-metadata-fixer/
├─ core/                  # Metadata handling logic and helpers
├─ fix_metadata.py        # CLI entry point
├─ gui_metadata_fixer.py  # GUI entry point
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## Roadmap

Planned improvements:

- Add support for FLAC, M4A, and other popular lossless formats
- Integrate album art fetching and embedding
- Add metadata preview and change-diff before applying edits
- Provide packaged binaries (Windows .exe, macOS app)
- Implement logging, dry-run, and stricter verification modes

---

## Contributing

Contributions, issues, and feature requests are welcome.

- Please open an issue to discuss large changes before submitting a PR.
- Follow the repository coding style and include tests for new behavior where possible.
- Add clear commit messages and keep PRs focused.

---

## License

MIT License — see LICENSE file. Copyright (c) 2025.

---

## Credits

- AcoustID / Chromaprint — audio fingerprinting
- MusicBrainz — metadata database

---
```
