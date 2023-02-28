from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

from kivy.metrics import dp
from kivy.graphics import RoundedRectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from kivy.properties import StringProperty, NumericProperty, ListProperty

class JDMScreen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.root = App.get_running_app().root
        self.size = self.root.size

    def update(self): ...
    def handleBackButton(self) -> bool: return True
    def keyboard_down(self, window, scancode=None, key=None, keyAscii=None, *args): ...
    def keyboard_up(self, window, scancode=None, key=None, keyAscii=None, *args): ...
    def mouse_down(self, window, x, y, button, modifiers): ...
    def mouse_move(self, window, x, y, button): ...
    def mouse_up(self, window, x, y, button, modifiers): ...

class JDMGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = App.get_running_app().root

class JDMBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = App.get_running_app().root

class JDMScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = App.get_running_app().root

class JDMTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = App.get_running_app().root

class JDMWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = App.get_running_app().root

class JDMLabel(Label):
    def __init__(self, **kwargs):
        self.font_name = "consolas"
        self.bind(size=self.setter('text_size'))
        self.valign = 'center'
        self.halign = 'center'
        super().__init__(**kwargs)
        self.root = App.get_running_app().root

class JDMImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = App.get_running_app().root

class CardBox(JDMWidget):

    __all_shadow_pos__ = ['n', 'l', 'r', 't', 'b', 'lt', 'lb', 'rt', 'rb']
    shadow_pos = StringProperty('n')
    shadow_width = NumericProperty(dp(2))
    shadow_opacity = NumericProperty(0.2)
    radius = ListProperty([10, 10, 10, 10])
    card_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'shadow_pos' in kwargs: self.shadow_pos = kwargs.get('shadow_pos')
        if 'shadow_width' in kwargs: self.shadow_width = kwargs.get('shadow_width')
        if 'shadow_opacity' in kwargs: self.shadow_opacity = kwargs.get('shadow_opacity')
        if 'radius' in kwargs: self.radius = kwargs.get('radius')
        if 'card_color' in kwargs: self.card_color = kwargs.get('card_color')

        self._display_card()
        self.bind(radius=self._change,
                  pos=self._change,
                  size=self._change,
                  shadow_pos=self._change,
                  shadow_width=self._change)
        self.bind(card_color=lambda *_: setattr(self._card_col, 'rgba', self.card_color))

    def _display_card(self):
        with self.canvas:
            Color(rgb=GetColor('000000'), a=self.shadow_opacity)
            self._card_shadow = RoundedRectangle(radius=self.radius)
            Color(rgb=GetColor('555555'), a=self.shadow_opacity)
            self._card_line = RoundedRectangle(radius=self.radius)
            self._card_col = Color(rgba=self.card_color)
            self._card_rect = RoundedRectangle(radius=self.radius)

    def _change(self, *_):
        if not self.shadow_pos in self.__all_shadow_pos__:
            raise KeyError(f"{self.shadow_pos} not in {self.__all_shadow_pos__}")

        self._card_rect.size = self.size
        self._card_rect.pos = self.pos
        
        self._card_shadow.size = self.size if self.shadow_pos != 'n' else (self.width+self.shadow_width, self.height+self.shadow_width)
        self._card_shadow.pos = (
            self.x + (self.shadow_width if 'r' in self.shadow_pos else (-self.shadow_width if 'l' in self.shadow_pos else
                (-self.shadow_width/2 if self.shadow_pos == 'n' else 0))),
            self.y + (self.shadow_width if 't' in self.shadow_pos else (-self.shadow_width if 'b' in self.shadow_pos else
                (-self.shadow_width/2 if self.shadow_pos == 'n' else 0))))
        self._card_line.size = self.size if self.shadow_pos != 'n' else (self.width+self.shadow_width/2, self.height+self.shadow_width/2)
        self._card_line.pos = (
            self.x + (self.shadow_width/2 if 'r' in self.shadow_pos else (-self.shadow_width/2 if 'l' in self.shadow_pos else
                (-self.shadow_width/4 if self.shadow_pos == 'n' else 0))),
            self.y + (self.shadow_width/2 if 't' in self.shadow_pos else (-self.shadow_width/2 if 'b' in self.shadow_pos else
                (-self.shadow_width/4 if self.shadow_pos == 'n' else 0))))