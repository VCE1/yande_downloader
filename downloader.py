import requests
import os
import logging
import datetime
import time
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor

class Downloader:
    def __init__(self, gui):
        self.gui = gui
        self.stop_flag = False
        self.max_retries = 3

    def download_images_thread(self, download_original):
        self.stop_flag = False
        search_tag = self.gui.tag_entry.get()
        directory = self.gui.directory_entry.get()

        if not directory:
            directory = os.path.join(os.getcwd(), datetime.date.today().strftime('%Y%m%d') + '_' + search_tag)

        if not os.path.exists(directory):
            os.makedirs(directory)

        start_page = int(self.gui.start_page_entry.get())
        end_page = int(self.gui.end_page_entry.get())

        if start_page > end_page:
            messagebox.showerror("Error", "Invalid page range")
            return

        with ThreadPoolExecutor() as executor:
            threads = []

            for page in range(start_page, end_page + 1):
                if self.stop_flag:
                    break

                json_data = self.get_json(page, bool(download_original))

                if json_data is None:
                    self.gui.update_log(f"Error downloading images on page {page}. Skipping...")
                    continue

                for current_post in json_data:
                    image_url = current_post['file_url']
                    image_id = current_post['id']
                    filename = os.path.join(directory, f"{image_id}")
                    file_ext = os.path.splitext(image_url)[1]  # 获取文件扩展名
                    filename_with_ext = f"{filename}{file_ext}"

                    threads.append(executor.submit(self.download_image, current_post, filename_with_ext, download_original))

                time.sleep(1)  # Sleep for 1 second between pages

            for thread in threads:
                thread.result()

        self.gui.update_log("Download complete")

    def get_json(self, page, download_original):
        url = f"https://yande.re/post.json?tags={self.gui.tag_entry.get()}&page={page}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return None

        if not download_original:
            json_data = [post for post in json_data if 'jpeg_url' in post]

        return json_data

    def download_image(self, current_post, filename, download_original):
        image_id = current_post['id']
        url = current_post['file_url'] if download_original else current_post['jpeg_url']

        retries = 0

        while retries < self.max_retries:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                self.gui.update_log(f"Downloaded: {filename}")  # 更新下载日志
                break
            except requests.exceptions.RequestException as e:
                logging.error(e)
                retries += 1
                time.sleep(1)  # Sleep for 1 second before retrying
