from asyncore import poll

from kivy.clock import Clock

import src.common
from src.widgets.main import MainApp

Clock.schedule_interval(poll, 0.1)

app = MainApp()
app.run()
