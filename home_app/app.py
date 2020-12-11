#!/home/pi/git/rpi_home/venv/bin/python3
import os

os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'

from src.widgets.main import MainApp
from kivy.config import Config

Config.set("graphics", "width", 480)
Config.set("graphics", "height", 320)



app = MainApp()
app.run()
