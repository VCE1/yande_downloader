import tkinter as tk
from tkinter import messagebox
from downloader import Downloader
import threading

class YandeDownloader:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Yande_Downloader")
        self.window.geometry("500x500")

        self.downloader = Downloader(self)

        self.create_widgets()

    def create_widgets(self):
        tag_label = tk.Label(self.window, text="Search Tag:")
        tag_label.pack()

        self.tag_entry = tk.Entry(self.window)
        self.tag_entry.pack()

        start_page_label = tk.Label(self.window, text="Start Page:")
        start_page_label.pack()

        self.start_page_entry = tk.Entry(self.window)
        self.start_page_entry.pack()

        end_page_label = tk.Label(self.window, text="End Page:")
        end_page_label.pack()

        self.end_page_entry = tk.Entry(self.window)
        self.end_page_entry.pack()

        directory_label = tk.Label(self.window, text="Download Directory:")
        directory_label.pack()

        self.directory_entry = tk.Entry(self.window)
        self.directory_entry.pack()

        self.original_var = tk.BooleanVar()
        self.original_var.set(True)
        original_checkbutton = tk.Checkbutton(self.window, text="Download Original", variable=self.original_var)
        original_checkbutton.pack()

        self.log_text = tk.Text(self.window, height=10)
        self.log_text.pack(side=tk.TOP)

        download_button = tk.Button(self.window, text="Download", command=self.start_download_thread)
        download_button.pack()

        stop_button = tk.Button(self.window, text="Stop", command=self.stop_download)
        stop_button.pack()

    def start_download_thread(self):
        if not self.tag_entry.get():
            messagebox.showerror("Error", "Please enter a search tag")
            return
        download_original = self.original_var.get()
        threading.Thread(target=self.downloader.download_images_thread, args=(download_original,)).start()

    def stop_download(self):
        self.downloader.stop_flag = True

    def update_log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

    def run(self):
        self.window.mainloop()
