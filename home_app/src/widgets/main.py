from kivy.uix.layout import Layout
from kivy.app import App
import kivy.uix.button
from src.control_button import ControlButton


class MainApp(App):
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")
        self.controllers = kwargs.get("controllers")

    def build(self):
        pass
