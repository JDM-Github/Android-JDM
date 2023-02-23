from kivy.core.text import LabelBase

LabelBase.register(
    name="consolas",
    fn_regular="assets/font/consolas/consolas_regular.ttf",
    fn_bold="assets/font/consolas/consolas_bold.ttf",
    fn_italic="assets/font/consolas/consolas_italic.ttf",
    fn_bolditalic="assets/font/consolas/consolas_italic_bold.ttf")

from src import MainField, MainScreen, JDMApp

if __name__ == "__main__":
    JDMApp("Calculator", (720*0.5, 1400*0.5)).run(screen_name="main", screen=MainScreen(), widget=MainField())

