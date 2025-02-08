import requests
import json
import os
import re
import threading
from time import sleep
from datetime import datetime

dau = "\033[1;32m [✓] => "

def delay(dl):
    t = datetime.now().strftime("%H:%M")
    for ti in range(int(dl) , 0, -1):
        print(dau, f'\033[1;31m DELAY REQUESTS > {ti} < Giây  ',end='\r')
        sleep(0.200)
        print(dau, f'\033[1;32m DELAY REQUESTS > {ti} < Giây  ',end='\r')
        sleep(0.200)
        print(dau, f'\033[1;33m DELAY REQUESTS > {ti} < Giây  ',end='\r')
        sleep(0.200)
        print(dau, f'\033[1;35m DELAY REQUESTS > {ti} < Giây  ',end='\r')
        sleep(0.200)
        print(dau, f'\033[1;36m DELAY REQUESTS > {ti} < Giây  ',end='\r')

def read_link_video(file_path):
    try:
        data = open(file_path).readlines()
        match = re.search(r"video/(\d+)", data[0])
        if not match:
            print(f"\033[1;32mKhông tìm thấy video ID -> Pass")
            return
        video_id = match.group(1)
        print(f"\033[1;32mTiktok video ID: {video_id}")
        data.remove(data[0])
        file2 = open(file_path, 'w')
        for text in data:
            file2.write(text)
        return video_id
    except:
        return False

def download_video(video_id):
    '''Download video from url'''
    while True:
        try:
            url = f"https://douyin.wtf/api/tiktok/app/fetch_one_video?aweme_id={video_id}"
            payload = {}
            headers = {
                'accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, data=payload)
            if response.status_code == 429:
                print(f"\033[1;31m [!] Requests quá nhanh: {response.status_code} - Re-Download video ID: {video_id}")
                sleep(3)
                continue
            link_download = response.json()['data']['video']['play_addr']['url_list'][0]
            name_video = response.json()['data']['desc']
            response_download = requests.get(link_download, stream=True)
            name_video = re.sub(r'[<>:"/\\|?*]', "_", name_video)
            with open(f"./Video/{name_video}.mp4", "wb") as file:
                file.write(response_download.content)
            print(f"\033[1;32mDownload thành công video: {video_id}")
            return True
        except Exception as e:
            print(f"\033[1;31m [!] Warning: {response.status_code} - {e}")
            return False

def main_tool():
    try:
        video_id = read_link_video(file_path="url_tiktok.txt")
        if video_id:
            download_video(video_id)
    except:
        return False

if __name__=="__main__":
    try:
        stream = int(input(f"\033[1;32m~THREAD ( <= 5): "))
        dl = int(input("DELAY ( >= 10 ): "))
        if stream > 5 or dl < 10:
            print(f"\033[1;32m~Giá trị không hợp lệ, vui lòng nhập lại.")
            exit()
        
        while True:
            threads = [threading.Thread(target=main_tool) for _ in range(stream)]
            for thread in threads:
                thread.start()
                sleep(0.2)
            for thread in threads:
                thread.join()
            
            delay(dl)
    except KeyboardInterrupt:
        print("\n[!] Đã dừng chương trình.")


