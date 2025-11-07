import os
import shutil
from pathlib import Path
from mutagen.easyid3 import EasyID3
from dotenv import load_dotenv
import logging
from core.tagger import run_tagger

from pathlib import Path

def find_mp3_files(root_folder):
    """Find all MP3 files in the given folder and its subfolders."""
    root_path = Path(root_folder)
    if not root_path.exists():
        raise ValueError(f"Folder not found: {root_folder}")
    return [str(p) for p in root_path.rglob("*.mp3")]


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
def setup_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / "metadata_fix.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("MetadataFixer")

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def check_fpcalc():
    fpcalc = "fpcalc.exe" if os.name == "nt" else "fpcalc"
    here = Path(__file__).resolve().parent.parent
    local = here / fpcalc
    if local.exists():
        os.environ["FPCALC"] = str(local)
        return
    path = shutil.which(fpcalc)
    if not path:
        raise FileNotFoundError("fpcalc.exe not found. Place it in the project folder.")
    os.environ["FPCALC"] = path

def scan_for_untagged(source_folder):
    """Find mp3s missing artist/title."""
    untagged = []
    for p in Path(source_folder).rglob("*.mp3"):
        try:
            tags = EasyID3(p)
            if not ("artist" in tags and tags["artist"] and "title" in tags and tags["title"]):
                untagged.append(p)
        except Exception:
            untagged.append(p)
    return untagged

def move_files(files, dest):
    dest.mkdir(exist_ok=True)
    moved = []
    for f in files:
        target = dest / f.name
        shutil.move(str(f), str(target))
        moved.append(target)
    return moved

def move_back_all(src, dest):
    for f in Path(src).glob("*.mp3"):
        shutil.move(str(f), str(Path(dest) / f.name))
    try:
        Path(src).rmdir()
    except OSError:
        pass  # folder not empty or in use

# ---------------------------------------------------------------------------
# Main automatic pipeline
# ---------------------------------------------------------------------------

def run_auto_tag_pipeline(source_folder=None):
    """Automatically handle move-to-temp, tag, and move-back."""
    load_dotenv()
    api_key = os.getenv("ACOUSTID_API_KEY")
    if not api_key:
        raise ValueError("ACOUSTID_API_KEY missing from .env")

    if not source_folder:
        source_folder = os.getenv("ROOT_FOLDER")
    if not source_folder:
        raise ValueError("ROOT_FOLDER missing or not provided")

    check_fpcalc()
    logger = setup_logger()
    logger.info(f"Starting auto tag pipeline for {source_folder}")

    temp_folder = Path(source_folder) / "_temp_untagged"
    temp_folder.mkdir(exist_ok=True)

    # Move untagged
    untagged = scan_for_untagged(source_folder)
    if not untagged:
        logger.info("No untagged songs found. Everything is up-to-date.")
        return

    logger.info(f"Found {len(untagged)} untagged files. Moving to {temp_folder}")
    moved = move_files(untagged, temp_folder)

    # Run tagger
    success, total = run_tagger(temp_folder, api_key, logger)

    # Move back
    move_back_all(temp_folder, source_folder)
    logger.info(f"Moved all files back to {source_folder}")

    logger.info("Auto tagging pipeline completed.")
    logger.info(f"Summary: {success}/{total} tagged successfully.")
