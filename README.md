# 📥  Video Downloader In Python on Windows 11
Becauuse thi program is made on operating system Windows 11. 

A desktop applications for downloading YouTube videos in high quality (up 4k and 60 fps), built with **Python**, **Tikinter**, and **yt-dlp***

## 🚀 Features
- **Customizable Quality & FPS:** Choose your preferred video resolution (from 240p up to 4K) and frame rate (30 or 60 FPS).
- **Custom Download Location:** Automatically defaults to your system's *Downloads* folder, with an easy-to-use directory browser.
- **Multithreading Support:** Runs downloads in a background thread to prevent the graphical interface (GUI) from freezing
- **Real-time Progress Bar:** Tracks the download progress dynamically.
- **Automatic Merging:** Automatically merges video and audio streams into an MP4 file using FFmpeg.

--
##  🛠️ Prerequisites & Installation
Before running the application, make sure you have following installed on your  installed on your system:
1. **Python** (version 3.x recommended) or my version I use  (Python 3.12.9)
2. **FFmpeg** (Required for merging video and audio formats correctly)
 
### 1. Installed FFmpeg(Windows)
open your terminal('cmd' or PowerShell) nad install FFmpeg via winget:
                
                
               winget install Gyan.FFmpeg



Open your terminal nad install yt-dlp I used Python 3.12.9 and the command is:
  
    
    pip install yt-dlp

The last on thing is how to run the program:
      
      
      python3 video_downloader.py 
    
      

