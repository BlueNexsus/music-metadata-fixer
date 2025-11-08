import os
import shutil
import logging
from pathlib import Path
from tkinter import simpledialog, Tk, messagebox
from dotenv import load_dotenv, set_key
from mutagen.easyid3 import EasyID3
import time, shutil, os

from core.tagger import run_tagger

def ensure_env_setup(selected_folder=None):
    """
    Ensure that the ACOUSTID_API_KEY exists in .env.
    If a folder is provided by GUI, save it as ROOT_FOLDER without prompting again.
    """
    from tkinter import simpledialog, Tk, messagebox
    from dotenv import load_dotenv, set_key

    env_path = ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("ACOUSTID_API_KEY")

    root = Tk()
    root.withdraw()

    # --- Step 1: Check API key only ---
    if not api_key or api_key.strip().upper() in {"", "YOUR_ACOUSTID_APP_KEY_HERE"}:
        messagebox.showinfo(
            "AcoustID Setup",
            "You need an AcoustID API key to tag songs.\n\n"
            "You can get one for free at https://acoustid.org/api-key."
        )
        api_key = simpledialog.askstring("Enter API Key", "Please enter your AcoustID API key:")
        if api_key:
            set_key(env_path, "ACOUSTID_API_KEY", api_key)
            messagebox.showinfo("Saved", "✅ API key saved successfully!")
        else:
            messagebox.showerror("Missing Key", "❌ Cannot continue without an API key.")
            root.destroy()
            raise ValueError("Missing API key")

    # --- Step 2: If GUI folder provided, save it ---
    if selected_folder:
        set_key(env_path, "ROOT_FOLDER", selected_folder)

    root.destroy()
    return api_key



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
    """Find mp3s missing artist/title, excluding _temp_untagged folder."""
    untagged = []
    for p in Path(source_folder).rglob("*.mp3"):
        if "_temp_untagged" in p.parts:
            continue  # skip temp processing directory
        try:
            tags = EasyID3(p)
            if not ("artist" in tags and tags["artist"] and "title" in tags and tags["title"]):
                untagged.append(p)
        except Exception:
            untagged.append(p)
    return untagged


def safe_move(src, dst, retries=5, delay=0.5):
    """Move files safely, retrying briefly if the source is still locked or delayed by the OS."""
    import time, shutil, os
    for attempt in range(retries):
        try:
            shutil.move(src, dst)
            return
        except FileNotFoundError:
            if not os.path.exists(src):
                # Still raise if the file really disappeared
                raise
            time.sleep(delay)
        except Exception:
            # Suppress transient Windows I/O errors until retries exhausted
            time.sleep(delay)
    try:
        shutil.move(src, dst)
    except Exception as e:
        # Log but don’t crash GUI
        print(f"[safe_move] Final move failed for {src}: {e}")



def move_files(files, dest):
    dest.mkdir(exist_ok=True)
    moved = []
    for f in files:
        target = dest / f.name
        safe_move(str(f), str(target))
        moved.append(target)
    return moved

def move_back_all(src, dest):
    for f in Path(src).glob("*.mp3"):
        safe_move(str(f), str(Path(dest) / f.name))
    try:
        Path(src).rmdir()
    except OSError:
        pass  # folder not empty or in use

# ---------------------------------------------------------------------------
# Main automatic pipeline
# ---------------------------------------------------------------------------

def run_auto_tag_pipeline(source_folder=None, progress_callback=None):
    """Automatically handle move-to-temp, tag, and move-back."""
    load_dotenv()
    api_key = os.getenv("ACOUSTID_API_KEY")

    if not api_key:
        raise ValueError("ACOUSTID_API_KEY not set in .env")

    if not source_folder:
        source_folder = os.getenv("ROOT_FOLDER")
        if not source_folder or not os.path.exists(source_folder):
            raise ValueError("ROOT_FOLDER not set or does not exist.")

    check_fpcalc()
    logger = setup_logger()
    logger.info(f"Starting auto tag pipeline for {source_folder}")

    temp_folder = Path(source_folder) / "_temp_untagged"
    temp_folder.mkdir(exist_ok=True)

    # Move untagged
    untagged = scan_for_untagged(source_folder)
    if not untagged:
        logger.info("No untagged songs found. Everything is up-to-date.")
        if progress_callback:
            progress_callback(1, 1)  # show full progress instantly
        return

    logger.info(f"Found {len(untagged)} untagged files. Moving to {temp_folder}")
    move_files(untagged, temp_folder)

    # --- Pass the progress callback into run_tagger() ---
    success, total = run_tagger(temp_folder, api_key, logger, progress_callback)

    move_back_all(temp_folder, source_folder)
    logger.info(f"Moved all files back to {source_folder}")
    logger.info("Auto tagging pipeline completed.")
    logger.info(f"Summary: {success}/{total} tagged successfully.")


