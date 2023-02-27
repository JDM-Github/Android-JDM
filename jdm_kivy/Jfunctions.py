import json
from .Jwidget import JDMWidget, JDMLabel
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, Color

def JDM_getColor(string: str) -> str:
    with open("jsons/all_color.json", 'r') as f:
        main : dict = json.load(f)
        color : str = main.get(string.title())
    return color if color else "#ffffff"

def JDM_addTitle(widget: JDMWidget, text: str, height: float,
             background_color: str, foreground_color: str, font_size: int or str):
    widget._main_title = JDMLabel(text=text, font_size=font_size, color=GetColor(foreground_color),
                                  size=(widget.width, height), pos=(widget.x, widget.top-height))
    with widget.canvas:
        widget._main_title_color = Color(rgba=GetColor(background_color))
        widget._main_title_rect = Rectangle(size=(widget.width, height), pos=(widget.y, widget.top-height))
    widget.add_widget(widget._main_title)
