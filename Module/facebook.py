import requests
import json
import os

class Reels:
    def __init__(self, cookie, token_profile):
        self.cookie = cookie
        self.token_profile = token_profile
        self.headers = {
            'Content-Type': 'application/json',
            'cookie': self.cookie
        }

    def get_token_page(self):
        url = "https://graph.facebook.com/v22.0/me?fields=accounts.limit(100)"
        params = {
            'access_token': self.token_profile
        }
        response = requests.get(url, params=params)
        return response.json()

    def initialize(self, page_id, page_access_token):
        url = f"https://graph.facebook.com/v22.0/{page_id}/video_reels"
        payload = json.dumps({
            "upload_phase": "start",
            "access_token": page_access_token
        })
        response = requests.post(url, headers=self.headers, data=payload)
        try:
            video_id = response.json()['video_id']
            return video_id
        except:
            # print(response.text)
            return False
    
    def upload(self, file_path, video_id, page_access_token):
        url = f"https://rupload.facebook.com/video-upload/v22.0/{video_id}"
        file_size = os.path.getsize(file_path)
        headers = {
            'Authorization': f'OAuth {page_access_token}',
            'offset': '0',
            'file_size': str(file_size),
            'Content-Type': 'text/plain'
        }
        with open(file_path, 'rb') as video_file:
            response = requests.post(url, headers=headers, data=video_file)
        if response.json()['success']:
            # print(response.json()['message'])
            return True

    def public(self, page_id, video_id, page_access_token, video_title):
        url = f"https://graph.facebook.com/v22.0/{page_id}/video_reels"
        params = {
            'access_token': page_access_token,
            'video_id': video_id,
            'upload_phase': 'finish',
            'video_state': 'PUBLISHED',
            'description': video_title
        }
        response = requests.post(url, params=params)
        if response.json()['success']:
            # print(response.json()['message'])
            return True

    def upload_reels(self, page_name, page_id, page_token, video_path, video_title):
        video_id = self.initialize(page_id, page_token)
        if video_id:
            print(f"\033[1;32m[ Reels ]\033[0m -> {page_name} <- | Video ID: {video_id}")
            status_upload = self.upload(video_path, video_id, page_token)
            if status_upload:
                print(f"\033[1;32m[ Reels ]\033[0m -> {page_name} <- | Status upload: Success")
            status_public = self.public(page_id, video_id, page_token, video_title)
            if status_public:
                print(f"\033[1;32m[ Reels ]\033[0m -> {page_name} <- | Status public: Processing")
        else:
            return False
        
if __name__=="__main__":
    with open('via_bm.txt', 'r', encoding='utf-8') as file:
        data = file.readline()

    cookie = data.split('|')[0].strip()
    token_profile = data.split('|')[1].strip()

    reels = Reels(cookie, token_profile)
    list_page = reels.get_token_page()
    # print(list_page)
    print(len(list_page['accounts']['data']))
