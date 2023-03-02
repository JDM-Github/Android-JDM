from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.effects.scroll import ScrollEffect
from kivy.effects.dampedscroll import DampedScrollEffect


from kivy.metrics import dp
from kivy.graphics import RoundedRectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty

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

    remove_overlapped = BooleanProperty(False)
    remove_scroll = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            remove_overlapped=self.__change_effect,
            remove_scroll=self.__change_effect,
        )
        self.__original_bar_color = self.bar_color
        if 'remove_overlapped' in kwargs: self.remove_overlapped = kwargs.get('remove_overlapped')
        if 'remove_scroll' in kwargs: self.remove_scroll = kwargs.get('remove_scroll')
        self.__change_effect()
        self.root = App.get_running_app().root

    def __change_effect(self, *_):
        self.effect_cls = ScrollEffect if self.remove_overlapped else DampedScrollEffect
        self.bar_color = '00000000' if self.remove_scroll else self.__original_bar_color

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

    def on_ref_press(self, ref):
        if ref: getattr(self, ref)()
        return super().on_ref_press(ref)

class JDMImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = App.get_running_app().root

class JDMCardBox(JDMWidget):

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

        self._card_shadow.radius = self.radius
        self._card_line.radius = self.radius
        self._card_rect.radius = self.radius

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

class JDMCode(JDMWidget):
    
    code_color = ListProperty([0.1, 0.1, 0.1, 1])
    font_size = NumericProperty(dp(14))
    radius = ListProperty([10, 10, 10, 10])
    text = StringProperty('')
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'code_color' in kwargs: self.code_color = kwargs.get('code_color')
        if 'font_size' in kwargs: self.font_size = kwargs.get('font_size')
        if 'radius' in kwargs: self.radius = kwargs.get('radius')
        if 'text' in kwargs: self.text = kwargs.get('text')
        if 'color' in kwargs: self.color = kwargs.get('color')

        self.max_width = 0
        self._display_code()
        self.bind(
            size=self._change,
            pos=self._change,
            font_size=self._refresh_text,
            color=self._refresh_text,
        )
        self.bind(text=self._refresh_text)

    def _refresh_text(self, *_):
        index = 0
        number = 1
        self._all_line.clear()
        self._all_line.append(f'{number: 3d}| ')
        for s in self.text:
            if s == '\n':
                index += 1
                number += 1
                self._all_line.append(f'{number: 3d}| ')
            else: self._all_line[index] += s

        self.max_width = len(self._all_line[0])*(self.font_size*0.65)
        self._main_grid.clear_widgets()
        for line in self._all_line:
            if self.max_width < len(line)*(self.font_size*0.65):
                self.max_width = len(line)*(self.font_size*0.65)
            self._main_grid.add_widget(JDMLabel(color=self.color,
                halign='left', text=line, size_hint_y=None, height=self.font_size, font_size=self.font_size))

        self._main_grid.width = max(self.max_width, self._main_scroll.width)

    def _display_code(self):
        self._all_line : list[str] = list()
        with self.canvas:
            self._main_col = Color(rgba=self.code_color)
            self._main_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=self.radius)
        self._main_grid = JDMGridLayout(size_hint_y=None, size_hint_x=None, cols=1, padding=dp(5))
        self._main_grid.bind(minimum_height=self._main_grid.setter('height'))
        self._main_scroll = JDMScrollView(remove_overlapped=True, remove_scroll=True, pos=self.pos)
        self._main_scroll.always_overscroll = False
        self._main_scroll.bind(width=lambda *_: setattr(self._main_grid, 'width', max(self.max_width, self._main_scroll.width)))
        self._main_scroll.size = self.size
        
        self._refresh_text()
        self._main_scroll.add_widget(self._main_grid)
        self.add_widget(self._main_scroll)

        self.bind(code_color=lambda *_: setattr(self._main_col, 'rgba', self.code_color))
        self.bind(radius=lambda *_: setattr(self._main_rect, 'radius', self.radius))
    
    def _change(self, *_):
        self._main_rect.radius = self.radius
        self._main_rect.size = self.size
        self._main_rect.pos = self.pos
        self._main_scroll.size = self.size
        self._main_scroll.pos = self.pos