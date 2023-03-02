import random
import json
import os
from kivy.core.clipboard import Clipboard
from jdm_kivy import *

class MainScreen(JDMScreen):
    def handleBackButton(self) -> bool:
        self.main.back_button()
        return super().handleBackButton()
class ShowButtonCard(JDMCardBox):
    
    def __init__(self, text='Show Info', func_bind=lambda: None, **kwargs):
        super().__init__(**kwargs)
        self.clicked = False
        self.func_binder = func_bind
        self.card_color = GetColor('598baf')
        self.main_label = JDMLabel(text=text, font_size=dp(13))
        self.add_widget(self.main_label)
        self.size = Window.width*0.3, Window.height*0.03

    def _change(self, *_):
        self.main_label.size = self.size
        self.main_label.pos = self.pos
        return super()._change(*_)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.clicked = True
            self.card_color = GetColor('396b8f')
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.clicked:
            self.clicked = False
            self.func_binder()
            self.card_color = GetColor('598baf')
        return super().on_touch_up(touch)

class TopicCard(JDMCardBox):

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.card_color = GetColor('0395c5')
        self.main_label = JDMLabel(bold=True, text=text, font_size=dp(13))
        self.card_info = ShowButtonCard(func_bind=lambda : self.parent.change_showed_info())
        self.card_info.width = Window.width*0.2
        self.card_open = ShowButtonCard('Open')
        self.card_open.width = Window.width*0.15
        self.add_widget(self.main_label)
        self.add_widget(self.card_info)
        self.add_widget(self.card_open)

    def _change(self, *_):
        if hasattr(self, "card_info"):
            self.main_label.size = (self.width*0.5-dp(5), self.height-dp(5))
            self.main_label.pos = self.x+dp(5)/2, self.y+dp(5)/2
            self.card_info.pos = self.x+self.width-self.card_info.width-dp(10), self.y+Window.height*0.02
            self.card_open.pos = self.x+self.width-self.card_info.width-self.card_open.width-dp(15), self.y+Window.height*0.02
        return super()._change(*_)

class InfoWidget(JDMCardBox):

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.card_color = GetColor('598baf')
        self.height = 0
        self.pos = (-Window.width, -Window.height)
        self.real_height = (len(text)*dp(14) / (Window.width)) * dp(14) + dp(10)
        self.display_title(text)

    def display_title(self, text):
        self.main_label = JDMLabel(
            size=self.size,
            pos=self.pos,
            text=text,
            font_size=dp(14),
            halign='left',
            valign='top',
        )
        self.add_widget(self.main_label)

    def _change(self, *_):
        if hasattr(self, "main_label"):
            self.main_label.size = (self.width-dp(10), self.height-dp(20))
            self.main_label.pos = self.x+dp(5), self.y+dp(5)

        return super()._change(*_)

class TopicWidget(JDMWidget):

    info_height = NumericProperty(0)

    def __init__(self, text, info_text='', widget=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.showed_info = False
        self.height = Window.height * 0.07
        self.main_topic_widget = widget if widget else JDMWidget()
        self.display_topic_and_info(text, info_text)
        self.bind(size=self._change, pos=self._change)
        self.bind(info_height=self.animation_info)

    def display_topic_and_info(self, text, info_text):
        self.main_topic = TopicCard(text, height=Window.height*0.07)
        self.main_topic.card_open.func_binder = lambda : self.root.main.main.display_main_topic(self.main_topic_widget)
        self.main_info = InfoWidget(info_text)
        self.add_widget(self.main_info)
        self.add_widget(self.main_topic)

    def change_showed_info(self):
        self.showed_info = not self.showed_info
        if self.showed_info:
            self.main_topic.card_info.main_label.text = 'Close Info'
            Animation(info_height=self.main_info.real_height, d=0.1, t='linear').start(self)
        else:
            self.main_topic.card_info.main_label.text = 'Show Info'
            anim = Animation(info_height=0, d=0.1, t='linear')
            anim.bind(on_complete=lambda *_: setattr(self.main_info, 'pos', (-Window.width, -Window.height)))
            anim.start(self)

    def animation_info(self, *_):
        self.main_info.height = self.info_height + dp(10)
        self.height = Window.height * 0.07 + self.info_height

    def _change(self, *_):
        self.main_topic.width = self.width
        self.main_topic.pos = self.x, self.y + self.info_height
        self.main_info.width = self.width
        if self.info_height: self.main_info.pos  = self.pos

class NormalCard(JDMCardBox):

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.card_color = GetColor(JDM_getColor('JDM'))
        self.main_label = JDMLabel(
            color=GetColor('598baf'),
            bold=True, markup=True, text=text, font_size=dp(20))
        self.add_widget(self.main_label)

    def _change(self, *_):
        if hasattr(self, "main_label"):
            self.main_label.size = (self.width-dp(5), self.height-dp(5))
            self.main_label.pos = self.x+dp(5)/2, self.y+dp(5)/2
        return super()._change(*_)

class ExtraNormalCard(JDMWidget):
    
    info_height = NumericProperty(Window.height*0.2)

    def __init__(self, text, info_text='', rheight=Window.height*0.2, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.info_height = rheight
        self.main_info = InfoWidget(info_text)
        self.main_info.height = self.info_height
        self.main_topic = NormalCard(text, height=self.height)
        self.height += self.info_height

        self.add_widget(self.main_info)
        self.add_widget(self.main_topic)
        self.bind(size=self._change, pos=self._change)

    def _change(self, *_):
        self.main_topic.width = self.width
        self.main_topic.pos = self.x, self.y + self.info_height
        self.main_info.width = self.width
        if self.info_height: self.main_info.pos  = self.x, self.y+dp(10)

class DataStructAndAlgorithms(JDMWidget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open('jsons/IT102.json') as f:
            self.config = json.load(f)
        self.size = self.root.size
        self.display_scroll()
        self.bind(pos=lambda *_: setattr(self.scroll, 'x', self.x+Window.width*0.05))
        self.pos = (Window.width, 0)

    def display_scroll(self):
        self.grid = JDMGridLayout(cols=1, padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll = JDMScrollView(
            bar_color=GetColor('00000000'),
            bar_inactive_color=GetColor('00000000'),
            size=(Window.width*0.9, Window.height*0.95-dp(10)),
            pos=(Window.width*0.05, dp(10))
        )
        with self.canvas:
            Color(rgb=GetColor('598baf'), a=0.5)
            self.rect = RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos)
        self.scroll.bind(pos=lambda *_: setattr(self.rect, 'pos', self.scroll.pos))
        
        self.grid.add_widget(ExtraNormalCard(
            text="[size=24dp][color=ffffff]Data Structures[/color][/size] and [size=24dp][color=ffffff]Algorithms[/color][/size] (IT201)",
            info_text=''.join(self.config.get('Description')), rheight=Window.height*(self.config.get('Rheight')),
            height=Window.height*0.15))
    
        self.grid.add_widget(ExtraNormalCard(
            '[color=ffffff]Introduction[/color]',
            info_text=''.join(self.config.get('1')), rheight=Window.height*1.7,
            height=Window.height*0.05))
    
        self.grid.add_widget(NormalCard('[color=ffffff]Data Structures[/color]', size_hint_y=None, height=Window.height*0.05))

        self.grid.add_widget(arr:=ExtraNormalCard('Arrays',
            info_text=''.join(self.config.get('Arrays')) + '\n[b][color=03d5f5][ref=implement]See Implementation...[/ref][/b][/color]', rheight=Window.height*0.35,
            height=Window.height*0.05))
        arr.main_info.main_label.markup = True
        arr.main_info.main_label.implement = lambda : self.root.main.main.show_implement('implementation/array/')
        self.grid.add_widget(arr:=ExtraNormalCard('Linked Lists',
            info_text=''.join(self.config.get('Linked Lists')) + '\n[b][color=03d5f5][ref=implement]See Implementation...[/ref][/b][/color]', rheight=Window.height*0.4,
            height=Window.height*0.05))
        arr.main_info.main_label.markup = True
        arr.main_info.main_label.implement = lambda : self.root.main.main.show_implement('implementation/linklist/')
        self.grid.add_widget(arr:=ExtraNormalCard('Stacks',
            info_text=''.join(self.config.get('Stacks')) + '\n[b][color=03d5f5][ref=implement]See Implementation...[/ref][/b][/color]', rheight=Window.height*0.35,
            height=Window.height*0.05))
        arr.main_info.main_label.markup = True
        arr.main_info.main_label.implement = lambda : self.root.main.main.show_implement('implementation/stack/')
        self.grid.add_widget(arr:=ExtraNormalCard('Queues',
            info_text=''.join(self.config.get('Queues')) + '\n[b][color=03d5f5][ref=implement]See Implementation...[/ref][/b][/color]', rheight=Window.height*0.4,
            height=Window.height*0.05))
        arr.main_info.main_label.markup = True
        arr.main_info.main_label.implement = lambda : self.root.main.main.show_implement('implementation/queue/')
        self.grid.add_widget(arr:=ExtraNormalCard('Trees',
            info_text=''.join(self.config.get('Trees')) + '\n[b][color=03d5f5][ref=implement]See Implementation...[/ref][/b][/color]', rheight=Window.height*0.35,
            height=Window.height*0.05))
        arr.main_info.main_label.markup = True
        arr.main_info.main_label.implement = lambda : self.root.main.main.show_implement('implementation/tree/')
        self.grid.add_widget(arr:=ExtraNormalCard('Graphs',
            info_text=''.join(self.config.get('Graphs')) + '\n[b][color=03d5f5][ref=implement]See Implementation...[/ref][/b][/color]', rheight=Window.height*0.35,
            height=Window.height*0.05))
        arr.main_info.main_label.markup = True
        arr.main_info.main_label.implement = lambda : self.root.main.main.show_implement('implementation/graph/')

        self.grid.add_widget(NormalCard('[color=ffffff]Algorithms[/color]', size_hint_y=None, height=Window.height*0.05))
        
        self.grid.add_widget(ExtraNormalCard('Sorting',
            info_text=''.join(self.config.get('Sorting')), rheight=Window.height*0.45, height=Window.height*0.05))
        self.grid.add_widget(ExtraNormalCard('Searching',
            info_text=''.join(self.config.get('Searching')), rheight=Window.height*0.45, height=Window.height*0.05))
        self.grid.add_widget(ExtraNormalCard('Recursive Algorithms',
            info_text=''.join(self.config.get('Recursive Algorithms')), rheight=Window.height*0.45, height=Window.height*0.05))
        self.grid.add_widget(ExtraNormalCard('Dynamic Programming',
            info_text=''.join(self.config.get('Dynamic Programming')), rheight=Window.height*0.45, height=Window.height*0.05))
        self.grid.add_widget(ExtraNormalCard('Greedy Algorithms',
            info_text=''.join(self.config.get('Greedy Algorithms')), rheight=Window.height*0.45, height=Window.height*0.05))

        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

class MainCardBox(JDMCardBox):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display_description()
        self.bind(pos=self.change, size=self.change)
    
    def display_description(self):
        self.main_label = JDMLabel(markup=True, font_size=dp(35), bold=True, color=GetColor('598baf'),
            text="[size=55dp][color=ffffff]JDM[/color][/size]Reviewer")
        self.add_widget(self.main_label)
        self.info_card = ShowButtonCard()
        self.add_widget(self.info_card)

    def change(self, *_):
        self.main_label.size = self.width, self.height/2
        self.main_label.pos = self.x, self.y+self.height*0.4
        self.info_card.pos = self.x+dp(10), self.y+dp(10)

class CodeExample(JDMWidget):
    
    def __init__(self, path='', **kwargs):
        super().__init__(**kwargs)
        self.index_nav = 0
        self.size = Window.width*0.8, Window.height*0.7
        self.pos = (Window.width*0.1, 0)
        self.manage_path(path)
        self.display_design()
        self.bind(pos=self.change)

    def manage_path(self, path):
        self.all_lang = list()
        self.all_text = list()
        
        if os.path.exists(path):
            all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if all_files:
                for f in all_files:
                    self.all_lang.append(os.path.splitext(f)[1][1:])
                    with open(path+f, 'r') as fi:
                       self.all_text.append(self.get_langauge(self.all_lang[-1]) + fi.read())
            else:
                self.all_lang.append('')
                self.all_text.append('')
        else:
            self.all_lang.append('')
            self.all_text.append('')

    def get_langauge(self, lang):
        if lang == 'py': return "# Python Implementation\n"
        if lang == 'c': return "// C Implementation\n"
        if lang == 'cpp': return "// C++ Implementation\n"
        if lang == 'js': return "// JavaScript Implementation\n"
        if lang == 'java': return "// Java Implementation\n"

    def change_language(self):
        self.index_nav += 1
        self.index_nav %= len(self.all_text)
        self.code.text = self.all_text[self.index_nav]
        self.colorized_language(self.all_lang[self.index_nav])

    def colorized_language(self, lang='py'):
        self.lexes = {
            
        }

    def display_design(self):
        with self.canvas:
            Color(rgb=GetColor(JDM_getColor('black')), a=0.5)
            Rectangle(size=Window.size)
            Color(rgba=GetColor(JDM_getColor('JDM')))
            self.rect = RoundedRectangle(
                size=self.size, pos=self.pos,
                radius=[10, 10, 10, 10])
        self.change_button = ShowButtonCard(
            text='Change Language',
            func_bind=self.change_language,
            size=(self.width-dp(10), self.height*0.1-dp(10)),
            pos=(self.x+dp(5), self.y+self.height*0.9+dp(5))
        )
        self.add_widget(self.change_button)
        self.code = JDMCode(
            font_size=dp(11),
            color=GetColor('ffffff'),
            code_color=GetColor('0395c5'),
            text=self.all_text[self.index_nav],
            size=(self.width-dp(10), self.height*0.9-dp(10)),
            pos=(self.x+dp(5), self.y+dp(5))
        )
        self.colorized_language(self.all_lang[self.index_nav])
        self.add_widget(self.code)
        self.copy_button = ShowButtonCard(
            text='Copy',
            pos=(self.x+self.width-(Window.width*0.3+dp(10)), self.y+dp(10)),
            func_bind=lambda *_: Clipboard.copy(self.code.text)
        )
        self.add_widget(self.copy_button)

    def change(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.code.pos = (self.x+dp(5), self.y+dp(5))
        self.copy_button.pos = (self.x+self.width-(Window.width*0.3+dp(10)), self.y+dp(10))
        self.change_button.size = (self.width-dp(10), self.height*0.1-dp(10))
        self.change_button.pos = (self.x+dp(5), self.y+self.height*0.9+dp(5))

class MainField(JDMWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clicked = False
        Window.clearcolor = GetColor('95c8d8')
        self.size = self.root.size
        self.current_widget = None
        self.code_example_widget = None
        self.all_topic_widget : list[JDMWidget] = list()
        self.display_all_topic()

    def show_implement(self, path=''):
        if self.code_example_widget:
            self.remove_widget(self.code_example_widget)
            self.code_example_widget = None

        self.code_example_widget = CodeExample(path)
        self.add_widget(self.code_example_widget)
        Animation(y=Window.height*0.15, d=0.2, t='linear').start(self.code_example_widget)

    def on_touch_down(self, touch):
        if self.code_example_widget and self.code_example_widget.collide_point(*touch.pos):
            self.clicked = True        
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.clicked is False:
            if self.code_example_widget:
                self.remove_widget(self.code_example_widget)
                self.code_example_widget = None
        self.clicked = False
        return super().on_touch_up(touch)

    def display_main_topic(self, widget: JDMWidget):
        if not widget in self.all_topic_widget:
            self.all_topic_widget.append(widget)
        widget.x = Window.width
        self.current_widget = widget
        self.remove_widget(widget)
        self.add_widget(widget)
        Animation(x=-Window.width, d=0.2, t='linear').start(self.scroll)
        Animation(x=0, d=0.2, t='linear').start(widget)

    def back_button(self):
        if self.code_example_widget:
            self.remove_widget(self.code_example_widget)
            self.code_example_widget = None
            self.clicked = False
        elif self.current_widget:
            Animation(x=Window.width*0.05, d=0.2, t='linear').start(self.scroll)
            Animation(x=Window.width, d=0.2, t='linear').start(self.current_widget)
            self.current_widget = None

    def display_all_topic(self):
        self.grid = JDMGridLayout(cols=1, padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll = JDMScrollView(
            bar_color=GetColor('00000000'),
            bar_inactive_color=GetColor('00000000'),
            size=(Window.width*0.9, Window.height*0.95-dp(10)),
            pos=(Window.width*0.05, dp(10))
        )
        with self.canvas:
            Color(rgb=GetColor('598baf'), a=0.5)
            self.rect = RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos)
        self.scroll.bind(pos=lambda *_: setattr(self.rect, 'pos', self.scroll.pos))
        self.grid.add_widget(MainCardBox(size_hint_y=None, card_color=GetColor(JDM_getColor('JDM')),
                                         height=Window.height*0.15))
        # self.grid.add_widget(TopicWidget("JDMSpecial -> Basic Programming"))
        self.grid.add_widget(TopicWidget("Object-Oriented Programming (CS102)",
            "This course teaches the fundamentals of object-oriented programming. "
            "Object-oriented programming is a programming paradigm based on the concept of \"objects\", "
            "which can contain data and code to manipulate that data. "
            "The course covers topics such as classes, inheritance, polymorphism, and encapsulation."))

        self.grid.add_widget(TopicWidget("Information Management (IT102)",
            "Information management refers to the process of organizing, storing, "
            "and retrieving information. This course covers topics such as database design, data modeling, and database management systems."))

        self.grid.add_widget(TopicWidget("Data Structures and Algorithms (IT201)",
            "This course teaches the fundamentals of data structures and algorithms. "
            "Data structures are ways of organizing and storing data, while algorithms are "
            "sets of instructions that solve specific problems. The course covers topics such as arrays, "
            "linked lists, stacks, queues, trees, graphs, sorting algorithms, and searching algorithms.",
            DataStructAndAlgorithms()))

        self.grid.add_widget(TopicWidget("Networks and Communication (NC102)",
            "This course covers the basics of computer networks and communication. "
            "It teaches the concepts of protocols, network architectures, network topologies, and network security."))

        self.grid.add_widget(TopicWidget("Number Theory (NUM102)",
            "Number theory is the study of numbers and their properties. "
            "This course covers topics such as prime numbers, divisibility, congruences, and Diophantine equations."))

        self.grid.add_widget(TopicWidget("Purposive Communication (PCOM102)",
            "Purposive communication refers to the process of communicating with a specific goal in mind. "
            "This course covers topics such as effective communication strategies, persuasive communication, and public speaking."))

        self.grid.add_widget(TopicWidget("Mechanics (CALC102)",
            "Mechanics is a branch of physics that deals with the motion and forces of objects. "
            "This course covers topics such as Newton's laws of motion, energy, and momentum."))

        self.grid.add_widget(TopicWidget("Rhythm Activities (PE102)",
            "Rhythm activities refer to physical activities that involve movements in time with music. "
            "This course covers topics such as dance, music, and other rhythmic activities."))

        self.grid.add_widget(TopicWidget("National Services Training Program 2 (NSTP102)",
            "The National Services Training Program (NSTP) is a program mandated by the government "
            "of the Philippines for students in tertiary education. NSTP 2 specifically focuses on "
            "the civic welfare and defense preparedness of the country. "
            "It covers topics such as disaster preparedness, environmental conservation, and national defense."))
        
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)
