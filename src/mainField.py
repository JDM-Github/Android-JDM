from __future__ import print_function
from jdm_kivy import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class CustomButton(JDMWidget):

    def __init__(self, name, color='ffffff', func_bind = lambda: None, fz=dp(24), **kwargs):
        super().__init__(**kwargs)
        self.func_binder = func_bind
        with self.canvas:
            Color(rgb=GetColor(JDM_getColor('JDM')), a=0.4)
            self._bg_line = Line(width=dp(2))
            self._main_Color = Color(rgba=GetColor('111111'))
            self._main_Rect = RoundedRectangle(radius=[10, 10, 10, 10])
        self._main_Label = JDMLabel(
            text=name, color=GetColor(color),
            font_size=fz, bold=True
        )
        self.add_widget(self._main_Label)
        self.bind(pos=self.change, size=self.change)
    
    def on_touch_down(self, touch):
        if (self._main_Rect.pos[0] <= touch.x <= (self._main_Rect.pos[0]+self._main_Rect.size[0]) and
            self._main_Rect.pos[1] <= touch.y <= (self._main_Rect.pos[1]+self._main_Rect.size[1])):
            self._main_Color.rgb = GetColor("333333")
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self._main_Color.rgb = GetColor('111111')
        return super().on_touch_up(touch)


    def change(self, *_):
        self._main_Label.size = self.size
        self._main_Label.pos = self.pos
        self._bg_line.rounded_rectangle = [*self.pos, *self.size, 10, 10, 10, 10]
        self._main_Rect.size = (self.width-dp(2), self.height-dp(2))
        self._main_Rect.pos = (
            (self.x+self.width/2)-self._main_Rect.size[0]/2,
            (self.y+self.height/2)-self._main_Rect.size[1]/2,
        )

class CustomTextInput(JDMWidget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (Window.width*0.9, Window.height*0.2)
        self.pos = (Window.width*0.05, Window.height*0.7-dp(10))
        with self.canvas:
            Color(rgb=GetColor(JDM_getColor('JDM')), a=0.4)
            Line(rounded_rectangle=[*self.pos, *self.size, 10, 10, 10, 10], width=dp(2))

class MainField(JDMWidget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = self.root.size
        JDM_addTitle(self, 'JDM Calculator', Window.height*0.05, JDM_getColor('JDM'), JDM_getColor('white'), dp(24))
        self.display_all_Modes()
        self.display_mode1_all_buttons()
        self.add_widget(CustomTextInput())

    def display_all_Modes(self):
        self.all_modes = GridLayout(
            size_hint_x=None, rows=1, spacing=dp(8), padding=dp(8),
        )
        self.all_modes.bind(minimum_width=self.all_modes.setter('width'))
        self.mode_scroll = ScrollView(
            size=(Window.width, Window.height*0.05),
            pos=(0, Window.height*0.9))
        self.all_modes.add_widget(CustomButton('Simple', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.all_modes.add_widget(CustomButton('Scientific', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.all_modes.add_widget(CustomButton('test', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.all_modes.add_widget(CustomButton('test', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.mode_scroll.add_widget(self.all_modes)
        self.add_widget(self.mode_scroll)
    
    def display_mode1_all_buttons(self):
        self.grid = GridLayout(
            cols=4, rows=6, spacing=dp(8), padding=dp(8),
            size=(Window.width, Window.height*0.6),
        )
        self.grid.add_widget(CustomButton('MC', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('M+', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('M-', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('MR', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('AC', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('<-', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('+/-', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('/', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('7'))
        self.grid.add_widget(CustomButton('8'))
        self.grid.add_widget(CustomButton('9'))
        self.grid.add_widget(CustomButton('x', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('4'))
        self.grid.add_widget(CustomButton('5'))
        self.grid.add_widget(CustomButton('6'))
        self.grid.add_widget(CustomButton('-', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('1'))
        self.grid.add_widget(CustomButton('2'))
        self.grid.add_widget(CustomButton('3'))
        self.grid.add_widget(CustomButton('+', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('%'))
        self.grid.add_widget(CustomButton('0'))
        self.grid.add_widget(CustomButton('.'))
        self.grid.add_widget(CustomButton('=', JDM_getColor('JDM')))
        self.add_widget(self.grid)
        