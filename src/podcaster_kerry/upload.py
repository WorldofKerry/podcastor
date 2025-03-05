import requests
import time
import json

def upload(file_path):
    url = "https://worldofkerry-server.vercel.app/upload"
    file_id = "podcast_audio_" + str(int(time.time()))
    with open(file_path, "rb") as file:
        files = {"file": file}
        data = {"file_id": file_id}
        response = requests.post(url, files=files, data=data)

    print(response.status_code)
    print(response.text)
    try:
        response = json.loads(response.text)
        file_id = response["file_id"]
        print(file_id)
        print(f"https://worldofkerry-server.vercel.app/download?file_id={file_id}")
    except Exception as e:
        print(e)