from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

name = "Index"

class View(Screen):
    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
        self.name = name
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        
        btn_upload = Button(text="Go to Upload Screen", size_hint=(1, 0.2), font_name="Roboto")
        btn_upload.bind(on_press=self.go_to_upload)
        layout.add_widget(btn_upload)
        
        self.add_widget(layout)

    def go_to_upload(self, instance):
        self.manager.current = "Upload"