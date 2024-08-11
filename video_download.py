import requests
import time
import os
import json, csv, sys
from pytube import YouTube
# pip install pytube
# pip install requests

headers = {
    'User-Agent': "your_device's_user_agent",
    'Referer': 'https://www.bilibili.com/'
}
cookies = {'your_cookie_name': 'your_cookie_value'}

# Bilibili video download func
def request_cid(bid):
  http = "https://api.bilibili.com/x/player/pagelist?"
  response = requests.get(http + "bvid=" + bid, headers=headers, cookies=cookies)
  data = response.json()
  if(data["code"] == 0 ):
    return data["data"][0]["cid"]
  return "error"

def request_url(bid):
  cid = request_cid(bid)
  if(cid != "error"):
    http ="https://api.bilibili.com/x/player/playurl?"
    response = requests.get(http + "bvid=" +bid+ "&cid="+str(cid)+"&qn=32", headers=headers, cookies=cookies)
    data = response.json()
    if(data["code"] == 0 ):
      return data["data"]["durl"][0]["url"]
  return "error"

def download_video(url, file_path):
    response = requests.get(url, stream=True,  headers=headers, cookies=cookies)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print("Download complete.")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")

def request_video(bid, path):
  url = request_url(bid)
  if(url != "error"):
    download_video(url, path)


def download_video_func(video_ids, platform, data_folder):
  dir = data_folder + "/" + str(video_id)
        
  for video_id in video_ids:
      if(platform == "Bilibili"):
        if not os.path.exists(dir):
          os.mkdir(dir)
        path = dir + "/video.mp4"
        if not os.path.exists(path):
          request_video(video_id, path)
          print(video_id + " Download successful")
          time.sleep(1)

      elif(platform == "YouTube"):
       if not os.path.exists(dir):
          yt = YouTube('http://youtube.com/watch?v=' + str(video_id))
          try:
            yt.streams.filter(progressive=True, file_extension='mp4')\
              .order_by('resolution').desc().first().download(output_path = dir)
            print(video_id + " Download successful")
            time.sleep(1)
          except Exception as e:
            print(str(e))
        
          
if __name__ == "__main__":
  video_ids = []
  platform = "YouTube" # Bilibili
  data_folder =  "the_folder_store_videos"
  download_video_func(video_ids,  platform)
