from kivy.config import Config
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "773")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.text import LabelBase
from index import Index_view


route_view = {
    Index_view.name: Index_view.View()
            }

#print(route_view)

LabelBase.register(name="Roboto", fn_regular="font/msyh.ttc", fn_bold="font/msyhbd.ttc")

class Message_Client_App(App):
    def __init__(self):
        super().__init__()
        self.body = ScreenManager()
    def build(self):
        return self.body
    def on_start(self):
        for screen_name, screen_view in route_view.items():
            #print(screen_name, screen_view)
            self.body.add_widget(screen_view)
       #print(self.on_start)


Main = Message_Client_App()
Main.run()