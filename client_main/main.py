import os
from kivy.resources import resource_add_path
from kivy.clock import Clock
from kivy.config import Config

font_path = os.path.join(os.path.dirname(__file__), "font")
resource_add_path(font_path)
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "773")


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from index import Index_view, Upload_view, Result_view



LabelBase.register(name="Roboto",
    fn_regular=os.path.join(font_path, "msyh.ttc"),
    fn_bold=os.path.join(font_path, "msyhbd.ttc")
)

route_view = {
    Index_view.name: Index_view.View(),
    Upload_view.name: Upload_view.UploadView(),
    Result_view.name: Result_view.ResultView("", "")
}
()

class Message_Client_App(App):
    def __init__(self):
        super().__init__()
        self.body = ScreenManager()

    def build(self):
        return self.body

    def on_start(self):
        # 添加所有屏幕到 ScreenManager
        for screen_name, screen_view in route_view.items():
            self.body.add_widget(screen_view)
        # 默认显示 Upload_view 屏幕
        self.body.current = Upload_view.name  
        # 定时检测 Result_view 屏幕的状态，每2秒调用一次
        Clock.schedule_interval(self.check_result_status, 2)

    def check_result_status(self, dt):
        # 如果当前屏幕为 Result_view，则调用其 check_status 方法进行状态检测
        if self.body.current == Result_view.name:
            result_screen = self.body.get_screen(Result_view.name)
            result_screen.check_status()

Main = Message_Client_App()
Main.run()