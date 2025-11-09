import os
import shutil
import logging
from pathlib import Path
from tkinter import messagebox
from dotenv import load_dotenv, set_key
from mutagen.easyid3 import EasyID3

from core.tagger import run_tagger

# Global flag to prevent multiple wizards
_wizard_open = False


def ensure_env_setup(selected_folder=None):
    """
    Ensure that the ACOUSTID_API_KEY exists in .env.

    Returns:
        True  -> API key is present (after this call) and we can continue.
        False -> No key yet (wizard shown or user cancelled); caller should STOP.
    """
    import webbrowser
    import customtkinter as ctk
    global _wizard_open

    env_path = ".env"
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("ACOUSTID_API_KEY")

    # If key already exists -> optionally store ROOT_FOLDER and we're done.
    if api_key and api_key.strip().upper() not in {"", "YOUR_ACOUSTID_APP_KEY_HERE"}:
        if selected_folder:
            set_key(env_path, "ROOT_FOLDER", selected_folder)
        return True

    # Prevent multiple wizard windows
    if _wizard_open:
        return False
    _wizard_open = True

    # ----------------- Setup Wizard -----------------
    win = ctk.CTkToplevel()
    win.title("AcoustID Setup Wizard")
    win.geometry("480x280")
    win.resizable(False, False)

    title = ctk.CTkLabel(
        win,
        text="🎧 AcoustID API Key Required",
        font=("Segoe UI", 18, "bold")
    )
    title.pack(pady=(20, 10))

    text = (
        "To use automatic song recognition, you need a free API key from AcoustID.\n\n"
        "1. Open AcoustID’s website.\n"
        "2. Click \"Register a new application\".\n"
        "3. Copy the generated API Key.\n"
        "4. Paste it below and click Save."
    )

    label = ctk.CTkLabel(
        win,
        text=text,
        font=("Segoe UI", 12),
        justify="left",
        wraplength=420
    )
    label.pack(pady=(0, 10), padx=15)

    def open_site():
        webbrowser.open("https://acoustid.org")

    ctk.CTkButton(
        win,
        text="🌐 Open AcoustID Website",
        command=open_site,
        width=220
    ).pack(pady=(5, 10))

    entry = ctk.CTkEntry(
        win,
        width=360,
        placeholder_text="Paste your API key here"
    )
    entry.pack(pady=(5, 10))

    btn_frame = ctk.CTkFrame(win, fg_color="transparent")
    btn_frame.pack(pady=(10, 5))

    def save_key():
        global _wizard_open
        key = entry.get().strip()
        if not key:
            messagebox.showerror("Error", "API key cannot be empty.")
            return
        set_key(env_path, "ACOUSTID_API_KEY", key)
        os.environ["ACOUSTID_API_KEY"] = key  # make it visible immediately
        if selected_folder:
            set_key(env_path, "ROOT_FOLDER", selected_folder)
        messagebox.showinfo("Saved", "✅ API key saved successfully!")
        _wizard_open = False
        win.destroy()

    def cancel():
        global _wizard_open
        messagebox.showerror(
            "Missing Key",
            "❌ Cannot start tagging without an AcoustID API key.\n"
            "Please obtain a key and try again."
        )
        _wizard_open = False
        win.destroy()

    ctk.CTkButton(
        btn_frame, text="Save", width=100, command=save_key
    ).pack(side="left", padx=10)
    ctk.CTkButton(
        btn_frame, text="Cancel", width=100, command=cancel
    ).pack(side="left", padx=10)

    # Bring wizard to front, but not permanently topmost
    win.lift()
    win.attributes("-topmost", True)
    win.after(150, lambda: win.attributes("-topmost", False))
    win.after(100, win.focus_force)

    print("[MetadataFixer] API key missing – showing AcoustID setup wizard.")
    # IMPORTANT: we do NOT block here; user will press Start again after saving.
    return False


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
            continue
        try:
            tags = EasyID3(p)
            if not (
                "artist" in tags and tags["artist"]
                and "title" in tags and tags["title"]
            ):
                untagged.append(p)
        except Exception:
            untagged.append(p)
    return untagged


def safe_move(src, dst, retries=5, delay=0.5):
    """Move files safely, retrying briefly if the source is still locked."""
    import time
    for attempt in range(retries):
        try:
            shutil.move(src, dst)
            return
        except FileNotFoundError:
            if not os.path.exists(src):
                raise
            time.sleep(delay)
        except Exception:
            time.sleep(delay)
    try:
        shutil.move(src, dst)
    except Exception as e:
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
        pass


# ---------------------------------------------------------------------------
# Main automatic pipeline
# ---------------------------------------------------------------------------
def run_auto_tag_pipeline(source_folder=None, progress_callback=None):
    """Automatically handle move-to-temp, tag, and move-back."""
    load_dotenv()
    api_key = os.getenv("ACOUSTID_API_KEY")

    # Defensive: in normal flow this should already be set by ensure_env_setup
    if not api_key:
        print("[MetadataFixer] ACOUSTID_API_KEY missing at pipeline start; aborting.")
        return

    if not source_folder:
        source_folder = os.getenv("ROOT_FOLDER")
        if not source_folder or not os.path.exists(source_folder):
            print("[MetadataFixer] Invalid or missing ROOT_FOLDER; stopping pipeline.")
            return

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
            progress_callback(1, 1)
        return

    logger.info(f"Found {len(untagged)} untagged files. Moving to {temp_folder}")
    move_files(untagged, temp_folder)

    # Run tagger
    success, total = run_tagger(temp_folder, api_key, logger, progress_callback)

    move_back_all(temp_folder, source_folder)
    logger.info(f"Moved all files back to {source_folder}")
    logger.info("Auto tagging pipeline completed.")
    logger.info(f"Summary: {success}/{total} tagged successfully.")
