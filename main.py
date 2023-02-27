import json
from src import MainField, MainScreen, JDMApp

class CustomApp(JDMApp):

    def on_stop(self):
        with open('jsons/history.json', 'w') as f:
            json.dump(self.root.main.main.config, f, indent=2)
        return super().on_stop()

if __name__ == "__main__":
    CustomApp("Calculator", (720*0.5, 1400*0.5)).run(screen_name="main", screen=MainScreen(), widget=MainField())
