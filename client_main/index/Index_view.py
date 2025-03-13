from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

name = "Index"

class View(Screen):
    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
        self.name = name

        self.add_widget(Button(text=name))