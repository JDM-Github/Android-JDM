from jdm_kivy import *

class MainScreen(JDMScreen): ...
class MainField(JDMWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(JDMLabel(
            size=self.root.size, text='JDM-Android Template',
            bold=True, italic=True, font_size=dp(24)))
