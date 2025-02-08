import os
import re
import random
import datetime
import requests
from random import randint

from Module.facebook import Reels
from Module.db import Database

def get_today():
    return datetime.date.today().isoformat()

with open('via_bm.txt', 'r', encoding='utf-8') as file:
    data = file.readline()

cookie = data.split('|')[0].strip()
token_profile = data.split('|')[1].strip()

reels = Reels(cookie, token_profile)
list_page = reels.get_token_page()

db = Database()  # Khởi tạo một instance duy nhất

try:
    for page in list_page['accounts']['data']:
        page_info = {
            "page_token": page['access_token'],
            "name": page['name'],
            "id": page['id'],
            "reels_post": {}
        }
        video_of_day = random.choice(os.listdir("./Video"))
        video_title = re.sub(r"#\S+", "", video_of_day).replace(".mp4", "").strip()
        
        today = get_today()
        status_upload = db.check_data(page_info['id'], page_info['name'], today)
        if status_upload:
            print(f"\033[1;32m[ Datetime ]\033[0m {today} -> {page['name']} <- đã up Reels -> Pass")
            continue
        page_info['reels_post'][today] = [video_of_day]

        reels = Reels(cookie, token_profile)
        status_upload = reels.upload_reels(page_info['name'], page_info['id'], page_info['page_token'], f"./Video/{video_of_day}", video_title)
        if status_upload is False:
            print(f"\033[1;31m[ Reels ]\033[0m -> {page_info['name']} <- | Limit Upload")
            continue

        db.insert_videos(page_info["id"], page_info['name'], today, page_info['reels_post'][today])

finally:
    db.close()  # Đóng kết nối sau khi chạy xong
