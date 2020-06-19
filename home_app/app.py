from asyncore import poll

from kivy.clock import Clock

from src.widgets.main import MainApp

Clock.schedule_interval(poll, 0.01)

app = MainApp()
app.run()
