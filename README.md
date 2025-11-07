# Metadata Fix Tool

This tool helps fix MP3 metadata using AcoustID and MusicBrainz databases.

## Prerequisites

1. Python 3.11 or higher
2. Chromaprint (for audio fingerprinting)
   - Windows: Download the latest fpcalc.exe from https://github.com/acoustid/chromaprint/releases
   - Place fpcalc.exe in the same directory as fix_metadata.py or add it to your PATH

## Installation

1. Create a virtual environment (already done):
```powershell
python -m venv .venv
```

2. Install dependencies:
```powershell
.\.venv\Scripts\pip install -r requirements.txt
```

3. Set up your .env file with your AcoustID API key and root folder path:
```
ACOUSTID_API_KEY=your_key_here
ROOT_FOLDER=path_to_your_music
```

## Usage

Basic usage:
```powershell
.\.venv\Scripts\python fix_metadata.py
```

With custom folder:
```powershell
.\.venv\Scripts\python fix_metadata.py --folder "path/to/your/music"
```

Force update all files:
```powershell
.\.venv\Scripts\python fix_metadata.py --force
```