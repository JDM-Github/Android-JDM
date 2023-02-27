from jdm_kivy import *

class MainScreen(JDMScreen): ...

class CardBox(JDMWidget):

    __all_shadow_pos__ = ['n', 'l', 'r', 't', 'b', 'lt', 'lb', 'rt', 'rb']
    shadow_pos = StringProperty('lb')
    shadow_width = NumericProperty(0)
    radius = ListProperty([10, 10, 10, 10])
    card_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'shadow_pos' in kwargs: self.shadow_pos = kwargs.get('shadow_pos')
        if 'shadow_width' in kwargs: self.shadow_width = kwargs.get('shadow_width')
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
            Color(rgba=GetColor('00000055'))
            self._card_shadow = RoundedRectangle(radius=self.radius)
            Color(rgba=GetColor('55555555'))
            self._card_line = RoundedRectangle(radius=self.radius)
            self._card_col = Color(rgba=self.card_color)
            self._card_rect = RoundedRectangle(radius=self.radius)

    def _change(self, *_):
        if not self.shadow_pos in self.__all_shadow_pos__:
            raise KeyError(f"{self.shadow_pos} not in {self.__all_shadow_pos__}")

        self._card_rect.size = self.size
        self._card_rect.pos = self.pos
        
        self._card_shadow.size = self.size
        self._card_shadow.pos = (
            self.x + (self.shadow_width if 'r' in self.shadow_pos else (-self.shadow_width if 'l' in self.shadow_pos else 0)),
            self.y + (self.shadow_width if 't' in self.shadow_pos else (-self.shadow_width if 'b' in self.shadow_pos else 0)))
        self._card_line.size = self.size
        self._card_line.pos = (
            self.x + (self.shadow_width/2 if 'r' in self.shadow_pos else (-self.shadow_width/2 if 'l' in self.shadow_pos else 0)),
            self.y + (self.shadow_width/2 if 't' in self.shadow_pos else (-self.shadow_width/2 if 'b' in self.shadow_pos else 0)))

class ShowButtonCard(CardBox):
    
    def __init__(self, text='Show Info', func_bind=lambda: None, **kwargs):
        super().__init__(**kwargs)
        self.func_binder = func_bind
        self.card_color = GetColor('598baf')
        self.main_label = JDMLabel(text=text)
        self.add_widget(self.main_label)
        self.size = Window.width*0.3, Window.height*0.03
    
    def _change(self, *_):
        self.main_label.size = self.size
        self.main_label.pos = self.pos
        return super()._change(*_)

class TopicCard(CardBox):
    
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y=None
        self.height=Window.height*0.07
        # self.shadow_width=dp(4)
        self.card_color = GetColor('0395c5')
        self.main_label = JDMLabel(bold=True, text=text, font_size=dp(13))
        self.card_info = ShowButtonCard()
        self.card_info.width = Window.width*0.2
        self.card_open = ShowButtonCard('Open')
        self.card_open.width = Window.width*0.15
        self.add_widget(self.main_label)
        self.add_widget(self.card_info)
        self.add_widget(self.card_open)

    def _change(self, *_):
        if hasattr(self, "card_info"):
            self.main_label.size = (self.width*0.5, self.height)
            self.main_label.pos = self.pos
            self.card_info.pos = self.x+self.width-self.card_info.width-dp(10), self.y+Window.height*0.02
            self.card_open.pos = self.x+self.width-self.card_info.width-self.card_open.width-dp(15), self.y+Window.height*0.02
        return super()._change(*_)

class MainCardBox(CardBox):
    
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

class MainField(JDMWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = GetColor('95c8d8')
        self.size = self.root.size
        self.display_all_topic()

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
            RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos)
        # self.grid.add_widget(JDMLabel(halign='center', valign='top', font_size=dp(14), size_hint_y=None, height=Window.height*0.4, text=(
        #     "This reviewer application is a comprehensive tool designed to help students in their first year, second semester Computer Science and IT courses prepare for exams and tests. With coverage of important topics including Object-Oriented Programming, Information Management, Data Structures and Algorithms, Networks and Communication, Number Theory, Purposive Communication, Mechanics, Rhythm Activities, and National Services Training Program 2, this application is an all-in-one solution for students who are looking to review and consolidate their knowledge."
        #     "The application provides a range of review materials such as practice questions, quizzes, flashcards, and study guides for each subject. These materials are carefully crafted to help students identify areas where they need to improve and to test their knowledge of important concepts and topics. By using this reviewer application, students can review key concepts, practice important skills, and gain confidence in their ability to succeed in their exams and tests."
        #     "In short, this reviewer application is an essential tool for any student in their first year, second semester Computer Science or IT course who wants to make their study easier and more effective. Whether you are looking to review for an upcoming exam or simply want to improve your understanding of key concepts, this application has everything you need to succeed."
        # )))
        
        """
        CS102 -> Object oriented Programming
        IT102 -> Information Management
        IT201 -> Data Structures and Algorithms
        NC102 -> Networks and Communication
        NUM102 -> Number Theory
        PCOM102 -> Purposive Communication
        CALC102 -> Mechanics
        PE102 -> Rhythm Activities
        NSTP102 -> National Services Training Program 2
        """
        self.grid.add_widget(MainCardBox(size_hint_y=None, card_color=GetColor(JDM_getColor('JDM')),
                                         height=Window.height*0.15))
        self.grid.add_widget(TopicCard("CS102 -> Object oriented Programming"))
        self.grid.add_widget(TopicCard("IT102 -> Information Management"))
        self.grid.add_widget(TopicCard("IT201 -> Data Structures and Algorithms"))
        self.grid.add_widget(TopicCard("NC102 -> Networks and Communication"))
        self.grid.add_widget(TopicCard("NUM102 -> Number Theory"))
        self.grid.add_widget(TopicCard("PCOM102 -> Purposive Communication"))
        self.grid.add_widget(TopicCard("CALC102 -> Mechanics"))
        self.grid.add_widget(TopicCard("PE102 -> Rhythm Activities"))
        self.grid.add_widget(TopicCard("NSTP102 -> National Services Training Program 2"))
        
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)
