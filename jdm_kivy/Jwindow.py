import json
from plyer import orientation
from kivy.core.window import Window
from kivy.app import App, platform
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, TransitionBase, SlideTransition

from .Jwidget import JDMWidget, JDMScreen

class JDMRootManager(ScreenManager):
    
    is_mouse_down = BooleanProperty(False)
    is_mouse_moving = BooleanProperty(False)

    mouse_button = StringProperty('')
    mouse_x = NumericProperty(0)
    mouse_y = NumericProperty(0)
    mouse_pos = ReferenceListProperty(mouse_x, mouse_y)
    
    prev_screen = StringProperty(None)
    prev_screen_widget = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = self
        self.size = Window.size
        self.elapseTime = None
        self.current_screen : JDMScreen
        self.__private_variable()
        with open(f"jsons/config.json") as f: self.__config = json.load(f)
        if self.__config.get("root_clock"): self._main_Clock = Clock.schedule_interval(self.update, 1/60)
        Window.bind(on_keyboard=self.hook_keyboard)

    def keyboard_down(self, window, scancode=None, key=None, keyAscii=None, *args):
        self.current_screen.keyboard_down(window, scancode, key, keyAscii, *args)

    def keyboard_up(self, window, scancode=None, key=None, keyAscii=None, *args):
        self.current_screen.keyboard_up(window, scancode, key, keyAscii, *args)

    def mouse_down(self, window, x, y, button, modifiers):
        self.is_mouse_down  = True
        self.current_screen.mouse_down(window, x, y, button, modifiers)

    def mouse_move(self, window, x, y, button):
        self.is_mouse_moving = True
        self.current_screen.mouse_move(window, x, y, button)

    def mouse_up(self, window, x, y, button, modifiers):
        self.is_mouse_down = False
        self.is_mouse_moving = False
        self.current_screen.mouse_up(window, x, y, button, modifiers)

    def _mouse_pos(self, window, pos):
        self.mouse_x, self.mouse_y = pos

    def hook_keyboard(self, _, key, *__):
        code = Window._keyboards.get("system").keycode_to_string(key)
        if code == 'escape':
            return self.current_screen.handleBackButton()
        return True

    def update(self, dt: float):
        self.elapseTime = dt

        if self.__config.get("display_fps"):
            if App.get_running_app(): App.get_running_app().title = (
                App.get_running_app()._main_title + f" -> FPS: {(1 / self.elapseTime):.2f}")
    
    def __private_variable(self):
        self.__adding_screen = False

    def add_widget(self, widget, *args, **kwargs):
        if self.__adding_screen: return super().add_widget(widget, *args, **kwargs)

    def change_screen(self, name: str, transition: TransitionBase = SlideTransition(direction='left')):
        if name not in self._get_screen_names(): self.add_screen(name)
        self.prev_screen = self.current
        self.prev_screen_widget = self.current_screen
        self.transition = transition
        self.current = name

    def add_screen(self, screen_name: str, screen: JDMScreen = None, widget: JDMWidget = None):
        if not screen: screen = JDMScreen(name=screen_name)
        if not widget: widget = JDMWidget()
        if not hasattr(self, screen_name):
            self.__adding_screen = True
            setattr(self, screen_name, screen)
            screen = getattr(self, screen_name)
            if not screen.name: screen.name = screen_name
            setattr(screen, screen_name, widget)
            screen.add_widget(getattr(screen, screen_name))
            self.add_widget(screen)
            self.__adding_screen = False
