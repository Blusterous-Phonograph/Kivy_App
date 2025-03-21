import time
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
import requests
import os

name = "Result"

class ResultView(Screen):
    def __init__(self, music_url_0, music_url_1, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.music_url_0 = music_url_0
        self.music_url_1 = music_url_1
        self.sound0 = None
        self.sound1 = None
        self.gen_time = time.time()  # 记录接收到结果的时间

        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.info_label = Label(text="Waiting for generated music...", size_hint=(1, 0.2), font_name="Roboto")
        self.layout.add_widget(self.info_label)

        self.play_btn_0 = Button(text="Play Music 1", size_hint=(1, 0.15), font_name="Roboto")
        self.play_btn_0.bind(on_press=self.play_music0)
        self.layout.add_widget(self.play_btn_0)

        self.download_btn_0 = Button(text="Download Music 1", size_hint=(1, 0.15), font_name="Roboto")
        self.download_btn_0.bind(on_press=self.download_music0)
        self.layout.add_widget(self.download_btn_0)

        self.play_btn_1 = Button(text="Play Music 2", size_hint=(1, 0.15), font_name="Roboto")
        self.play_btn_1.bind(on_press=self.play_music1)
        self.layout.add_widget(self.play_btn_1)

        self.download_btn_1 = Button(text="Download Music 2", size_hint=(1, 0.15), font_name="Roboto")
        self.download_btn_1.bind(on_press=self.download_music1)
        self.layout.add_widget(self.download_btn_1)

        # Back 按钮：点击后返回 Upload_view，并重置状态
        self.back_btn = Button(text="Back to Upload Screen", size_hint=(1, 0.15), font_name="Roboto")
        self.back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_btn)

        self.add_widget(self.layout)

    def update_results(self, url0, url1):
        self.music_url_0 = url0
        self.music_url_1 = url1
        self.gen_time = time.time()  # 更新接收到数据的时间
        self.info_label.text = "Music generated successfully. \nClick Back to generate another."
        # 自动切换到当前屏幕（Result_view）
        if self.manager:
            self.manager.current = self.name

    def check_status(self):
        # 超过40秒仍未获得 URL，则显示生成失败
        if (not self.music_url_0 or not self.music_url_1) and (time.time() - self.gen_time > 40):
            self.info_label.text = "Music generation failed. \nClick Back to try again."
        elif self.music_url_0 and self.music_url_1:
            self.info_label.text = "Music generated successfully. \nClick Back to generate another."

    def stop_all_audio(self):
        # 停止当前播放的所有音频
        if self.sound0 and getattr(self.sound0, "state", None) == "play":
            self.sound0.stop()
        if self.sound1 and getattr(self.sound1, "state", None) == "play":
            self.sound1.stop()

    def play_music0(self, instance):
        # 停止所有正在播放的音频后，再进行播放 Music 1
        self.stop_all_audio()
        tempo_folder = "temp"
        if not os.path.exists(tempo_folder):
            os.makedirs(tempo_folder)
        file_path = os.path.join(tempo_folder, "temp0.mp3")
        # 检查本地是否已存在该文件
        if os.path.exists(file_path):
            self.sound0 = SoundLoader.load(file_path)
            if self.sound0:
                self.sound0.play()
            else:
                self.info_label.text = "Local file load failed, re-requesting Music 1..."
                try:
                    r = requests.get(self.music_url_0)
                    r.raise_for_status()
                    with open(file_path, "wb") as f:
                        f.write(r.content)
                    self.sound0 = SoundLoader.load(file_path)
                    if self.sound0:
                        self.sound0.play()
                    else:
                        self.info_label.text = "Failed to load MP3 for Music 1 even after re-download."
                except Exception as e:
                    self.info_label.text = f"Error re-requesting Music 1: {e}"
        else:
            try:
                r = requests.get(self.music_url_0)
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(r.content)
                self.sound0 = SoundLoader.load(file_path)
                if self.sound0:
                    self.sound0.play()
                else:
                    self.info_label.text = "Failed to load MP3 for Music 1 after download, please try again."
            except Exception as e:
                self.info_label.text = f"Error downloading Music 1: {e}"

    def play_music1(self, instance):
        # 停止所有正在播放的音频后，再进行播放 Music 2
        self.stop_all_audio()
        tempo_folder = "temp"
        if not os.path.exists(tempo_folder):
            os.makedirs(tempo_folder)
        file_path = os.path.join(tempo_folder, "temp1.mp3")
        if os.path.exists(file_path):
            self.sound1 = SoundLoader.load(file_path)
            if self.sound1:
                self.sound1.play()
            else:
                self.info_label.text = "Local file load failed, re-requesting Music 2..."
                try:
                    r = requests.get(self.music_url_1)
                    r.raise_for_status()
                    with open(file_path, "wb") as f:
                        f.write(r.content)
                    self.sound1 = SoundLoader.load(file_path)
                    if self.sound1:
                        self.sound1.play()
                    else:
                        self.info_label.text = "Failed to load MP3 for Music 2 even after re-download."
                except Exception as e:
                    self.info_label.text = f"Error re-requesting Music 2: {e}"
        else:
            try:
                r = requests.get(self.music_url_1)
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(r.content)
                self.sound1 = SoundLoader.load(file_path)
                if self.sound1:
                    self.sound1.play()
                else:
                    self.info_label.text = "Failed to load MP3 for Music 2 after download, please try again."
            except Exception as e:
                self.info_label.text = f"Error downloading Music 2: {e}"

    def download_music0(self, instance):
        if self.music_url_0:
            try:
                r = requests.get(self.music_url_0)
                r.raise_for_status()
                # 确保下载文件夹存在
                download_folder = "download"
                if not os.path.exists(download_folder):
                    os.makedirs(download_folder)
                file_path = os.path.join(download_folder, "downloaded_output_0.mp3")
                with open(file_path, "wb") as f:
                    f.write(r.content)
                self.info_label.text = f"Music 1 downloaded successfully to {file_path}"
            except Exception as e:
                self.info_label.text = f"Error downloading Music 1: {e}"

    def download_music1(self, instance):
        if self.music_url_1:
            try:
                r = requests.get(self.music_url_1)
                r.raise_for_status()
                download_folder = "download"
                if not os.path.exists(download_folder):
                    os.makedirs(download_folder)
                file_path = os.path.join(download_folder, "downloaded_output_1.mp3")
                with open(file_path, "wb") as f:
                    f.write(r.content)
                self.info_label.text = f"Music 2 downloaded successfully to {file_path}"
            except Exception as e:
                self.info_label.text = f"Error downloading Music 2: {e}"

    def go_back(self, instance):
        # 停止所有正在播放的音频
        self.stop_all_audio()
        # 清空 temp 文件夹下的所有内容
        temp_folder = "temp"
        if os.path.exists(temp_folder):
            for filename in os.listdir(temp_folder):
                file_path = os.path.join(temp_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)
                except Exception as e:
                    self.info_label.text += f"\nError clearing temp file {file_path}: {e}"
        # 重置状态：清空 URL、重新计时，并返回 Upload_view 屏幕
        self.music_url_0 = ""
        self.music_url_1 = ""
        self.gen_time = time.time()
        self.info_label.text = "Waiting for generated music..."
        if self.manager:
            self.manager.current = "Upload"