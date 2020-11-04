import bot
from datetime import datetime
import keyboard
import logging


logging.basicConfig(level=logging.INFO)

map_config = bot.Config("config.json")
intralism_bot = bot.Bot('enter', 'esc', map_config, wait=0)

keyboard.wait()
