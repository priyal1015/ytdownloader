#importing tkinter
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from pytube import YouTube
import threading

#creating functions here
#function for downloading
def start_download():
    yt_link = link.get()
    try:
        yt = YouTube(yt_link, on_progress_callback=show_progress)
        video_stream = yt.streams.get_highest_resolution()

        destination_folder = filedialog.askdirectory()
        if destination_folder:
            download_label.config(text="Downloading...", foreground="blue")
            download_button.config(state=tk.DISABLED)
            download_options_label.config(text="")
            options_button.config(state=tk.DISABLED)
            download_thread = threading.Thread(target=download_video, args=(video_stream, destination_folder))
            download_thread.start()
    except Exception as e:
        download_label.config(text="Download failed!", foreground="red")
        download_button.config(state=tk.NORMAL)
        options_button.config(state=tk.NORMAL)

def download_video(stream, destination_folder):
    try:
        stream.download(output_path=destination_folder)
        download_label.config(text="Downloaded!", foreground="green")
    except Exception as e:
        download_label.config(text="Download failed!", foreground="red")
    finally:
        download_button.config(state=tk.NORMAL)
        options_button.config(state=tk.NORMAL)

#function which will show progress 
def show_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar['value'] = percentage_of_completion
    root.update()

#function for options
def show_options():
    download_format = simpledialog.askstring("Download Options", "Enter download format (e.g., mp4, webm, etc.):")

    if download_format:
        download_options_label.config(text="Download Format: " + download_format)
    else:
        download_options_label.config(text="No options selected")

#creating the main/root gui
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("400x400")
root.resizable(width=False, height=False)
root.iconbitmap('downloader icon.ico')

main_frame = ttk.Frame(root, padding=20)
main_frame.grid(row=0, column=0)

# Create a custom font style for the link label
link_label_font = ('Arial', 14)

# Create a ttk style for the link label
style = ttk.Style()
style.configure('LinkLabel.TLabel', font=link_label_font, foreground='black', background='lightgrey')

#creating a label
link_label = ttk.Label(main_frame, text="Enter YouTube Link:", style='LinkLabel.TLabel')
link_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")

#lets now create entry widget
link = tk.StringVar()
link_entry = ttk.Entry(main_frame, width=40, textvariable=link)
link_entry.grid(row=1, column=0, padx=10, pady=5)

#let us now create a download button
download_button = ttk.Button(main_frame, text="Download", command=start_download)
download_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

#creating an option button
options_button = ttk.Button(main_frame, text="Options", command=show_options)
options_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

#creating a label which will show 'downloaded' or 'download failed'
download_label = ttk.Label(main_frame, text="")
download_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

#creating a progress bar
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

download_options_label = ttk.Label(main_frame, text="")
download_options_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Set the background and foreground colors for the download button
download_button.configure(style='Download.TButton')

# Create a ttk style for the download button
style = ttk.Style()
style.configure('Download.TButton', background='green', foreground='black', font=('Arial', 12), padding=6)

#lets run the main loop
root.mainloop()