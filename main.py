from jdm_kivy import *
from src import MainScreen, MainField

class MainApp(JDMApp, App):
    def __init__(self, title: str = None, size: list = ..., manager: JDMRootManager = None, **kwargs):
        super().__init__(title, size, manager, **kwargs)

if __name__ == "__main__":
    MainApp("Calculator", (720*0.5, 1400*0.5)).run(screen=MainScreen(), widget=MainField())
