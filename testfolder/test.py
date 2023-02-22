from kivy.uix.label import Label

class NewLabel(Label):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Hello World Test"