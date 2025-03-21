from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import requests

name = "Upload"

class UploadView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.prompt_input = TextInput(hint_text="Enter prompt", size_hint=(1, 0.2), font_name="Roboto")
        layout.add_widget(self.prompt_input)
        self.title_input = TextInput(hint_text="Enter title", size_hint=(1, 0.2), font_name="Roboto")
        layout.add_widget(self.title_input)
        self.style_input = TextInput(hint_text="Enter style", size_hint=(1, 0.2), font_name="Roboto")
        layout.add_widget(self.style_input)
        self.upload_btn = Button(text="Generate Music", size_hint=(1, 0.2), font_name="Roboto")
        self.upload_btn.bind(on_press=self.upload_text)
        layout.add_widget(self.upload_btn)
        self.add_widget(layout)

    def upload_text(self, instance):
        prompt = self.prompt_input.text
        title = self.title_input.text
        style = self.style_input.text
        url = "http://127.0.0.1:5000/upload_text"
        try:
            response = requests.post(url, data={"prompt": prompt, "title": title, "style": style})
            result = response.json()
            print("Response:", result)
            if result.get("status") == "success":
                music_url_0 = result.get("music_url_0")
                print("Music 0:", music_url_0)
                music_url_1 = result.get("music_url_1")
                print("Music 1:", music_url_1)
                result_screen = self.manager.get_screen("Result")
                result_screen.update_results(music_url_0, music_url_1)
                self.manager.current = "Result"
            else:
                print("Error:", result.get("message"))
        except Exception as e:
            print("Upload failed:", e)