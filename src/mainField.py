from __future__ import print_function
import math
from jdm_kivy import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard

class MainScreen(JDMScreen): ...
class CustomButton(JDMWidget):

    def __init__(self, name, color='ffffff', func_bind = lambda: None, fz=dp(24), **kwargs):
        super().__init__(**kwargs)
        self.func_binder = func_bind
        self.clicked = False
        with self.canvas:
            Color(rgb=GetColor(JDM_getColor('JDM')), a=0.4)
            self._bg_line = Line(width=dp(2))
            self._main_Color = Color(rgba=GetColor('111111'))
            self._main_Rect = RoundedRectangle(radius=[10, 10, 10, 10])
        self._main_Label = JDMLabel(markup=True,
            text=name, color=GetColor(color),
            font_size=fz, bold=True
        )
        self.add_widget(self._main_Label)
        self.bind(pos=self.change, size=self.change)
    
    def on_touch_down(self, touch):
        if (self._main_Rect.pos[0] <= touch.x <= (self._main_Rect.pos[0]+self._main_Rect.size[0]) and
            self._main_Rect.pos[1] <= touch.y <= (self._main_Rect.pos[1]+self._main_Rect.size[1])):
            self.clicked = True
            self._main_Color.rgb = GetColor("333333")
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.clicked:
            self._main_Color.rgb = GetColor('111111')
            self.clicked = False
            self.func_binder()
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
    
    def __init__(self, result_box=False, **kwargs):
        super().__init__(**kwargs)
        self.result_box = result_box
        self.size = (Window.width*0.9, Window.height*0.25)
        self.pos = (Window.width*0.05, Window.height*0.65-dp(10))
        with self.canvas:
            Color(rgb=GetColor(JDM_getColor('JDM')), a=0.4)
            Line(rounded_rectangle=[*self.pos, *self.size, 10, 10, 10, 10], width=dp(2))
        
        self.scroll = ScrollView(size=(self.width-dp(20), self.height/2-dp(20)), bar_color = GetColor('00000000'), 
                                 pos=(self.x+dp(10), self.y+(self.height/2 if self.result_box is False else 0)+dp(10)), bar_inactive_color = GetColor('00000000'))
        self.main_label = JDMLabel(halign='right', text='', font_size=dp(30), size_hint_x=None,
            width=self.width-dp(20), bold=True, italic=True)
        self.main_label.bind(text=lambda *_: setattr(self.main_label, 'width', max(len(self.main_label.text)*dp(18), self.width-dp(20))))
        self.scroll.add_widget(self.main_label)
        self.add_widget(self.scroll)

class MainField(JDMWidget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        JDM_addTitle(self, 'JDM Calculator', Window.height*0.05, JDM_getColor('JDM'), JDM_getColor('white'), dp(24))
        self.all_variables()
        self.display_all_Modes()
        self.display_utilities()
        self.display_mode1_all_buttons()
        self.main_textinput = CustomTextInput()
        self.result_textinput = CustomTextInput(True)
        self.add_widget(self.main_textinput)
        self.add_widget(self.result_textinput)

    def display_all_Modes(self):
        self.all_modes = GridLayout(size_hint_x=None, rows=1, spacing=dp(8), padding=dp(8))
        self.all_modes.bind(minimum_width=self.all_modes.setter('width'))
        self.mode_scroll = ScrollView(
            size=(Window.width-dp(10), Window.height*0.05),
            pos=(dp(5), Window.height*0.9))
        self.mode_scroll.bar_color = GetColor('00000000')
        self.mode_scroll.bar_inactive_color = GetColor('00000000')
        self.all_modes.add_widget(CustomButton('Simple', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.mode_scroll.add_widget(self.all_modes)
        self.add_widget(self.mode_scroll)

    def display_utilities(self):
        self.all_util = GridLayout(size_hint_x=None, rows=1, spacing=dp(8), padding=dp(8))
        self.all_util.bind(minimum_width=self.all_util.setter('width'))
        self.util_scroll = ScrollView(
            size=(Window.width-dp(10), Window.height*0.05),
            pos=(dp(5), Window.height*0.55+dp(20)))
        self.util_scroll.bar_color = GetColor('00000000')
        self.util_scroll.bar_inactive_color = GetColor('00000000')
        self.all_util.add_widget(CustomButton('Sound', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.all_util.add_widget(CustomButton('History', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.all_util.add_widget(CustomButton('Copy', fz=dp(10), size_hint_x=None, width=Window.width/5, func_bind=self.copy_text))
        self.all_util.add_widget(CustomButton('Cut', fz=dp(10), size_hint_x=None, width=Window.width/5, func_bind=self.cut_text))
        self.all_util.add_widget(CustomButton('Paste', fz=dp(10), size_hint_x=None, width=Window.width/5, func_bind=self.paste_text))
        self.util_scroll.add_widget(self.all_util)
        self.add_widget(self.util_scroll)

    def display_mode1_all_buttons(self):
        self.grid = GridLayout(
            cols=4, rows=7, spacing=dp(8), padding=dp(8),
            size=(Window.width, Window.height*0.55),
        )
        self.grid.add_widget(CustomButton('(', JDM_getColor('JDM'), func_bind=lambda : self.add_text('(')))
        self.grid.add_widget(CustomButton(')', JDM_getColor('JDM'), func_bind=lambda : self.add_text(')')))
        self.grid.add_widget(CustomButton('^', JDM_getColor('JDM'), func_bind=lambda : self.add_text('^')))
        self.grid.add_widget(CustomButton('√', JDM_getColor('JDM'), func_bind=lambda : self.add_text('√')))
        self.grid.add_widget(CustomButton('MC', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('M+', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('M-', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('MR', JDM_getColor('JDM')))
        self.grid.add_widget(CustomButton('AC', JDM_getColor('JDM'), func_bind=self.clear_text))
        self.grid.add_widget(CustomButton('<-', JDM_getColor('JDM'), func_bind=self.del_text))
        self.grid.add_widget(CustomButton('±', JDM_getColor('JDM'), func_bind=self.change_sign))
        self.grid.add_widget(CustomButton('÷', JDM_getColor('JDM'), func_bind=lambda : self.add_text('÷')))
        self.grid.add_widget(CustomButton('7', func_bind=lambda : self.add_text('7')))
        self.grid.add_widget(CustomButton('8', func_bind=lambda : self.add_text('8')))
        self.grid.add_widget(CustomButton('9', func_bind=lambda : self.add_text('9')))
        self.grid.add_widget(CustomButton('x', JDM_getColor('JDM'), func_bind=lambda : self.add_text('x')))
        self.grid.add_widget(CustomButton('4', func_bind=lambda : self.add_text('4')))
        self.grid.add_widget(CustomButton('5', func_bind=lambda : self.add_text('5')))
        self.grid.add_widget(CustomButton('6', func_bind=lambda : self.add_text('6')))
        self.grid.add_widget(CustomButton('-', JDM_getColor('JDM'), func_bind=lambda : self.add_text('-')))
        self.grid.add_widget(CustomButton('1', func_bind=lambda : self.add_text('1')))
        self.grid.add_widget(CustomButton('2', func_bind=lambda : self.add_text('2')))
        self.grid.add_widget(CustomButton('3', func_bind=lambda : self.add_text('3')))
        self.grid.add_widget(CustomButton('+', JDM_getColor('JDM'), func_bind=lambda : self.add_text('+')))
        self.grid.add_widget(CustomButton('%', func_bind=lambda : self.add_text('%')))
        self.grid.add_widget(CustomButton('0', func_bind=lambda : self.add_text('0')))
        self.grid.add_widget(CustomButton('.', func_bind=lambda : self.add_text('.')))
        self.grid.add_widget(CustomButton('=', JDM_getColor('JDM'), func_bind=lambda : self.evaluate(self.main_textinput.main_label.text)))
        self.add_widget(self.grid)

    def add_text(self, text, auto_eval=True):
        if text in self.all_operations:
            if text == '-' and (not self.current_text[self.all_index] or self.current_text[self.all_index][-1] in '()'):
                self.current_text[self.all_index] += text
            elif self.current_text[self.all_index] and self.current_text[self.all_index][-1] in self.all_operations:
                if text == '-' and self.current_text[self.all_index][-1] != '-':
                    self.current_text[self.all_index] = self.current_text[self.all_index][:-1]
                    self.current_text[self.all_index] += text
                else:
                    self.current_text[self.all_index] = str()
                    self.all_index -= 1
                    self.current_text[self.all_index] = self.current_text[self.all_index][:-1]
                    self.current_text[self.all_index] += text
                    self.all_index += 1
            elif not self.current_text[self.all_index]:
                self.current_text[self.all_index] = str()
                self.all_index -= 1
                self.current_text[self.all_index] = self.current_text[self.all_index][:-1]
                self.current_text[self.all_index] += text
                self.all_index += 1
            else:
                self.all_index += 2
                self.current_text.append(text)
                self.current_text.append(str())
        else:
            if text in ')':
                if (self.current_text[self.all_index]
                    and not self.current_text[self.all_index][-1] in self.all_operations
                    and not self.current_text[self.all_index][-1] == '('):
                    if self.main_textinput.main_label.text.count('(') > self.main_textinput.main_label.text.count(')'):
                        self.current_text[self.all_index] += text
            elif text == '.':
                if self.current_text[self.all_index].find('.') == -1:
                    self.current_text[self.all_index] += text
            elif text in self.all_functions:
                if not (self.string_have(self.current_text[self.all_index], '1234567890x÷+-^'+self.all_functions)):
                    self.current_text[self.all_index] += text
            else: self.current_text[self.all_index] += text

        self.main_textinput.main_label.text = ''.join(self.current_text)
        self.main_textinput.scroll.scroll_x = 1
        if auto_eval: self.evaluate(self.main_textinput.main_label.text, True)
    
    def string_have(self, new_text: str, string: str):
        for text in new_text:
            if text in string: return True
        return False        

    def del_text(self):
        if self.current_text[self.all_index]:
            self.current_text[self.all_index] = self.current_text[self.all_index][:-1]
        else:
            if self.all_index > 0:
                self.current_text = self.current_text[:-2]
                self.all_index -= 2

        self.main_textinput.main_label.text = ''.join(self.current_text)
        self.main_textinput.scroll.scroll_x = 1
        self.evaluate(self.main_textinput.main_label.text, True)

    def clear_text(self):
        self.main_textinput.main_label.text = ''
        self.main_textinput.scroll.scroll_x = 1
        self.all_index = 0
        self.current_text : list[str] = [str()]
        self.evaluate(self.main_textinput.main_label.text, True)

    def change_sign_function(self, string: str):
        already = False
        end_it = False
        num_str = str()
        new_str = str() 
        for text in reversed(string):
            if end_it: pass
            elif already is False:
                if text.isdigit():
                    already = True
                    num_str = text + num_str
            else:
                if text in self.all_operations + '()' + self.all_functions:
                    end_it = True
                    if text == '-': num_str = text + num_str
                    if float(num_str) >= 0:
                        new_str = '-' + new_str
                    else: continue
                else: num_str = text + num_str
            new_str = text + new_str
        if end_it is False and already:
            if float(num_str) >= 0:
                new_str = '-' + new_str
            else: new_str = new_str[1:]
        return new_str

    def change_sign(self):
        if self.current_text[self.all_index]:
            self.current_text[self.all_index] = self.change_sign_function(self.current_text[self.all_index])
            self.main_textinput.main_label.text = ''.join(self.current_text)
            self.main_textinput.scroll.scroll_x = 1
            self.evaluate(self.main_textinput.main_label.text, True)
    
    def copy_text(self):
        if self.main_textinput.main_label.text:
            Clipboard.copy(self.main_textinput.main_label.text)
        else: Clipboard.copy('0')

    def cut_text(self):
        self.copy_text()
        self.clear_text()

    def paste_text(self):
        old_text = self.main_textinput.main_label.text
        self.clear_text()
        if Clipboard.paste():
            new_text = self.clean_text(Clipboard.paste())
            for text in old_text+new_text:
                self.add_text(text, False)
        print(self.current_text)
        self.evaluate(self.main_textinput.main_label.text, True)

    def all_variables(self):
        self.all_operations = 'x÷+-^'
        self.all_functions = '√'
        self.real_string = str()
        self.all_index = 0
        self.current_text : list[str] = [str()]
        self.already_have_dot = str()

    def add_str(self, str1: str, str2: str) -> str:
        try: return str(float(str1) + float(str2))
        except: return "ERROR"
    def min_str(self, str1: str, str2: str) -> str:
        try: return str(float(str1) - float(str2))
        except: return "ERROR"
    def mul_str(self, str1: str, str2: str) -> str:
        try: return str(float(str1) * float(str2))
        except: return "ERROR"
    def div_str(self, str1: str, str2: str) -> str:
        try: return str(float(str1) / float(str2))
        except: return "ERROR"
    def pow_str(self, str1: str, str2: str) -> str:
        try: return str(pow(float(str1), float(str2)))
        except: return "ERROR"
    def sqrt_str(self, str1: str) -> str:
        try: return str(math.sqrt(float(str1)))
        except: return "ERROR"

    def calculate(self, str1: str, str2: str, operation: str) -> str:
        if operation == '+': return self.add_str(str1, str2)
        if operation == '-': return self.min_str(str1, str2)
        if operation == 'x': return self.mul_str(str1, str2)
        if operation == '÷': return self.div_str(str1, str2)
        if operation == '^': return self.pow_str(str1, str2)
    
    def calculate2(self, str1: str, operation: str) -> str:
        if operation == '√': return self.sqrt_str(str1)
    
    def find_and_calculate(self, new_text: str, operation: str) -> str:
        while True:
            first = str()
            second = str()
            first_number = str()
            second_number = str()
            operation_index = None
            if operation_index is None:
                for index, text in enumerate(new_text):
                    if text in operation:
                        if text == '-' and (new_text[index-1] in self.all_operations or index == 0): continue
                        operation_index = index
                        break
            if operation_index is None: break
            already = False
            for text_index in reversed(new_text[:operation_index]):
                if text_index in self.all_operations or already:
                    if already is False and text_index == '-':
                        first_number = text_index + first_number
                        already = True
                        continue
                    already = True
                    first = text_index + first
                elif text_index.isdigit() or text_index == '.': first_number = text_index + first_number
            already = False
            for text_index in new_text[operation_index+1:]:
                if text_index in self.all_operations or already:
                    if not second_number and text_index == '-' and already is False:
                        second_number += text_index
                        continue
                    already = True
                    second += text_index
                elif text_index.isdigit() or text_index == '.': second_number += text_index
            evaluation = self.calculate(first_number, second_number, new_text[operation_index])
            if evaluation == 'ERROR': return 'ERROR'
            new_text = self.clean_text(first + evaluation + second)
        return new_text

    def separate_evaluation(self, new_text: str) -> str:
        while True:
            index_1 = None
            index_2 = None
            for index, text in enumerate(new_text):
                if text == '(': index_1 =  index
                elif text == ')' and index_2 is None:
                    index_2 = index
                    break
            if index_1 is not None and index_2 is not None:
                first = new_text[:index_1]
                if first and first[-1].isdigit(): first += 'x'
                last = new_text[index_2+1:]
                if last and last[0].isdigit(): last = 'x' + last
                new_text = first + self.evaluate(new_text[index_1+1:index_2], True) + last
            elif index_1 is not None:
                first = new_text[:index_1]
                if first and first[-1].isdigit(): first += 'x'
                new_text = first + new_text[index_1+1:]
                break
            elif index_2 is not None:
                first = new_text[index_2+1:]
                if first and first[0].isdigit(): first = 'x(' + first
                new_text = '(' + first + new_text[:index_2]
                break
            else: break
        return new_text

    def function_calculate(self, new_text: str, func_sign: str):
        while True:
            first = str()
            first_number = str()
            function_index = None
            if function_index is None:
                for index, text in enumerate(new_text):
                    if text in func_sign:
                        if text == '-' and (new_text[index-1] in self.all_operations or index == 0): continue
                        function_index = index
                        break
            if function_index is None: break
            already = False
            for text_index in new_text[function_index+1:]:
                if text_index in self.all_operations or already:
                    if not first_number and text_index == '-' and already is False:
                        first_number += text_index
                        continue
                    already = True
                    first += text_index
                elif text_index.isdigit() or text_index == '.': first_number += text_index
            evaluation = self.calculate2(first_number, new_text[function_index])
            if evaluation == 'ERROR': return 'ERROR'
            new_text = self.clean_text(new_text[:function_index] + evaluation + first)
        return new_text

    def clean_text(self, string: str): return ''.join([text for text in string if text in '1234567890().'+self.all_functions+self.all_operations])
    def set_scroll_box(self):
        self.main_textinput.scroll.scroll_x = 1
        self.result_textinput.scroll.scroll_x = 1

    def equal_set_all_tracker(self):
        self.all_index = 0
        self.current_text = [self.main_textinput.main_label.text]

    def error_manager(self, result, result_box):
        self.result_textinput.main_label.text = result
        if result_box is False:
            self.main_textinput.main_label.text = result if result != 'ERROR' else '0'
            self.equal_set_all_tracker()
        self.set_scroll_box()

    def evaluate(self, string: str, result_box = False):
        new_text = self.clean_text(string)
        new_text = self.separate_evaluation(new_text)

        new_text = self.find_and_calculate(new_text, '^')
        if new_text == 'ERROR':
            self.error_manager(new_text, result_box)
            return 'ERROR'
        new_text = self.function_calculate(new_text, '√')
        if new_text == 'ERROR':
            self.error_manager(new_text, result_box)
            return 'ERROR'
        new_text = self.find_and_calculate(new_text, 'x÷')
        if new_text == 'ERROR':
            self.error_manager(new_text, result_box)
            return 'ERROR'
        new_text = self.find_and_calculate(new_text, '+-')
        if new_text == 'ERROR':
            self.error_manager(new_text, result_box)
            return 'ERROR'

        if string == self.main_textinput.main_label.text:
            try: result = (new_text if not new_text or (len(new_text)==1 and new_text == '-')
                      else (str(int(float(new_text))) if int(float(new_text)) == float(new_text) else new_text))
            except: result = 'ERROR'
            self.error_manager(result, result_box)
        return new_text
