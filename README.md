# 🎵 Music Metadata Fixer

A Python tool and GUI app to **automatically fix and clean up MP3 metadata** using **AcoustID** and **MusicBrainz** databases.

It can detect songs by their **audio fingerprint**, correct wrong or missing tags, and organize your library — whether you’re a casual listener or a metadata perfectionist.

---

## 🚀 Features

- Uses **Chromaprint** (`fpcalc.exe`) for fingerprinting
- Fetches accurate metadata from **MusicBrainz**
- Supports both **GUI** and **command-line** operation
- Batch processes entire folders
- Allows manual override and selective updates
- Easy setup with `.env` configuration

---

## 🧩 Prerequisites

1. **Python 3.11 or higher**
2. **Chromaprint** (for audio fingerprinting)
   - Download `fpcalc.exe` from [AcoustID Releases](https://github.com/acoustid/chromaprint/releases)
   - Place it in the same folder as `fix_metadata.py` or add it to your `PATH`
3. (Optional) **AcoustID API key**
   - Get one free from [https://acoustid.org/api-key](https://acoustid.org/api-key)

---

## ⚙️ Installation

1. **Create and activate a virtual environment**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Set up your .env file with your AcoustID API key and root folder:

ACOUSTID_API_KEY=your_key_here
ROOT_FOLDER=path_to_your_music

💻 Usage (Command Line)

Run the main script:

python fix_metadata.py


Specify a folder manually:

python fix_metadata.py --folder "D:\My Music"


Force-refresh all files (ignore existing tags):

python fix_metadata.py --force

🖥️ GUI Mode

If you prefer a visual interface, run:

python gui_metadata_fixer.py


Then:

Choose your music folder

Review detected songs and metadata

Apply changes in bulk or selectively

🗂️ Project Structure
music-metadata-fixer/
├─ core/                  # Metadata handling logic
├─ fix_metadata.py        # CLI entry point
├─ gui_metadata_fixer.py  # GUI entry point
├─ requirements.txt
├─ .env.example
└─ README.md

🧭 Roadmap

 Support FLAC and M4A files

 Add metadata preview before applying

 Integrate album artwork fetching

 Create Windows executable (.exe) version

 Implement auto-tag verification and logs

📄 License

MIT License
Copyright (c) 2025

You are free to use, modify, and distribute this software with attribution.

🧠 Credits

AcoustID

MusicBrainz

Chromaprint```markdown
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