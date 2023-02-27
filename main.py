from src import MainField, MainScreen, JDMApp

if __name__ == "__main__":
    JDMApp("JDM-Reviewer", (720*0.5, 1400*0.5)).run(screen_name="main", screen=MainScreen(), widget=MainField())
