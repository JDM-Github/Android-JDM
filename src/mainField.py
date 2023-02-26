from __future__ import print_function
import math
import decimal
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
        JDM_addTitle(
            self,
            'JDM Calculator',
            Window.height * 0.05,
            JDM_getColor('JDM'),
            JDM_getColor('white'),
            dp(24)
        )
        self.all_variables()
        self.display_all_Modes()
        self.display_utilities()
        self.display_mode1_all_buttons()
        self.main_textinput = CustomTextInput()
        self.result_textinput = CustomTextInput(True)
        self.add_widget(self.main_textinput)
        self.add_widget(self.result_textinput)

    def display_all_Modes(self):
        """
        Creates a GridLayout with custom buttons for all calculator modes
        and adds it to the main widget.
        """
        self.all_modes = GridLayout(
            size_hint_x=None,
            rows=1,
            spacing=dp(8),
            padding=dp(8)
        )
        self.all_modes.bind(minimum_width=self.all_modes.setter('width'))
        self.mode_scroll = ScrollView(
            size=(Window.width - dp(10), Window.height * 0.05),
            pos=(dp(5), Window.height * 0.9),
            bar_color=GetColor('00000000'),
            bar_inactive_color=GetColor('00000000')
        )
        self.all_modes.add_widget(CustomButton('Simple', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.mode_scroll.add_widget(self.all_modes)
        self.add_widget(self.mode_scroll)

    def display_utilities(self) -> None:
        """
        Create and display the utility buttons (sound, history, copy, cut, and paste)
        on the calculator interface.
        """
        self.all_util = GridLayout(
            size_hint_x=None,
            rows=1,
            spacing=dp(8),
            padding=dp(8)
        )
        self.all_util.bind(minimum_width=self.all_util.setter('width'))
        self.util_scroll = ScrollView(
            size=(Window.width - dp(10), Window.height * 0.05),
            pos=(dp(5), Window.height *0.55 + dp(20)),
            bar_color = GetColor('00000000'),
            bar_inactive_color = GetColor('00000000')
        )
        self.all_util.add_widget(CustomButton('Sound', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.all_util.add_widget(CustomButton('History', fz=dp(10), size_hint_x=None, width=Window.width/5))
        self.all_util.add_widget(CustomButton('Copy', fz=dp(10), size_hint_x=None, width=Window.width/5, func_bind=self.copy_text))
        self.all_util.add_widget(CustomButton('Cut', fz=dp(10), size_hint_x=None, width=Window.width/5, func_bind=self.cut_text))
        self.all_util.add_widget(CustomButton('Paste', fz=dp(10), size_hint_x=None, width=Window.width/5, func_bind=self.paste_text))
        self.util_scroll.add_widget(self.all_util)
        self.add_widget(self.util_scroll)

    def display_mode1_all_buttons(self) -> None:
        """
        Displays all the buttons for calculator mode 1 in a GridLayout.
    
        The GridLayout is a 4x7 grid with 8 pixels of spacing and padding. The buttons are added to the grid in the 
        following order: (, ), ^, √, MC, M+, M-, MR, AC, <-, ±, ÷, 7, 8, 9, x, 4, 5, 6, -, 1, 2, 3, +, %, 0, ., =.
        Each button is represented by a CustomButton instance with a function binded to it that calls a specific 
        method of the calculator.
        """
        self.grid = GridLayout(
            cols=4,
            rows=7,
            spacing=dp(8),
            padding=dp(8),
            size=(Window.width, Window.height * 0.55),
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

    def add_text(self, text: str, auto_eval: bool = True) -> None:
        """
        Adds the given text to the calculator's main input field, updating its display and optionally evaluating the expression.

        Args:
            text (str): The text to add to the input field.
            auto_eval (bool): Whether to evaluate the expression after adding the text (default: True).

        Returns:
            None
        """
        # Check if the input text is a valid operation
        if text in self.all_operations:
            # Replace certain operations with symbols
            if text == '/': text = '÷'
            elif text == '*': text = 'x'

            # Handle special case for minus sign
            if text == '-' and (not self.current_text[self.all_index] or self.current_text[self.all_index][-1] in '()'):
                self.current_text[self.all_index] += text

            # Handle cases where input text follows another operation
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

            # Handle case where input text is first character
            elif not self.current_text[self.all_index] and self.current_text[self.all_index-1] != '%':
                self.current_text[self.all_index] = str()
                self.all_index -= 1
                self.current_text[self.all_index] = self.current_text[self.all_index][:-1]
                self.current_text[self.all_index] += text
                self.all_index += 1

            # Handle all other cases
            else:
                self.all_index += 2
                self.current_text.append(text)
                self.current_text.append(str())

        # Handle case where input text is not a valid operation
        else:
            # Handle closing parentheses
            if text in ')':
                if (self.current_text[self.all_index]
                    and not self.current_text[self.all_index][-1] in self.all_operations
                    and not self.current_text[self.all_index][-1] == '('):
                    if self.main_textinput.main_label.text.count('(') > self.main_textinput.main_label.text.count(')'):
                        self.current_text[self.all_index] += text

            # Handle decimal point
            elif text == '.':
                if self.current_text[self.all_index].find('.') == -1:
                    self.current_text[self.all_index] += text

            # Handle functions
            elif text in self.all_functions:
                if text == '%':
                    if self.current_text[self.all_index] and self.string_have(self.current_text[self.all_index], '1234567890'):
                        self.current_text.append('%')
                        self.current_text.append(str())
                        self.all_index += 2

                elif not (self.string_have(self.current_text[self.all_index], '1234567890x÷+-^'+self.all_functions)):
                    self.current_text[self.all_index] += text

            # Handle all other cases
            else:
                self.current_text[self.all_index] += text

        # Update main text input with current text
        self.main_textinput.main_label.text = ''.join(self.current_text)
        self.main_textinput.scroll.scroll_x = 1

        # Evaluate expression if auto_eval is True
        if auto_eval: self.evaluate(self.main_textinput.main_label.text, True)

    def string_have(self, new_text: str, string: str) -> bool:
        """Check if any of the characters in new_text exist in string"""
        for text in new_text:
            if text in string:
                return True
        return False        

    def del_text(self):
        """Delete the last character from current_text and update the main_label"""
        if self.current_text[self.all_index]:
            self.current_text[self.all_index] = self.current_text[self.all_index][:-1]
        else:
            # If there is no character to delete, go back two entries in the history
            if self.all_index > 0:
                self.current_text = self.current_text[:-2]
                self.all_index -= 2

        self.main_textinput.main_label.text = ''.join(self.current_text)
        self.main_textinput.scroll.scroll_x = 1
        self.evaluate(self.main_textinput.main_label.text, True)

    def clear_text(self):
        """Clear the main_label and reset the current_text and all_index variables"""
        self.main_textinput.main_label.text = ''
        self.main_textinput.scroll.scroll_x = 1
        self.all_index = 0
        self.current_text: list[str] = [str()]
        self.evaluate(self.main_textinput.main_label.text, True)
    
    def change_sign_function(self, string: str) -> str:
        """
        Changes the sign of a number in a given string by inserting a minus sign
        before it, or removing it if it already has a minus sign. Returns the
        modified string.
    
        Args:
        - string (str): The string to modify.
    
        Returns:
        - str: The modified string.
        """
        already = False
        end_it = False
        num_str = str()
        new_str = str() 
    
        # loop through reversed string
        for text in reversed(string):
            if end_it:
                pass
            elif already is False:
                # if digit is found, start storing it in num_str
                if text.isdigit():
                    already = True
                    num_str = text + num_str
            else:
                # if non-digit character is found, end the loop
                if text in self.all_operations + '()' + self.all_functions:
                    end_it = True
                    if text == '-': num_str = text + num_str
                    if float(num_str) >= 0:
                        new_str = '-' + new_str
                    else: continue
                else: num_str = text + num_str
    
            # build new string
            new_str = text + new_str
    
        # handle case where loop ends and num_str contains a value
        if end_it is False and already:
            if float(num_str) >= 0:
                new_str = '-' + new_str
            else: new_str = new_str[1:]

        return new_str
    
    def change_sign(self):
        """This method changes the sign of the current text by calling the change_sign_function 
        and updates the label and evaluation."""
        if self.current_text[self.all_index]:
            self.current_text[self.all_index] = self.change_sign_function(self.current_text[self.all_index])
            self.main_textinput.main_label.text = ''.join(self.current_text)
            self.main_textinput.scroll.scroll_x = 1
            self.evaluate(self.main_textinput.main_label.text, True)

    def copy_text(self):
        """This method copies the text from the label to the clipboard."""
        if self.main_textinput.main_label.text:
            Clipboard.copy(self.main_textinput.main_label.text)
        else: 
            Clipboard.copy('0')

    def cut_text(self):
        """This method copies the text from the label to the clipboard and clears the label."""
        self.copy_text()
        self.clear_text()

    def paste_text(self):
        """This method pastes the text from the clipboard to the label and updates the evaluation."""
        old_text = self.main_textinput.main_label.text
        self.clear_text()
        if Clipboard.paste():
            new_text = self.clean_text(Clipboard.paste())
            for text in old_text+new_text:
                self.add_text(text, False)
        self.evaluate(self.main_textinput.main_label.text, True)

    def all_variables(self):
        """All variables"""
        self.all_operations = '*x÷/+-^'
        self.all_functions = '√%'
        self.real_string = str()
        self.all_index = 0
        self.current_text : list[str] = [str()]
        self.already_have_dot = str()

    def _remove_scientific_notation(self, num: float) -> str:
        """Remove scientific notation from a float while maintaining precision.

        Args:
            num (float): The number to convert to a string.

        Returns:
            str: The string representation of the number, with scientific
                notation removed and precision maintained.
        """
        formatted_num = '{:.20f}'.format(num)
        return formatted_num

    def add_str(self, str1: str, str2: str) -> str:
        """Add two string representations of numbers.

        Args:
            str1 (str): The first number to add.
            str2 (str): The second number to add.

        Returns:
            str: The result of adding str1 and str2, as a string.
                If an error occurs (e.g. non-numeric input), returns "ERROR".
        """
        try:
            result = float(str1) + float(str2)
            return self._remove_scientific_notation(result)
        except:
            return "ERROR"

    def min_str(self, str1: str, str2: str) -> str:
        """Subtract one string representation of a number from another.

        Args:
            str1 (str): The number to subtract from.
            str2 (str): The number to subtract.

        Returns:
            str: The result of subtracting str2 from str1, as a string.
                If an error occurs (e.g. non-numeric input), returns "ERROR".
        """
        try:
            result = float(str1) - float(str2)
            return self._remove_scientific_notation(result)
        except:
            return "ERROR"

    def mul_str(self, str1: str, str2: str) -> str:
        """Multiply two string representations of numbers.

        Args:
            str1 (str): The first number to multiply.
            str2 (str): The second number to multiply.

        Returns:
            str: The result of multiplying str1 and str2, as a string.
                If an error occurs (e.g. non-numeric input), returns "ERROR".
        """
        try:
            result = float(str1) * float(str2)
            return self._remove_scientific_notation(result)
        except:
            return "ERROR"

    def div_str(self, str1: str, str2: str) -> str:
        """Divide one string representation of a number by another.

        Args:
            str1 (str): The number to divide.
            str2 (str): The divisor.

        Returns:
            str: The result of dividing str1 by str2, as a string.
                If an error occurs (e.g. non-numeric input or division by zero),
                returns "ERROR".
        """
        try:
            result = float(str1) / float(str2)
            return self._remove_scientific_notation(result)
        except:
            return "ERROR"

    def pow_str(self, str1: str, str2: str) -> str:
        """
        Raise a number to a power.

        Args:
            str1 (str): The base number as a string.
            str2 (str): The exponent as a string.

        Returns:
            str: The result of raising str1 to the power of str2, as a string with no scientific notation.
                 If either str1 or str2 cannot be converted to a float, returns "ERROR".
        """
        try:
            result = pow(float(str1), float(str2))
            return self._remove_scientific_notation(result)
        except:
            return "ERROR"

    def sqrt_str(self, str1: str) -> str:
        """
        Calculate the square root of a number.

        Args:
            str1 (str): The number to calculate the square root of, as a string.

        Returns:
            str: The square root of str1, as a string with no scientific notation.
                 If str1 cannot be converted to a float, returns "ERROR".
        """
        try:
            result = math.sqrt(float(str1))
            return self._remove_scientific_notation(result)
        except:
            return "ERROR"

    def percent_str(self, str1: str) -> str:
        """
        Convert a percentage to a decimal.

        Args:
            str1 (str): The percentage to convert, as a string.

        Returns:
            str: The decimal equivalent of str1, as a string with no scientific notation.
                 If str1 cannot be converted to a float, returns "ERROR".
        """
        try:
            result = float(str1) / 100
            return self._remove_scientific_notation(result)
        except:
            return "ERROR"

    def calculate(self, str1: str, str2: str, operation: str) -> str:
        """Performs the basic arithmetic operations of addition, subtraction,
        multiplication, division, and exponentiation etc. on two given strings.

        Args:
            str1 (str): The first operand.
            str2 (str): The second operand.
            operation (str): The operator to be used for calculation.

        Returns:
            str: The result of the arithmetic operation performed on the two given
            operands.
        """
        if operation == '+':
            return self.add_str(str1, str2)
        elif operation == '-':
            return self.min_str(str1, str2)
        elif operation == 'x':
            return self.mul_str(str1, str2)
        elif operation == '÷':
            return self.div_str(str1, str2)
        elif operation == '^':
            return self.pow_str(str1, str2)

    def calculate2(self, str1: str, operation: str) -> str:
        """Performs the special arithmetic operations of finding square root and
        percentage etc. of a given string.

        Args:
            str1 (str): The string on which the special arithmetic operation is to be
            performed.
            operation (str): The type of special arithmetic operation to be performed.

        Returns:
            str: The result of the special arithmetic operation performed on the given
            string.
        """
        if operation == '√':
            return self.sqrt_str(str1)
        elif operation == '%':
            return self.percent_str(str1)

    def find_and_calculate(self, new_text: str, operation: str) -> str:
        """Finds the first occurrence of the given operation in the given text and performs the operation on the
        numbers that precede and follow it.

        Args:
            new_text (str): The text to search for the operation.
            operation (str): The operation to search for.

        Returns:
            str: The resulting text after performing the operation.
        """

        while True:
            # Initialize variables for the first and second parts of the text surrounding the operation, as well as the
            # first and second numbers.
            first = str()
            second = str()
            first_number = str()
            second_number = str()
            operation_index = None
    
             # If the operation index is not set, find the index of the operation in the text.
            if operation_index is None:
                for index, text in enumerate(new_text):
                    if text in operation:
                        # Skip over negative signs that are not being used as subtraction operators.
                        if text == '-' and (new_text[index-1] in self.all_operations+self.all_functions or index == 0):
                            continue
                        operation_index = index
                        break
            
            # If the operation index is still not set, break out of the loop.
            if operation_index is None:
                break

            already = False
            
            # Loop through the first part of the text to extract the first number and non-numeric characters.
            for text_index in reversed(new_text[:operation_index]):
                if text_index in self.all_operations+self.all_functions or already:
                    # If the character is not the first character and is a negative sign, add it to the first number.
                    if already is False and text_index == '-':
                        first_number = text_index + first_number
                        already = True
                        continue
                    already = True
                    first = text_index + first
                elif text_index.isdigit() or text_index == '.':
                    first_number = text_index + first_number

            already = False
            
            # Loop through the second part of the text to extract the second number and non-numeric characters.
            for text_index in new_text[operation_index+1:]:
                if text_index in self.all_operations+self.all_functions or already:
                    # If the character is not the first character and is a negative sign, add it to the first number.
                    if not second_number and text_index == '-' and already is False:
                        second_number += text_index
                        continue
                    already = True
                    second += text_index
                elif text_index.isdigit() or text_index == '.':
                    second_number += text_index

            # Evaluate the expression and return an error if an error occurs.
            evaluation = self.calculate(first_number, second_number, new_text[operation_index])
            if evaluation == 'ERROR':
                return 'ERROR'
        
            # Clean up the text and continue the loop.
            new_text = self.clean_text(first + evaluation + second)
        return new_text

    def separate_evaluation(self, new_text: str) -> str:
        """
        Separates text into segments that can be evaluated separately, with parentheses taking precedence over other
        operations. Returns the evaluated text as a string.
        """
        while True:
            index_1 = None
            index_2 = None
            for index, text in enumerate(new_text):
                if text == '(':
                    index_1 = index
                elif text == ')' and index_2 is None:
                    index_2 = index
                    break
            if index_1 is not None and index_2 is not None:
                first = new_text[:index_1]
                if first and first[-1].isdigit():
                    first += 'x'
                last = new_text[index_2+1:]
                if last and last[0].isdigit():
                    last = 'x' + last
                new_text = first + self.evaluate(new_text[index_1+1:index_2], True) + last
            elif index_1 is not None:
                first = new_text[:index_1]
                if first and first[-1].isdigit():
                    first += 'x'
                new_text = first + new_text[index_1+1:]
                break
            elif index_2 is not None:
                first = new_text[index_2+1:]
                if first and first[0].isdigit():
                    first = 'x(' + first
                new_text = '(' + first + new_text[:index_2]
                break
            else:
                break
        return new_text

    def function_calculate(self, new_text: str, func_sign: str) -> str:
        """
        Calculates the result of a function in the given text and returns the evaluated text as a string.

        Parameters:
        new_text (str): The text containing the function.
        func_sign (str): The function sign (e.g. 'sin', 'cos', 'tan').

        Returns:
        str: The evaluated text with the function result.
        """
        while True:
            # Initialize variables for the first and second parts of the text surrounding the operation, as well as the
            # first and second numbers.
            first = str()
            first_number = str()
            function_index = None

            if function_index is None:
                for index, text in enumerate(new_text):
                    if text in func_sign:
                        if text == '-' and (new_text[index-1] in self.all_operations+self.all_functions or index == 0):
                            continue
                        function_index = index
                        break

            if function_index is None:
                break

            already = False

            for text_index in new_text[function_index+1:]:
                if text_index in self.all_operations+self.all_functions or already:
                    if not first_number and text_index == '-' and already is False:
                        first_number += text_index
                        continue
                    already = True
                    first += text_index
                elif text_index.isdigit() or text_index == '.':
                    first_number += text_index
            evaluation = self.calculate2(first_number, new_text[function_index])
            if evaluation == 'ERROR':
                return 'ERROR'
            new_text = self.clean_text(new_text[:function_index] + evaluation + first)
        return new_text

    def last_function_calculate(self, new_text: str, func_sign: str):
        """
        Calculates the result of a function at the end of the given text and returns the evaluated text as a string.

        Parameters:
        new_text (str): The text containing the function.
        func_sign (str): The function sign (e.g. 'sin', 'cos', 'tan').

        Returns:
        str: The evaluated text with the function result.
        """
        while True:
            # Initialize variables for the first and second parts of the text surrounding the operation, as well as the
            # first and second numbers.
            first = str()
            first_number = str()
            function_index = None

            if function_index is None:
                for index, text in enumerate(new_text):
                    if text in func_sign:
                        if text == '-' and (new_text[index-1] in self.all_operations+self.all_functions or index == 0):
                            continue
                        function_index = index
                        break

            if function_index is None:
                break

            already = False

            for text_index in reversed(new_text[:function_index]):
                if text_index in self.all_operations+self.all_functions or already:
                    if already is False and text_index == '-':
                        first_number = text_index + first_number
                        already = True
                        continue
                    already = True
                    first = text_index + first
                elif text_index.isdigit() or text_index == '.':
                    first_number = text_index + first_number

            evaluation = self.calculate2(first_number, new_text[function_index])
            if evaluation == 'ERROR':
                return 'ERROR'

            rtext = new_text[function_index+1:]
            if rtext and rtext[0] not in self.all_operations+self.all_functions:
                rtext = 'x' + rtext
            new_text = self.clean_text(first + evaluation + rtext)
        return new_text
    
    def clean_text(self, string: str) -> str:
        """This method takes a string and returns a cleaned version of it by filtering out any 
        characters that are not digits, parentheses, periods, or operators."""
        return ''.join([text for text in string if text in '1234567890().'+self.all_functions+self.all_operations])

    def set_scroll_box(self):
        """This method sets the scroll position of the main and result text inputs to the end."""
        self.main_textinput.scroll.scroll_x = 1
        self.result_textinput.scroll.scroll_x = 1

    def equal_set_all_tracker(self):
        """This method sets the all_index to 0 and updates the current_text to the text in the main 
        label of the main text input."""
        self.all_index = 0
        self.current_text = [self.main_textinput.main_label.text]

    def error_manager(self, result: str, result_box: bool):
        """This method updates the result text input with the given result. If result_box is False, 
        it updates the main label of the main text input with the result if it's not 'ERROR', otherwise 
        it sets it to '0'. It then calls equal_set_all_tracker() and set_scroll_box() methods."""
        self.result_textinput.main_label.text = result
        if result_box is False:
            self.main_textinput.main_label.text = result if result != 'ERROR' else '0'
            self.equal_set_all_tracker()
        self.set_scroll_box()
    
    def count_decimals(self, string: str) -> int:
        """Count how many decimals on String"""
        try:
            d = decimal.Decimal(string)
        except decimal.InvalidOperation:
            return 0
        else:
            return abs(d.as_tuple().exponent)

    def evaluate(self, string: str, result_box: bool = False) -> str:
        """This method takes a string and a result_box parameter (default is False) and evaluates the 
        expression in the string. It returns the evaluated result as a string. If result_box is False, 
        it updates the main label of the main text input with the result. Otherwise, it updates the 
        result text input with the result. It also calls error_manager() and set_scroll_box() methods."""
        new_text = self.clean_text(string)
        new_text = self.separate_evaluation(new_text)

        new_text = self.function_calculate(new_text, '√')
        if new_text == 'ERROR':
            self.error_manager(new_text, result_box)
            return 'ERROR'
        new_text = self.last_function_calculate(new_text, '%')
        if new_text == 'ERROR':
            self.error_manager(new_text, result_box)
            return 'ERROR'
        new_text = self.find_and_calculate(new_text, '^')
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
            try:
                result = (new_text if not new_text or (len(new_text)==1 and new_text == '-')
                      else (str(int(float(new_text))) if int(float(new_text)) == float(new_text) else new_text))
                if self.count_decimals(result) > 8:
                    result = result[:-(self.count_decimals(result)-8)]

            except: result = 'ERROR'
            self.error_manager(result, result_box)
        return new_text
