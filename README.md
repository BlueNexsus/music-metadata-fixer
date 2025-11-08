# 🎵 Music Metadata Fixer

[![GitHub release](https://img.shields.io/github/v/release/BlueNexsus/music-metadata-fixer?label=latest%20release&color=blue)](https://github.com/BlueNexsus/music-metadata-fixer/releases/latest)

**MetadataFixer** is a smart MP3 tag repair tool that automatically detects, identifies, and corrects missing or incorrect song metadata using **AcoustID** audio fingerprinting and **MusicBrainz** data.  
It features a modern **GUI built with CustomTkinter** and can also run from the command line.

---

## 🚀 Features

- 🎧 Accurate audio fingerprinting via Chromaprint (`fpcalc`)
- 🔍 Metadata lookup through AcoustID + MusicBrainz
- 🪟 Modern GUI interface (CustomTkinter dark theme)
- ⚙️ Automatic setup – prompts for missing API key on first run
- 🗂️ Automatic folder handling – untagged songs moved to temp, tagged, then restored
- 🧠 Smart filename fallback tagging
- 📊 Real-time progress bar and logging
- 🧾 `.exe` build available for Windows (no Python required)

---

## 🧰 Requirements

- **Python 3.11** or higher  
- **fpcalc (Chromaprint)** — [download here](https://github.com/acoustid/chromaprint/releases)  
  Place it next to the executable or in your PATH.  
- **AcoustID API key** — get one for free at [acoustid.org/api-key](https://acoustid.org/api-key)

Supported format: `MP3` (FLAC and M4A coming soon)

---

## 🪟 GUI Usage (recommended)

1. Launch:
   ```bash
   python gui_metadata_fixer.py
   ```
   *(or run `MetadataFixer.exe` if you downloaded the packaged build)*

2. On first run, the app will:
   - Ask for your **AcoustID API key**
   - Let you select your **music folder**
   - Automatically save both to a `.env` file for next time

3. Click **Start** to begin tagging  
   - Untagged songs will be processed in the background  
   - Progress is shown in real time  
   - Once complete, files are restored to their original folder

---

## 💻 CLI Usage (optional)

Run the command-line version if you prefer automation:

```bash
python fix_metadata.py --folder "D:\My Music"
```

It will use the same `.env` configuration as the GUI version.

---

## 🗂️ Project Structure

```
music-metadata-fixer/
├─ core/
│  ├─ tagger.py          # MusicBrainz/AcoustID tagging logic
│  ├─ file_utils.py      # File movement, logging, and env setup
├─ gui_metadata_fixer.py  # CustomTkinter GUI
├─ fix_metadata.py        # CLI entry point
├─ fpcalc.exe             # Chromaprint binary (Windows)
├─ requirements.txt
├─ version_info.txt
└─ README.md
```

---

## 🧩 Environment Setup (for developers)

```bash
git clone https://github.com/BlueNexsus/music-metadata-fixer.git
cd music-metadata-fixer
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🏗️ Building an EXE

Use **PyInstaller**:
```bash
pyinstaller --noconfirm --onefile --windowed ^
  --name "MetadataFixer" ^
  --add-data "fpcalc.exe;." ^
  --add-data "core;core" ^
  --add-data "logs;logs" ^
  --version-file "version_info.txt" ^
  gui_metadata_fixer.py
```

Output will appear in the `dist/` folder as `MetadataFixer.exe`.

---

## 🗓️ Roadmap

- [ ] Combine GUI folder selection with `.env` sync  
- [ ] Silence `fpcalc.exe` console window  
- [ ] Add “Cancel” button during tagging  
- [ ] Add album art fetching  
- [ ] Support FLAC, M4A formats  
- [ ] Add “About” dialog with version info and GitHub link  

---

## 📜 License

MIT License  
© 2025 BlueNexsus. All rights reserved.

---

## 🙌 Credits

- [AcoustID](https://acoustid.org/) & [Chromaprint](https://github.com/acoustid/chromaprint)  
- [MusicBrainz](https://musicbrainz.org/)  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
