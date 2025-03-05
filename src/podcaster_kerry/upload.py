import requests

def upload(file_path):
    url = "https://worldofkerry-server.vercel.app/upload"
    file_id = "podcast_audio"

    with open(file_path, "rb") as file:
        files = {"file": file}
        data = {"file_id": file_id}
        response = requests.post(url, files=files, data=data)

    print(response.status_code)
    print(response.text)
