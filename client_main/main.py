import os
from kivy.resources import resource_add_path

# 添加字体所在的目录（请保证路径正确）
font_path = os.path.join(os.path.dirname(__file__), "font")
resource_add_path(font_path)

from kivy.config import Config
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "773")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.text import LabelBase
from index import Index_view
from index import Upload_view
from index import Result_view  

route_view = {
    Index_view.name: Index_view.View(),
    Upload_view.name: Upload_view.UploadView(),
    Result_view.name: Result_view.ResultView("", "")  # 启动时先用空数据初始化
}

# 使用绝对路径注册中文字体
LabelBase.register(name="Roboto",
    fn_regular=os.path.join(font_path, "msyh.ttc"),
    fn_bold=os.path.join(font_path, "msyhbd.ttc")
)

class Message_Client_App(App):
    def __init__(self):
        super().__init__()
        self.body = ScreenManager()
    def build(self):
        return self.body
    def on_start(self):
        for screen_name, screen_view in route_view.items():
            self.body.add_widget(screen_view)
        self.body.current = Upload_view.name  # 默认显示上传屏幕

Main = Message_Client_App()
Main.run()