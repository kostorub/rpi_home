from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from home_service.src.models.device_list import DeviceList
from src.common import config, model_path
from src.models.controller_app import ControllerApp
from src.speech_recognition import SpeechRecognition
from src.widgets.control_button import ControlButton
from threading import Timer

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        # self.sr = SpeechRecognition(model_path)

        # Clock.schedule_interval(
        #     partial(
        #         self.sr.recognition_loop, 
        #         callback_speech=self.on_speech,
        #         callback_permission=self.check_call_sign), 0.1)

        self.controllers = DeviceList(
            [ControllerApp(
                relay["bcm_pin"],
                relay["phrase_on"],
                relay["phrase_off"],
                relay["name"]) for relay in config["relays"]])
                
        for controller in self.controllers:
            button = ControlButton(
                controller=controller, 
                text=controller.name)
            self.ids.grid_control_buttons.add_widget(button)

    def on_speech(self, text):
        self.ids.label_speech.text = text
        controller, state = self.controllers.find_similar_phrase(text)
        if controller:
            callback = controller.button.on_send
            controller.on(on_send=callback) \
                if state else \
                    controller.off(on_send=callback)
    
    def check_call_sign(self, text):
        if text == config["call_sign"]:
            self.allow_command()

    def allow_command(self):
        self.ids.label_permission.color = (0, 1, 0, 1)
        self.sr.can_command = True
        self.timer = Timer(30, self.deny_command)
        self.timer.start()

    def deny_command(self):
        self.ids.label_permission.color = (1, 0, 0, 1)
        self.sr.can_command = False


class MainApp(App):
    title = "Smart home"

    def build(self):
        return MainWidget()
