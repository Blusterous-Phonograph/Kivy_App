from flask import Flask, request, jsonify
from model import Suno

app = Flask(__name__)

@app.route('/upload_text', methods=['POST'])
def upload_text():
    prompt = request.form.get('prompt')
    style = request.form.get('style')
    title = request.form.get('title')
    if prompt and style and title:
        print("收到文本:", prompt, style, title)
        # 调用 Suno.generate 生成音乐文件链接
        music_url_0, music_url_1 = Suno.generate(prompt, style, title)
        print("音乐链接:", music_url_0, music_url_1)
        if music_url_0 and music_url_1:
            return jsonify({
                "status": "success",
                "message": "文本已接收，音乐生成成功",
                "music_url_0": music_url_0,
                "music_url_1": music_url_1
            })
        else:
            return jsonify({"status": "error", "message": "生成音乐失败"}), 500
    return jsonify({"status": "error", "message": "缺少文本、标签或标题"}), 400

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"status": "error", "message": "未上传音频文件"}), 400
    audio = request.files['audio']
    # 保存或处理音频文件
    audio.save("uploaded_audio.wav")
    print("收到音频文件")
    return jsonify({"status": "success", "message": "音频已接收"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)