import os
import time
import logging
import traceback
import acoustid
import musicbrainzngs
from mutagen.easyid3 import EasyID3
from pathlib import Path
import re
from tqdm import tqdm
import logging as _logging

# ---------------------------------------------------------------------------
# SETUP
# ---------------------------------------------------------------------------

def setup_musicbrainz():
    """Initialize MusicBrainz user agent."""
    musicbrainzngs.set_useragent("MetadataFixer", "2.0", "https://musicbrainz.org")
    _logging.getLogger("musicbrainzngs").setLevel(_logging.ERROR)

def is_already_tagged(path):
    """Check if the file already has artist and title."""
    try:
        song = EasyID3(path)
        return all(k in song for k in ["artist", "title"])
    except Exception:
        return False

def fallback_tag_from_filename(path, logger):
    """Extract artist/title from filename if AcoustID fails."""
    filename = Path(path).stem
    parts = re.split(r"[-–_]", filename, maxsplit=1)
    if len(parts) == 2:
        artist, title = parts[0].strip(), parts[1].strip()
        try:
            song = EasyID3(path)
        except Exception:
            song = EasyID3()
        song["artist"] = artist
        song["title"] = title
        song.save(path)
        logger.info(f"Fallback tagged from filename: {artist} - {title}")
        return True
    return False

def tag_file(path, api_key, logger):
    """Tag a single MP3 file using AcoustID + MusicBrainz."""
    try:
        if is_already_tagged(path):
            logger.info(f"Skipping already tagged file: {path}")
            return True

        # fingerprint lookup
        try:
            results = acoustid.match(api_key, path)
        except Exception as e:
            logger.warning(f"Fingerprinting failed for {path}: {e}")
            time.sleep(1)
            return False

        time.sleep(1.2)  # respect rate limit

        for score, rid, title, artist in results:
            try:
                if score > 0.6:
                    track = musicbrainzngs.get_recording_by_id(rid, includes=["artists", "releases"])
                    try:
                        track = musicbrainzngs.get_recording_by_id(rid, includes=["artists", "releases"])
                    except musicbrainzngs.NetworkError as ne:
                        logger.warning(f"Network error on {path}: {ne}. Retrying after 3s...")
                        time.sleep(3)
                        continue

                    info = track.get("recording", {})
                    try:
                        song = EasyID3(path)
                    except Exception:
                        song = EasyID3()
                        song.save(path)
                        song = EasyID3(path)
                    song["title"] = info.get("title", title or "")
                    credits = info.get("artist-credit", [])
                    names = []
                    for a in credits:
                        if isinstance(a, dict) and "artist" in a:
                            names.append(a["artist"].get("name", ""))
                        elif isinstance(a, str):
                            names.append(a)
                    song["artist"] = ", ".join(filter(None, names))

                    if info.get("releases"):
                        song["album"] = info["releases"][0].get("title", "")
                        song["date"] = info["releases"][0].get("date", "")
                    song.save()
                    logger.info(f"Successfully tagged: {path}")
                    return True
            except Exception as e2:
                logger.error(f"Error parsing MusicBrainz data for {path}: {e2}")
                traceback.print_exc()

        # no good matches
        logger.warning(f"No good matches for: {path}")
        return fallback_tag_from_filename(path, logger)

    except Exception as e:
        logger.error(f"Unhandled error tagging {path}: {e}")
        traceback.print_exc()
        return False

def run_tagger(folder, api_key, logger, progress_callback=None):
    """Run tagging on all MP3s inside given folder, reporting progress if callback provided."""
    setup_musicbrainz()
    mp3_files = [p for p in Path(folder).rglob("*.mp3")]
    total = len(mp3_files)
    logger.info(f"Found {total} MP3 files in {folder}")

    if total == 0:
        return 0, 0

    success = 0
    for idx, f in enumerate(mp3_files, start=1):
        if tag_file(str(f), api_key, logger):
            success += 1

        # ---- 🔄 Progress update ----
        if progress_callback:
            try:
                progress_callback(idx, total)
            except Exception:
                pass  # avoid GUI crash if callback fails

    logger.info(f"Successfully tagged {success}/{total} files.")
    return success, total

