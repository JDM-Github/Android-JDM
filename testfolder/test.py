from kivy.uix.label import Label
from kivy.app import App
from kivy.core.text import LabelBase

LabelBase.register(
    name="consolas",
    fn_regular="assets/font/consolas/consolas_regular.ttf",
    fn_bold="assets/font/consolas/consolas_bold.ttf",
    fn_italic="assets/font/consolas/consolas_italic.ttf",
    fn_bolditalic="assets/font/consolas/consolas_italic_bold.ttf")

class NewLabel(Label):
    
    def __init__(self, **kwargs):
        self.font_name = "consolas"
        super().__init__(**kwargs)
        self.text = "Hello World Test"