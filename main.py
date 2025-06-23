import tkinter as tk
from tkinter import messagebox, filedialog
from pytubefix import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def download_and_convert():
    url = url_entry.get()
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()

        download_folder = filedialog.askdirectory(title="Select Download Folder")
        if not download_folder:
            return

        messagebox.showinfo("Downloading", "Downloading audio...")
        out_file = stream.download(output_path=download_folder)
        
        messagebox.showinfo("Converting", "Converting to MP3...")

        mp3_file = os.path.splitext(out_file)[0] + ".mp3"
        with VideoFileClip(out_file) as video:
            video.audio.write_audiofile(mp3_file)

        os.remove(out_file)
        messagebox.showinfo("Success", f"Saved as {mp3_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("YouTube to MP3 Downloader")
root.geometry("400x180")

tk.Label(root, text="YouTube URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack()

tk.Button(root, text="Download & Convert", command=download_and_convert).pack(pady=20)

root.mainloop()
