import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import sys
import os
from core.file_utils import run_auto_tag_pipeline, ensure_env_setup, find_mp3_files
from core import tagger
import traceback



# --- App settings ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MetadataFixerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Metadata Fixer")
        self.geometry("700x480")
        self.resizable(False, False)

        # --- Header ---
        header = ctk.CTkLabel(self, text="🎵 Music Metadata Fixer", font=("Segoe UI", 20, "bold"))
        header.pack(pady=(20, 10))

        # --- Source folder field ---
        frame_path = ctk.CTkFrame(self)
        frame_path.pack(padx=20, pady=(10, 10), fill="x")

        ctk.CTkLabel(frame_path, text="Source Folder:").pack(side="left", padx=(10, 5), pady=10)
        self.entry_path = ctk.CTkEntry(frame_path)
        self.entry_path.pack(side="left", expand=True, fill="x", padx=(0, 5), pady=10)

        self.button_browse = ctk.CTkButton(frame_path, text="Browse", width=100, command=self.browse_folder)
        self.button_browse.pack(side="right", padx=(5, 10))

        # --- Start & Exit buttons ---
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(5, 10))

        self.button_start = ctk.CTkButton(button_frame, text="Start", width=100, command=self.start_tagging)
        self.button_start.pack(side="left", padx=10)

        self.button_exit = ctk.CTkButton(button_frame, text="Exit", width=100, command=self.quit)
        self.button_exit.pack(side="left", padx=10)

        # --- Progress bar ---
        self.progress = ctk.CTkProgressBar(self, width=640)
        self.progress.pack(pady=(10, 5))
        self.progress.set(0)

        # --- Log output ---
        self.text_log = ctk.CTkTextbox(self, width=660, height=260)
        self.text_log.pack(padx=20, pady=(0, 10))
        # --- Footer ---
        footer = ctk.CTkLabel(
            self,
            text="v2.2.0  •  © BlueNexsus  •  github.com/BlueNexsus/music-metadata-fixer",
            font=("Segoe UI", 10),
            text_color="gray"
        )
        footer.pack(side="bottom", pady=(0,6))
        self.log("✅ Ready to start.\n")

    # -----------------------------------------------------------------------
    # Handlers
    # -----------------------------------------------------------------------
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select your music folder")
        if folder:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, folder)
            self.log(f"Selected folder: {folder}\n")

    def start_tagging(self):
        folder = self.entry_path.get().strip()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder first.")
            return

        # ✅ Make sure .env setup runs in main thread (prompts user if needed)
        ensure_env_setup()

        self.button_start.configure(state="disabled")
        self.progress.set(0)
        self.text_log.delete("1.0", "end")
        self.log(f"🚀 Started tagging pipeline for: {folder}\n")

        threading.Thread(target=self.run_pipeline_thread, args=(folder,), daemon=True).start()

        # --- Pre-check: see if all files are already tagged ---
        try:
            from core import tagger
            mp3_files = find_mp3_files(folder)
            if not mp3_files:
                messagebox.showinfo("No MP3 Files", "No MP3 files were found in this folder.")
                self.log("ℹ️ No MP3 files found in this folder.\n")
                return

            already_tagged = [f for f in mp3_files if tagger.is_already_tagged(f)]
            if len(already_tagged) == len(mp3_files):
                messagebox.showinfo(
                    "All Files Tagged",
                    f"🎶 All {len(mp3_files)} MP3 files in this folder are already tagged!"
                )
                self.log(f"ℹ️ All {len(mp3_files)} MP3 files are already tagged. Skipping processing.\n")
                return
        except Exception as e:
            self.log(f"⚠️ Pre-check failed: {e}\n")

        # --- Continue normally ---
        self.button_start.configure(state="disabled")
        self.progress.set(0)
        self.text_log.delete("1.0", "end")
        self.log(f"🚀 Started tagging pipeline for: {folder}\n")

        threading.Thread(target=self.run_pipeline_thread, args=(folder,), daemon=True).start()


    def run_pipeline_thread(self, folder):
        """Run the tagging pipeline in a background thread."""
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            def gui_logger(msg):
                self.log(msg + "\n")

            # redirect stdout/stderr to GUI
            sys.stdout = sys.stderr = LogRedirector(gui_logger)

            def update_progress(done, total):
                self.progress.set(done / total)
                self.update_idletasks()

            run_auto_tag_pipeline(folder, progress_callback=update_progress)

            self.progress.set(1)
            self.log("✅ Tagging completed successfully.\n")

        except Exception as e:
            self.log(f"❌ Error: {e}\n{traceback.format_exc()}\n")
            messagebox.showerror("Error", str(e))

        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            self.button_start.configure(state="normal")

    def log(self, msg):
        """Append text to the log box."""
        self.text_log.insert("end", msg)
        self.text_log.see("end")
        self.update_idletasks()


class LogRedirector:
    """Redirects print() output to the GUI log box."""
    def __init__(self, callback):
        self.callback = callback

    def write(self, data):
        if data.strip():
            self.callback(str(data))
        return len(data)

    def flush(self):
        pass


# -----------------------------------------------------------------------
# App start
# -----------------------------------------------------------------------
if __name__ == "__main__":
    app = MetadataFixerApp()
    app.mainloop()
