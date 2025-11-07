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

Chromaprint