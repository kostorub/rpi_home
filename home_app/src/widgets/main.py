from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from home_core.src.models.controller_list import ControllerList
from src.common import config, model_path
from src.models.controller_app import ControllerApp
from src.speech_recognition import SpeechRecognition
from src.widgets.control_button import ControlButton


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.sr = SpeechRecognition(model_path)

        Clock.schedule_interval(partial(self.sr.recognition_loop, callback=self.on_speech), 0.1)

        self.controllers = ControllerList(
            [ControllerApp(
                binding["bcm_pin"], 
                binding["name"]) for binding in config["bindings"]])
        print(self.controllers)

        for controller in self.controllers:
            button = ControlButton(
                controller=controller, 
                text=controller.name)
            self.ids.grid_control_buttons.add_widget(button)

    def on_speech(self, text):
        self.ids.label_speech.text = text


class MainApp(App):
    title = "Smart home"

    def build(self):
        return MainWidget()
