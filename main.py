from jdm_kivy import *
from src import MainScreen, MainField

if __name__ == "__main__":
    JDMConfig.set("display_kivy_logs", False)
    JDMApp("Calculator", (720*0.5, 1400*0.5)).run(screen=MainScreen(), widget=MainField())
