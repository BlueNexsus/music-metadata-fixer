# 🎵 Music Metadata Fixer

[![GitHub release](https://img.shields.io/github/v/release/BlueNexsus/music-metadata-fixer?label=latest%20release&color=blue)](https://github.com/BlueNexsus/music-metadata-fixer/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/BlueNexsus/music-metadata-fixer/total?color=brightgreen)](https://github.com/BlueNexsus/music-metadata-fixer/releases)

**MetadataFixer** is a smart MP3 tag repair tool that automatically detects, identifies, and corrects missing or incorrect song metadata using **AcoustID** audio fingerprinting and **MusicBrainz** data.

It features a modern **CustomTkinter GUI**, a guided first-run setup for the AcoustID API key, and a safe auto-tagging pipeline.

---

## 🚀 Features

- 🎧 Accurate audio fingerprinting via **Chromaprint** (`fpcalc`)
- 🔍 Metadata lookup through **AcoustID + MusicBrainz**
- 🪟 Modern **CustomTkinter GUI** (dark theme)
- ⚙️ Guided AcoustID API key setup wizard (no manual `.env` editing required)
- 📂 Folder scan feedback — shows how many MP3 files are detected before processing
- 🗂️ Smart handling:
  - Untagged songs are moved to a temp folder
  - Tagged
  - Safely moved back (with retry logic on Windows)
- 🧠 Intelligent filename fallback tagging when lookups fail
- 📊 Real-time progress bar and detailed log output
- 🧾 Pre-built **Windows EXE** available (no Python required)

---

## 🧰 Requirements

For running from source:

- **Python 3.11** or newer
- **fpcalc (Chromaprint)**  
  Download from the official Chromaprint / AcoustID releases and place `fpcalc.exe`:
  - Next to `MetadataFixer.exe`, or
  - In the project folder, or
  - Anywhere on your system `PATH`
- **AcoustID API key**

### AcoustID API key (important)

MetadataFixer uses the **Application API key**, not the personal “User API key”.

Quick steps:

1. Create an account at <https://acoustid.org>.
2. Go to your account and choose **“Register a new application”**.
3. Copy the **API Key** shown for that application.
4. On first run, MetadataFixer’s **Setup Wizard** will ask for this key and store it for you.

You don’t need to manually edit `.env` unless you want to.

Supported format (current): **MP3**  
(*FLAC / M4A planned for future versions.*)

---

## 🪟 GUI Usage (Recommended)

1. Start the GUI:

   ```bash
   python gui_metadata_fixer.py
   ```

   Or run `MetadataFixer.exe` from the Releases page.

2. Choose your **music folder** with the **Browse** button.
   - The app will display how many MP3 files were found.

3. If this is your first run and no API key is configured:
   - A **Setup Wizard** window will open.
   - Click to open AcoustID in your browser.
   - Register a new application, copy the API key.
   - Paste it into the wizard and click **Save**.

4. Click **Start**:
   - Untagged MP3s are detected and moved into a temporary folder.
   - Each file is processed via AcoustID + MusicBrainz.
   - Successfully tagged files are moved back.
   - Progress bar and log area show what’s happening.

If no untagged songs are found, the log will tell you everything is already up to date.

---

## 💻 CLI Usage (Optional)

For batch/automated runs (for advanced users):

```bash
python fix_metadata.py --folder "D:\My Music"
```

- Uses the same `ACOUSTID_API_KEY` as configured by the GUI.
- Requires `fpcalc` and Python environment to be properly set up.

---

## 🗂️ Project Structure

```text
music-metadata-fixer/
├─ core/
│  ├─ tagger.py          # AcoustID / MusicBrainz tagging logic
│  ├─ file_utils.py      # File ops, logging, setup wizard, .env handling
├─ gui_metadata_fixer.py  # CustomTkinter GUI entry point
├─ fix_metadata.py        # CLI entry point (optional)
├─ fpcalc.exe             # Chromaprint binary (Windows, optional here)
├─ version_info.txt       # Embedded version info for the EXE
├─ requirements.txt
└─ README.md
```

---

## 🧩 Environment Setup (Developers)

```bash
git clone https://github.com/BlueNexsus/music-metadata-fixer.git
cd music-metadata-fixer

python -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🏗️ Building the EXE

Build the Windows executable using the provided spec file:

```bash
pyinstaller --clean MetadataFixer.spec
```

- Produces the final build under `dist/MetadataFixer/`.
- `.env` is **not** bundled — users can provide their own or use the Setup Wizard.

---

## 🗓️ Roadmap

- [ ] Add “Cancel” button during tagging  
- [ ] Fetch and embed album artwork  
- [ ] Support FLAC and M4A formats  
- [ ] Add “About” dialog with version + GitHub link  
- [ ] Async/parallel tagging for smoother UI on large libraries  

---

## 📜 License

MIT License  
© 2025 BlueNexsus

---

## 🙌 Credits

- [AcoustID](https://acoustid.org/)
- [Chromaprint](https://github.com/acoustid/chromaprint)
- [MusicBrainz](https://musicbrainz.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
