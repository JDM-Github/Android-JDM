def _register_all_label():
    from kivy.core.text import LabelBase
    LabelBase.register(
        name="consolas",
        fn_regular="assets/font/consolas/consolas_regular.ttf",
        fn_bold="assets/font/consolas/consolas_bold.ttf",
        fn_italic="assets/font/consolas/consolas_italic.ttf",
        fn_bolditalic="assets/font/consolas/consolas_italic_bold.ttf")

from jdm_kivy import *
from kivy.app import App
from plyer import orientation

class JDMApp(App):

    def __init__(self, title: str = None, size: list = (500, 500), manager: JDMRootManager=None, **kwargs):
        super().__init__(**kwargs)
        _register_all_label()
        if not platform == 'android':
            Window.size = size
            Window.left = 1
            Window.top = 30
        else: orientation.set_portrait()
        self.root: JDMRootManager = manager if manager else JDMRootManager()
        self.title = title if title else __class__.__name__.removesuffix('App')
        self._main_title = self.title

    def on_start(self):
        if platform != 'android':
            Window.bind(on_key_down=self.root.keyboard_down)
            Window.bind(on_key_up=self.root.keyboard_up)
            Window.bind(on_mouse_down=self.root.mouse_down)
            Window.bind(on_mouse_move=self.root.mouse_move)
            Window.bind(on_mouse_up=self.root.mouse_up)
            Window.bind(mouse_pos=self.root._mouse_pos)
        return super().on_start()

    def run(self, screen_name: str = "main", screen: JDMScreen = None, widget: JDMWidget = None):
        self.__first_screen = screen
        self.__first_screen_name = screen_name
        self.__first_widget = widget
        return super().run()

    def build(self):
        self.root.add_screen(
            self.__first_screen_name,
            self.__first_screen,
            self.__first_widget)
        return self.root
