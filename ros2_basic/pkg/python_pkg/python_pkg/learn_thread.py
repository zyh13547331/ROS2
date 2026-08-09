import threading
import requests

class DownLoad:
    def download(self, url, callback_count ):
        print(f"线程：{threading.get_ident()}，开始下载：{url}")
        response = requests.get(url)
        response.encoding = 'utf-8'
        callback_count(url, response.text) #调用回调函数

    def start_download(self, url, callback_count):
        threading.Thread(target=self.download, args=(url, callback_count)).start()

def word_count(url, result):
    """普通函数，用于回调"""
    print(f"{url}:{len(result)}->{result[:5]}")

def main():
    download = DownLoad()
    download.start_download("http://localhost:8000/nocel1.txt", word_count)
    download.start_download("http://localhost:8000/nocel2.txt", word_count)
    download.start_download("http://localhost:8000/nocel3.txt", word_count)