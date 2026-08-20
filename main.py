import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

import yt_dlp


class YtMp3Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube → MP3 Downloader")
        self.root.geometry("640x560")
        self.root.minsize(520, 460)
        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        # --- URL input (supports multiple URLs, one per line)
        url_frame = ttk.LabelFrame(self.root, text="URL(s) — one per line")
        url_frame.pack(fill="both", padx=10, pady=5)
        self.url_box = scrolledtext.ScrolledText(url_frame, height=6, wrap=tk.WORD)
        self.url_box.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Save folder selection
        folder_frame = ttk.LabelFrame(self.root, text="Save folder")
        folder_frame.pack(fill="x", padx=10, pady=5)
        self.folder_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        ttk.Entry(folder_frame, textvariable=self.folder_var).pack(
            side="left", fill="x", expand=True, padx=5, pady=5)
        ttk.Button(folder_frame, text="Browse…", command=self._browse_folder).pack(
            side="left", padx=(0, 5), pady=5)

        # --- Options
        opt_frame = ttk.LabelFrame(self.root, text="Options")
        opt_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(opt_frame, text="MP3 quality (kbps):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.quality_var = tk.StringVar(value="192")
        ttk.Combobox(opt_frame, textvariable=self.quality_var,
                     values=["128", "192", "256", "320"], width=5,
                     state="readonly").grid(row=0, column=1, padx=(0, 15), sticky="w")
        self.playlist_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_frame, text="Download full playlist",
                        variable=self.playlist_var).grid(row=0, column=2, padx=5, sticky="w")

        # --- Progress bar
        prog_frame = ttk.LabelFrame(self.root, text="Progress")
        prog_frame.pack(fill="x", padx=10, pady=5)
        self.progress = tk.DoubleVar()
        ttk.Progressbar(prog_frame, variable=self.progress, maximum=100).pack(
            fill="x", padx=5, pady=(5, 0))
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(prog_frame, textvariable=self.status_var).pack(anchor="w", padx=5, pady=5)

        # --- Download button
        self.download_btn = ttk.Button(self.root, text="Download & Convert to MP3",
                                       command=self._start_download)
        self.download_btn.pack(pady=8)

        # --- Log window
        log_frame = ttk.LabelFrame(self.root, text="Log")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_box = scrolledtext.ScrolledText(log_frame, height=7, state="disabled", wrap=tk.WORD)
        self.log_box.pack(fill="both", expand=True, padx=5, pady=5)

    # ------------------------------------------------------------- helpers
    def _browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get() or ".")
        if folder:
            self.folder_var.set(folder)

    def _log(self, msg):
        # root.after() makes this safe to call from the download thread
        def job():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", msg + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        self.root.after(0, job)

    def _set_progress(self, pct, status):
        def job():
            self.progress.set(pct)
            self.status_var.set(status)
        self.root.after(0, job)

    # -------------------------------------------------------- yt-dlp hook
    def _hook(self, d):
        if d["status"] == "downloading":
            try:
                pct = float(d.get("_percent_str", "0").strip().rstrip("%"))
            except ValueError:
                pct = 0.0
            status = (f"Downloading… {d.get('_percent_str', '').strip()}   "
                      f"Speed: {d.get('_speed_str', 'n/a').strip()}   "
                      f"ETA: {d.get('_eta_str', 'n/a').strip()}")
            self._set_progress(pct, status)
        elif d["status"] == "finished":
            self._set_progress(100, "Converting to MP3… (ffmpeg)")
            self._log("Download finished → converting with ffmpeg…")

    # ------------------------------------------------------------- actions
    def _start_download(self):
        urls = [u.strip() for u in self.url_box.get("1.0", "end").splitlines() if u.strip()]
        if not urls:
            messagebox.showwarning("No URL", "Please paste at least one URL.")
            return

        folder = self.folder_var.get().strip()
        if not os.path.isdir(folder):
            messagebox.showwarning("Invalid folder", "Please choose a valid save folder.")
            return

        self.download_btn.configure(state="disabled")
        # Run download in a background thread so the GUI doesn't freeze
        threading.Thread(target=self._download, args=(urls, folder), daemon=True).start()

    def _download(self, urls, folder):
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
            "noplaylist": not self.playlist_var.get(),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": self.quality_var.get(),
            }],
            "progress_hooks": [self._hook],
            "quiet": True,
            "ffmpeg_location": r"C:\ffmpeg-n9.0-latest-win64-lgpl-9.0\ffmpeg-n9.0-latest-win64-lgpl-9.0\bin",
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(urls)
            self._set_progress(100, "Done ✔")
            self._log("All downloads finished.")
            self.root.after(0, lambda: messagebox.showinfo("Done", "All files converted to MP3!"))
        except Exception as exc:
            self._log(f"ERROR: {exc}")
            self._set_progress(0, "Error — see log")
            self.root.after(0, lambda e=exc: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.download_btn.configure(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    YtMp3Downloader(root)
    root.mainloop()
