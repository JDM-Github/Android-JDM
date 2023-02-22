from jdm_kivy import *
from kivy.app import App
from src import MainField

if __name__ == "__main__":
    JDMApp("Calculator", (720*0.5, 1400*0.5)).run(widget=MainField())
