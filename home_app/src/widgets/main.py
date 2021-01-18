from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from home_service.src.models.device_list import DeviceList
from src.common import config, model_path
from src.models.relay import Relay
from src.models.dht11 import DHT11
from src.speech_recognition import SpeechRecognition
from src.widgets.relay_button import RelayButton
from src.widgets.dht11_label import DHT11Label
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

        self.relays = DeviceList(
            [Relay(
                relay["bcm_pin"],
                relay["phrase_on"],
                relay["phrase_off"],
                relay["name"]) for relay in config["relays"]])
                
        for relay in self.relays:
            button = RelayButton(
                relay=relay, 
                text=relay.name)
            self.ids.grid_control_buttons.add_widget(button)

        self.dht11s = DeviceList(
            [DHT11(
                dht11["bcm_pin"],
                dht11["phrase"],
                dht11["name"]) for dht11 in config["dht11s"]])

        for dht11 in self.dht11s:
            label = DHT11Label(
                dht11=dht11, 
                text=dht11.name)
            self.ids.grid_control_buttons.add_widget(label)

    def on_speech(self, text):
        self.ids.label_speech.text = text
        relay, state = self.relays.find_similar_phrase(text)
        if relay:
            callback = relay.button.on_send
            relay.on(on_send=callback) \
                if state else \
                    relay.off(on_send=callback)
    
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
