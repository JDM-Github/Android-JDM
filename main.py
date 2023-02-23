# from jdm_kivy import *
# from src import MainField

# if __name__ == "__main__":
#     JDMApp("Calculator", (720*0.5, 1400*0.5)).run(widget=MainField())
from kivy.app import App
from testfolder import NewLabel

class NewApp(App):
    
    def build(self):
        return NewLabel()

if __name__ == "__main__":
    NewApp().run()
