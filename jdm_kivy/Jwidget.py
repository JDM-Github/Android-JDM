from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

class JDMScreen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.root = App.get_running_app().root
        self.size = self.root.size

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
