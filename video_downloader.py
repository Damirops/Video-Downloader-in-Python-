import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp


## Potrebne bilbolteke za da proradi program: 

##   pip install yt-dlp
## u cmd: winget install Gyan.FFmpeg

class YouTubeDownloaderApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Windows YouTube Downloader")
    self.root.geometry("600x420")
    self.root.resizable(False, False)

    # Styling for modern look
    style = ttk.Style()
    style.theme_use("clam")

    # --- 1. Insert Link Section ---
    link_frame = ttk.LabelFrame(root, text=" Insert Link ", padding=10)
    link_frame.pack(fill="x", padx=20, pady=10)

    self.link_entry = ttk.Entry(link_frame, width=65)
    self.link_entry.pack(side="left", padx=5, ipady=3)

    # --- 2. Download Location Section ---
    loc_frame = ttk.LabelFrame(root, text=" Download Location ", padding=10)
    loc_frame.pack(fill="x", padx=20, pady=10)

    self.loc_entry = ttk.Entry(loc_frame, width=52)
    self.loc_entry.pack(side="left", padx=5, ipady=3)
    # Set default location to user's Downloads folder
    default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    self.loc_entry.insert(0, default_download_path)

    browse_btn = ttk.Button(loc_frame, text="Browse", command=self.select_folder)
    browse_btn.pack(side="right", padx=5)

    # --- 3. Options Section (Quality & FPS) ---
    opt_frame = ttk.LabelFrame(
        root, text=" Video Options (Quality & FPS) ", padding=10
    )
    opt_frame.pack(fill="x", padx=20, pady=10)

    # Quality Selection
    ttk.Label(opt_frame, text="Quality:").grid(
        row=0, column=0, sticky="w", padx=5
    )
    self.quality_var = tk.StringVar(value="4K")
    qualities = ["240p", "360p", "480p", "720p", "1080p", "1440p", "4K"]
    self.quality_menu = ttk.Combobox(
        opt_frame,
        textvariable=self.quality_var,
        values=qualities,
        width=10,
        state="readonly",
    )
    self.quality_menu.grid(row=0, column=1, padx=5, sticky="w")

    # FPS Selection
    ttk.Label(opt_frame, text="FPS:").grid(row=0, column=2, sticky="w", padx=15)
    self.fps_var = tk.StringVar(value="60")
    fps_options = ["30", "60"]
    self.fps_menu = ttk.Combobox(
        opt_frame,
        textvariable=self.fps_var,
        values=fps_options,
        width=8,
        state="readonly",
    )
    self.fps_menu.grid(row=0, column=3, padx=5, sticky="w")

    # --- 4. Start Button & Progress Bar ---
    action_frame = ttk.Frame(root, padding=10)
    action_frame.pack(fill="x", padx=20, pady=5)

    self.start_btn = ttk.Button(
        action_frame, text="Start Download", command=self.start_download_thread
    )
    self.start_btn.pack(fill="x", ipady=5, pady=(0, 10))

    self.progress_bar = ttk.Progressbar(
        action_frame, orient="horizontal", length=540, mode="determinate"
    )
    self.progress_bar.pack(fill="x")

  def select_folder(self):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
      self.loc_entry.delete(0, tk.END)
      self.loc_entry.insert(0, folder_selected)

  def start_download_thread(self):
    url = self.link_entry.get().strip()
    save_path = self.loc_entry.get().strip()

    if not url:
      messagebox.showerror(
          "Error", "Please insert a valid YouTube link in the first box."
      )
      return

    if not save_path or not os.path.isdir(save_path):
      messagebox.showerror("Error", "Please select a valid download location.")
      return

    # Disable start button to prevent multiple clicks while downloading
    self.start_btn.config(state="disabled")
    self.progress_bar["value"] = 0

    # Run the download in a separate thread so the GUI doesn't freeze
    threading.Thread(
        target=self.download_video, args=(url, save_path), daemon=True
    ).start()

  def progress_hook(self, d):
    if d["status"] == "downloading":
      percent_str = d.get("_percent_str", "0%").strip()
      # Clean up potential ANSI escape color codes from yt-dlp output strings
      percent_str = (
          percent_str.replace("%", "").replace("\x1b[0m", "").strip()
      )
      for code in ["\x1b[0;32m", "\x1b[0;33m", "\x1b[1;32m"]:
        percent_str = percent_str.replace(code, "")
      try:
        val = float(percent_str)
        self.progress_bar["value"] = val
        self.root.update_idletasks()
      except ValueError:
        pass

  def download_video(self, url, save_path):
    selected_quality = self.quality_var.get().replace("p", "")
    selected_fps = self.fps_var.get()

    # Map height selection for yt-dlp format filter
    height_limit = int(selected_quality) if selected_quality.isdigit() else 2160

    # yt-dlp configuration to ensure highest quality matching the constraints
    ydl_opts = {
        # Select best video matching height and fps criteria + best audio, fallback to best overall
        "format": (
            f"bestvideo[height<={height_limit}][fps={selected_fps}]+bestaudio/"
            f"bestvideo[height<={height_limit}]+bestaudio/best"
        ),
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "progress_hooks": [self.progress_hook],
    }

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
      self.progress_bar["value"] = 100
      messagebox.showinfo("Success", "Video downloaded successfully without loss!")
    except Exception as e:
      messagebox.showerror("Download Error", f"An error occurred:\n{str(e)}")
    finally:
      self.start_btn.config(state="normal")


if __name__ == "__main__":
  root = tk.Tk()
  app = YouTubeDownloaderApp(root)
  root.mainloop()
