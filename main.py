import sys
import os
import subprocess

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QComboBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt

from pytubefix import YouTube

class YouTubeAudioDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Audio Downloader")
        self.setFixedSize(400, 250)
        self.init_ui()

        # Ganti dengan path ffmpeg kamu jika belum masuk PATH
        self.ffmpeg_path = "C:/FFMPEG/bin/ffmpeg.exe"  # atau contoh: "C:\FFMPEG\bin\ffmpeg.exe"

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("YouTube URL:"))
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Paste the YouTube URL here...")
        layout.addWidget(self.url_entry)

        layout.addWidget(QLabel("Choose Audio Format:"))
        self.format_box = QComboBox()
        self.format_box.addItems(["MP3", "AAC", "WAV", "AIF", "Apple Lossless (ALAC)"])
        layout.addWidget(self.format_box)

        download_button = QPushButton()
        download_button.setIcon(QIcon("D:/Code/Python/PySide/mp3 downloader youtube/download (4).png"))
        download_button.setIconSize(QSize(32, 32))
        download_button.setFixedSize(50, 50)
        download_button.setToolTip("Download & Convert")
        download_button.clicked.connect(self.download_and_convert)
        layout.addWidget(download_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def download_and_convert(self):
        url = self.url_entry.text().strip()
        format_choice = self.format_box.currentText()

        extensions = {
            "MP3": (".mp3", {"acodec": "libmp3lame"}),
            "AAC": (".aac", {"acodec": "aac"}),
            "WAV": (".wav", {"acodec": "pcm_s16le"}),
            "AIF": (".aif", {"acodec": "pcm_s16be"}),
            "Apple Lossless (ALAC)": (".m4a", {"acodec": "alac"})
        }

        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a YouTube URL.")
            return

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()

            if not stream:
                raise Exception("No audio stream found.")

            download_folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
            if not download_folder:
                return

            QMessageBox.information(self, "Downloading", "Downloading audio...")
            out_file = stream.download(output_path=download_folder)
            base = os.path.splitext(out_file)[0]

            ext, codec_opts = extensions.get(format_choice, (".mp3", {"acodec": "libmp3lame"}))
            final_file = base + ext

            QMessageBox.information(self, "Converting", f"Converting to {format_choice}...")

            # Build ffmpeg command
            input_args = ['-i', out_file]
            codec_args = []
            for k, v in codec_opts.items():
                codec_args.extend([f'-{k}', v])
            ffmpeg_command = [self.ffmpeg_path, *input_args, *codec_args, final_file]

            # Run ffmpeg
            result = subprocess.run(
                ffmpeg_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                raise Exception(f"FFmpeg error:\n{result.stderr.strip()}")

            os.remove(out_file)
            QMessageBox.information(self, "Success", f"Saved as:\n{final_file}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeAudioDownloader()
    window.show()
    sys.exit(app.exec())
