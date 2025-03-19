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

def generate(user_prompt, tags, title):
    prompt = f"{user_prompt}"
    GENERATOR_API_KEY = get_key()

    try:
        response = requests.post(
            url="https://api.gptgod.online/v1/suno/generate",
            headers={
                "Authorization": f"Bearer {GENERATOR_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Host": "api.gptgod.online",
                "Connection": "keep-alive"
            },
            data=json.dumps({
                "prompt": "",
                "gpt_description_prompt": prompt,
                "tags": tags,
                "title": title,
                "mv": "chirp-v3-5",
                "make_instrumental": True
            }),
            timeout=None
        )
        print("Response from Suno AI:", response.text)  # 打印响应内容
        response.raise_for_status()  # 检查请求是否成功

        task_id_0 = response.json()['clips'][0]['id']
        # 根据实际情况处理 task_id 后续流程
        # 示例直接返回下载链接，如果 API 返回了相关链接，可根据实际 API 修改
        music_url_0 = f"https://api.gptgod.online/v1/suno/clips/{task_id_0}/download"
        # 假设生成第二个音乐的链接流程类似
        music_url_1 = f"https://api.gptgod.online/v1/suno/clips/{task_id_0}/download?variant=2"
        return music_url_0, music_url_1

    except requests.exceptions.RequestException as e:
        print("Error in generate:", e)
        return None, None

def query_task_status(task_id_0, task_id_1):
    GENERATOR_API_KEY = get_key()
    url = f"https://api.gptgod.online/v1/suno/feed?ids={task_id_0},{task_id_1}"
    payload={}
    headers = {"Authorization": f"Bearer {GENERATOR_API_KEY}",
               'Accept': '*/*',
               'Host': 'api.gptgod.online',
               'Connection': 'keep-alive'}
    while True:
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            response.raise_for_status()
            print(f"Response Query from Suno AI:", response.text)
            task_status_0 = response.json()['clips'][0]
            task_status_1 = response.json()['clips'][1]

            if task_status_0['status'] == 'streaming'and task_status_1['status'] == 'streaming':
                return task_status_0['audio_url'], task_status_1['audio_url']
            
            elif task_status_0['status'] == 'failed' or task_status_1['status'] == 'failed':
                print("任务失败")
                return None, None
            
            else:
                print("任务尚未完成，等待5秒后再次查询...")
                time.sleep(5)  # 等待5秒后再次查询

        except requests.exceptions.RequestException as e:
            print(f"查询任务状态失败: {e}")
            return None, None