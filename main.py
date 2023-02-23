from kivy.app import App, platform
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.label import Label

LabelBase.register(
    name="consolas",
    fn_regular="assets/font/consolas/consolas_regular.ttf",
    fn_bold="assets/font/consolas/consolas_bold.ttf",
    fn_italic="assets/font/consolas/consolas_italic.ttf",
    fn_bolditalic="assets/font/consolas/consolas_italic_bold.ttf")

class JDMLabel(Label):
    
    def __init__(self, **kwargs):
        self.font_name = "consolas"
        self.bind(size=self.setter('text_size'))
        self.valign = 'center'
        self.halign = 'center'
        super().__init__(**kwargs)

class JDMApp(App):

    def __init__(self, title: str = None, size: list = (500, 500), **kwargs):
        super().__init__(**kwargs)
        if not platform == 'android':
            Window.size = size
            Window.left = 1
            Window.top = 30
        self.title = title if title else __class__.__name__.removesuffix('App')
        self._main_title = self.title

    def build(self):
        self.root = JDMLabel(text="TEST")
        return self.root

if __name__ == "__main__":
    JDMApp("Calculator", (720*0.5, 1400*0.5)).run()
