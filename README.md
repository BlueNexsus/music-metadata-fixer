# 🎵 Music Metadata Fixer

[![GitHub release](https://img.shields.io/github/v/release/BlueNexsus/music-metadata-fixer?label=latest%20release&color=blue)](https://github.com/BlueNexsus/music-metadata-fixer/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/BlueNexsus/music-metadata-fixer/total?color=brightgreen)](https://github.com/BlueNexsus/music-metadata-fixer/releases)

**MetadataFixer** is a smart MP3 tag repair tool that automatically detects, identifies, and corrects missing or incorrect song metadata using **AcoustID** audio fingerprinting and **MusicBrainz** data.  
It features a modern **GUI built with CustomTkinter** and can also run from the command line.

---

## 🚀 Features

- 🎧 Accurate audio fingerprinting via **Chromaprint** (`fpcalc`)
- 🔍 Metadata lookup through **AcoustID + MusicBrainz**
- 🪟 Modern **CustomTkinter GUI** (dark theme)
- ⚙️ Automatic setup — prompts for missing API key on first run
- 🗂️ Smart folder handling — untagged songs are moved, tagged, and restored automatically
- 🧠 Intelligent filename fallback tagging
- 📊 Real-time progress bar and detailed logging
- 🧾 **Windows EXE** build available (no Python required)

---

## 🧰 Requirements

- **Python 3.11** or newer  
- **fpcalc (Chromaprint)** — [Download here](https://github.com/acoustid/chromaprint/releases)  
  Place it next to the executable or add to PATH.  
- **AcoustID API key** — get one free at [acoustid.org/api-key](https://acoustid.org/api-key)

Supported format: **MP3**  
(*FLAC and M4A support planned for future releases.*)

---

## 🪟 GUI Usage (Recommended)

1. Launch:
   ```bash
   python gui_metadata_fixer.py
   ```
   *(or run `MetadataFixer.exe` if you downloaded the packaged build)*

2. On first run, the app will:
   - Ask for your **AcoustID API key**
   - Let you select your **music folder**
   - Automatically save both to `.env` for next sessions

3. Click **Start** to begin tagging  
   - Untagged songs are processed in the background  
   - Progress is shown live  
   - Files are restored when tagging completes

---

## 💻 CLI Usage (Optional)

Run the command-line version if you prefer automation:
```bash
python fix_metadata.py --folder "D:\My Music"
```
It uses the same `.env` configuration as the GUI.

---

## 🗂️ Project Structure

```
music-metadata-fixer/
├─ core/
│  ├─ tagger.py          # MusicBrainz / AcoustID tagging logic
│  ├─ file_utils.py      # File movement, logging, and .env setup
├─ gui_metadata_fixer.py  # CustomTkinter GUI
├─ fix_metadata.py        # CLI entry point
├─ fpcalc.exe             # Chromaprint binary (Windows)
├─ requirements.txt
├─ version_info.txt
└─ README.md
```

---

## 🧩 Environment Setup (For Developers)

```bash
git clone https://github.com/BlueNexsus/music-metadata-fixer.git
cd music-metadata-fixer
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🏗️ Building the EXE

Build a single-file EXE using **PyInstaller**:
```bash
pyinstaller --noconfirm --onefile --windowed ^
  --name "MetadataFixer" ^
  --add-data "fpcalc.exe;." ^
  --add-data "core;core" ^
  --add-data "logs;logs" ^
  --version-file "version_info.txt" ^
  gui_metadata_fixer.py
```

Output will appear in `dist/MetadataFixer.exe`.

---

## 🗓️ Roadmap

- [ ] Add “Cancel” button during tagging  
- [ ] Add album art fetching  
- [ ] Support FLAC and M4A formats  
- [ ] Add “About” dialog with version info and GitHub link  
- [ ] Implement async tagging for smoother UI  

---

## 📜 License

MIT License  
© 2025 BlueNexsus

---

## 🙌 Credits

- [AcoustID](https://acoustid.org/) & [Chromaprint](https://github.com/acoustid/chromaprint)  
- [MusicBrainz](https://musicbrainz.org/)  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
