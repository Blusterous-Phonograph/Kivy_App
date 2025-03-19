from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
import requests

name = "Result"

class ResultView(Screen):
    def __init__(self, music_url_0, music_url_1, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.music_url_0 = music_url_0
        self.music_url_1 = music_url_1
        self.sound0 = None
        self.sound1 = None

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

        self.back_btn = Button(text="Back to Upload Screen", size_hint=(1, 0.15), font_name="Roboto")
        self.back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_btn)

        self.add_widget(self.layout)

    def update_results(self, url0, url1):
        self.music_url_0 = url0
        self.music_url_1 = url1
        self.info_label.text = "Music generated successfully, please choose to play or download"

    def play_music0(self, instance):
        if self.music_url_0:
            try:
                r = requests.get(self.music_url_0)
                r.raise_for_status()
                with open("temp0.mp3", "wb") as f:
                    f.write(r.content)
                self.sound0 = SoundLoader.load("temp0.mp3")
                if self.sound0:
                    self.sound0.play()
            except Exception as e:
                self.info_label.text = f"Error playing Music 1: {e}"

    def play_music1(self, instance):
        if self.music_url_1:
            try:
                r = requests.get(self.music_url_1)
                r.raise_for_status()
                with open("temp1.mp3", "wb") as f:
                    f.write(r.content)
                self.sound1 = SoundLoader.load("temp1.mp3")
                if self.sound1:
                    self.sound1.play()
            except Exception as e:
                self.info_label.text = f"Error playing Music 2: {e}"

    def download_music0(self, instance):
        if self.music_url_0:
            try:
                r = requests.get(self.music_url_0)
                r.raise_for_status()
                file_path = "downloaded_output_0.mp3"
                with open(file_path, "wb") as f:
                    f.write(r.content)
                self.info_label.text = f"Music 1 downloaded to {file_path}"
            except Exception as e:
                self.info_label.text = f"Error downloading Music 1: {e}"

    def download_music1(self, instance):
        if self.music_url_1:
            try:
                r = requests.get(self.music_url_1)
                r.raise_for_status()
                file_path = "downloaded_output_1.mp3"
                with open(file_path, "wb") as f:
                    f.write(r.content)
                self.info_label.text = f"Music 2 downloaded to {file_path}"
            except Exception as e:
                self.info_label.text = f"Error downloading Music 2: {e}"

    def go_back(self, instance):
        self.manager.current = "Upload"