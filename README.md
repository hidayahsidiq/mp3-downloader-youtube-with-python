🎵 YouTube → MP3 Downloader (GUI)
A simple desktop application to download YouTube videos and convert them to MP3.Built with Python, yt-dlp, FFmpeg, and Tkinter.

PythonLicense

✨ Features
Paste one or many YouTube URLs (one per line)
Choose which folder to save the MP3 files
Select MP3 quality (128 / 192 / 256 / 320 kbps)
Option to download the full playlist
Live progress bar with speed & ETA
Log window for status messages
Runs downloads in the background — the window never freezes
📋 Requirements
Software	Version	Required
Python	3.8+	✅ Yes
FFmpeg	any	✅ Yes (for MP3 conversion)
yt-dlp	latest	✅ Yes (installed via pip)
Tkinter is already included with the standard Python installer on Windows and macOS.

🚀 Installation
Step 1 — Install Python
Download Python from https://www.python.org/downloads/
Run the installer.
⚠️ IMPORTANT (Windows): check the box "Add Python to PATH" on the first screen.
Verify the installation — open a terminal (Command Prompt / PowerShell) and run:
python --version
Step 2 — Install FFmpeg
FFmpeg is required to convert the downloaded audio into MP3.

Windows
macOS
Linux (Ubuntu / Debian)
Step 3 — Install Python dependencies
Open a terminal inside the project folder and run:

pip install yt-dlp
Or, if a requirements.txt file is provided:

pip install -r requirements.txt
▶️ How to Run
python youtube_mp3_downloader.py
📖 How to Use
Paste one or more YouTube URLs into the top box (one URL per line).
Choose the folder where MP3 files will be saved (or keep the default Downloads).
Pick the MP3 quality (default is 192 kps).
Check "Download full playlist" if your URL is a playlist and you want all songs.
Click Download & Convert to MP3.
Watch the progress bar — when done, a popup appears and your MP3s are in the chosen folder.
❓ Troubleshooting
Problem	Solution
'python' is not recognized…	Python is not on PATH. Reinstall Python and check "Add Python to PATH".
ERROR: ffprobe/ffmpeg not found	FFmpeg is missing or not on PATH. Redo Step 2, or set ffmpeg_location in the script.
Download fails / errors from YouTube	YouTube changed something — update yt-dlp: pip install -U yt-dlp
MP3 files are in wrong folder	Make sure the folder path in the app exists.
Antivirus blocks the .exe (see below)	Normal false-positive for PyInstaller apps. Add an exclusion or run from source.
📦 (Optional) Build a standalone .exe for Windows
So other people don't need Python installed:

pip install pyinstallerpyinstaller --onefile --windowed youtube_mp3_downloader.py
The finished file is in the dist/ folder.

⚠️ FFmpeg still needs to be installed separately, or placed next to the exe and referenced via ffmpeg_location in the code.

📁 Project Structure
youtube-mp3-downloader/├── youtube_mp3_downloader.py   # main application├── requirements.txt            # python dependencies└── README.md                   # this file
⚠️ Disclaimer
This tool is for personal use only (e.g. downloading your own content or Creative Commons audio). Please respect YouTube's Terms of Service and copyright laws in your country.

Also create a small requirements.txt file next to it:

text

yt-dlp
Tips for sharing with other people:

Put both files (youtube_mp3_downloader.py + README.md + requirements.txt) in one folder, or push to GitHub — the README will render nicely there automatically.
The <details> sections collapse on GitHub, keeping the page clean — they still work fine if opened as plain text.
If the other laptop can't install FFmpeg on PATH, tell them to edit this line in ydl_opts:
python

"ffmpeg_location": r"C:\path\to\ffmpeg\bin",


