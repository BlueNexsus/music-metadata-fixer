try:
    import PySimpleGUI4 as sg
    _PYSIMPLEGUI_IMPORT_ERROR = None
except Exception as _err:
    sg = None
    _PYSIMPLEGUI_IMPORT_ERROR = _err

# Cast the module to Any for static type checkers so attribute access (Text, Window, etc.)
# doesn't generate false-positive errors from static analyzers that don't know PySimpleGUI.
from typing import Any, cast
if sg is not None:
    sg = cast(Any, sg)
import threading
import io
import sys
from core.file_utils import run_auto_tag_pipeline

# ---------------------------------------------------------------------------
# Redirect stdout/stderr to the GUI console
# ---------------------------------------------------------------------------
class StdoutRedirector(io.TextIOBase):
    def __init__(self, window, key):
        self.window = window
        self.key = key

    def write(self, data):
        # Ensure we always work with a string and ignore empty writes
        try:
            s = str(data)
        except Exception:
            return 0

        if s.strip():
            # Send the text as an event value so the main thread can append it
            try:
                self.window.write_event_value(self.key, s)
            except Exception:
                # If the window is closed or not available, silently ignore
                pass

        return len(s)

    def flush(self):
        return None


# ---------------------------------------------------------------------------
# GUI Worker Thread
# ---------------------------------------------------------------------------
def run_pipeline_thread(window, folder_path):
    """Runs the tagging pipeline in a thread."""
    try:
        run_auto_tag_pipeline(folder_path)
        window.write_event_value("-DONE-", "✅ Tagging completed successfully.")
    except Exception as e:
        window.write_event_value("-ERROR-", str(e))


# ---------------------------------------------------------------------------
# GUI Layout
# ---------------------------------------------------------------------------
def main():
    if sg is None:
        # Friendly popup if PySimpleGUI isn't installed. Use tkinter if available
        msg = (
            "PySimpleGUI is not available. Please install it to run the GUI.\n\n"
            "Run:\n    pip install PySimpleGUI\n\n"
            "or:\n    pip install -r requirements.txt\n\n"
            f"Original import error: {_PYSIMPLEGUI_IMPORT_ERROR}"
        )
        try:
            import tkinter as _tk
            from tkinter import messagebox as _mb

            # Show a small error dialog and return without raising so imports stay safe
            _root = _tk.Tk()
            _root.withdraw()
            _mb.showerror("Missing dependency: PySimpleGUI", msg)
            try:
                _root.destroy()
            except Exception:
                pass
        except Exception:
            # tkinter not available — print to stderr as a fallback
            print(msg, file=sys.stderr)

        return

    getattr(sg, "theme")("DarkGrey13")

    # Create a small factory that calls PySimpleGUI attributes via getattr at runtime.
    # This avoids static analyzers reporting that PySimpleGUI doesn't expose these names.
    def E(name, *a, **k):
        return getattr(sg, name)(*a, **k)

    layout = [
        [E("Text", "🎵 Music Metadata Fixer", font=("Segoe UI", 16, "bold"))],
        [E("Text", "Source Folder:"), E("Input", key="-SRC-", expand_x=True), E("FolderBrowse", "Browse")],
        [E("Button", "Start", key="-START-", size=(10, 1), button_color=("white", "#007ACC")),
         E("Button", "Exit", key="-EXIT-", size=(10, 1))],
        [E("ProgressBar", 100, orientation="h", size=(40, 20), key="-PROG-", visible=False)],
        [E("Multiline", size=(90, 20), key="-OUTPUT-", autoscroll=True, reroute_stdout=False,
                      background_color="#1e1e1e", text_color="white", font=("Consolas", 9))],
    ]

    window = getattr(sg, "Window")("Metadata Fixer", layout, finalize=True, resizable=True)

    # Save original streams so we can restore them on exit
    _original_stdout = sys.stdout
    _original_stderr = sys.stderr

    # Redirect system output to the GUI (-LOG- event)
    sys.stdout = StdoutRedirector(window, "-LOG-")
    sys.stderr = StdoutRedirector(window, "-LOG-")

    # ---------------------------------------------------------------------------
    # Main Event Loop
    # ---------------------------------------------------------------------------
    try:
        while True:
            event, values = window.read()

            if event in (getattr(sg, "WIN_CLOSED", sg), "-EXIT-"):
                break

            elif event == "-START-":
                folder = values["-SRC-"].strip()
                if not folder:
                    getattr(sg, "popup_error")("Please select a source folder first.")
                    continue

                window["-OUTPUT-"].update("")
                window["-PROG-"].update(0, visible=True)
                window["-START-"].update(disabled=True)

                threading.Thread(target=run_pipeline_thread, args=(window, folder), daemon=True).start()
                print(f"🚀 Started tagging pipeline for: {folder}\n")

            elif event == "-LOG-":
                # Show logs incrementally
                window["-OUTPUT-"].update(values["-LOG-"], append=True)

            elif event == "-DONE-":
                window["-OUTPUT-"].update(values["-DONE-"] + "\n", append=True)
                window["-START-"].update(disabled=False)
                window["-PROG-"].update(100)

            elif event == "-ERROR-":
                getattr(sg, "popup_error")(f"An error occurred:\n\n{values['-ERROR-']}")
                window["-START-"].update(disabled=False)
    finally:
        # Restore original streams so further prints go to the console as expected
        try:
            sys.stdout = _original_stdout
        except Exception:
            pass
        try:
            sys.stderr = _original_stderr
        except Exception:
            pass
        window.close()


if __name__ == "__main__":
    main()
