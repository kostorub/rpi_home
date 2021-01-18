from kivy.lang import Builder
from kivy.uix.button import Button

from src.common import config
from src.service.relay_service_client import RelayServiceClient

Builder.load_file(__file__.replace(".py", ".kv"))

class RelayButton(Button):
    def __init__(self, **kwargs):
        self.relay = kwargs.pop("relay")
        self.relay.button = self
        super(RelayButton, self).__init__(**kwargs)

    def pressed(self):
        self.relay.off(on_send=self.on_send) \
            if self.relay.state else \
                self.relay.on(on_send=self.on_send)

    def on_send(self, state):
        self.relay.state = state
        if state:
            self.text = "[color=#00FF00]" + self.relay.name + "[/color]"
        else:
            self.text = "[color=#FF0000]" + self.relay.name + "[/color]"

    def get_remote_state(self):
        RelayServiceClient(
            self.relay,
            callback=self.on_send,
            get_remote_status=True)
