import os
import json
import requests
import time

def get_key():
    file_path = os.path.join(os.path.dirname(__file__), "credentials.json")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            secrets = json.load(f)
        return secrets['GENERATOR']['GENERATOR_API_KEY']
    else:
        raise FileNotFoundError("Credentials file not found.")

def query_task_status(task_id):
    GENERATOR_API_KEY = get_key()
    url = "https://apibox.erweima.ai/api/v1/generate/record-info"
    payload = {"taskId": task_id}
    headers = {
        "Authorization": f"Bearer {GENERATOR_API_KEY}",
        "Accept": "application/json",
        "Connection": "keep-alive"
    }
    ERROR = True
    while ERROR:
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        code = response.json()["code"]
        print("Response from query:", response.json()["msg"])

        #print(response.text)
        if code == 200:
            statusType = response.json()["data"]["status"]
            if statusType == "TEXT_SUCCESS":
                clips = response.json()["data"]["response"]["sunoData"]
                #print(clips)
                clip0 = clips[0]
                clip1 = clips[1]
                return clip0["sourceStreamAudioUrl"], clip1["sourceStreamAudioUrl"]
            else:
                print("Waiting for the audio generation task to complete...")
            time.sleep(5)
        else:
            print("Error querying task status:", code)
            ERROR = False
            return None, None


def generate(user_prompt, style, title):
    prompt = f"{user_prompt}"
    GENERATOR_API_KEY = get_key()
    payload = {
        "prompt": prompt,
        "style": style,
        "title": title,
        "customMode": True,
        "instrumental": True,
        "model": "V4",
        "negativeTags": "Relaxing Piano",
        "callBackUrl": "https://api.example.com/callback"
    }
    try:
        response = requests.post(
            url="https://apibox.erweima.ai/api/v1/generate",
            headers={
                "Authorization": f"Bearer {GENERATOR_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Connection": "keep-alive"
            },
            data=json.dumps(payload),
            timeout=None
        )
        print("Response from Suno AI:", response.text)
        response.raise_for_status()
        task_id = response.json()["data"]["taskId"]
        print("Task created with task id:", task_id)
        music_url_0, music_url_1 = query_task_status(task_id)
        print("Music URLs:", music_url_0, music_url_1)
        return music_url_0, music_url_1

    except requests.exceptions.RequestException as e:
        print("Error in generate:", e)
        return None, None