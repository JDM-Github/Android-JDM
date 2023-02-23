from kivy import platform
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.graphics import Line, Rectangle, RoundedRectangle, Color, Ellipse, Triangle
from kivy.utils import get_color_from_hex as GetColor, get_hex_from_color as GetHex, get_random_color as GetRandom
from kivy.metrics import sp, dp
from .Jwidget import JDMWidget
from .Jlabel import JDMLabel
from .Jimage import JDMImage
from .Jfunctions import JDM_addTitle, JDM_getColor
