import json
import os
import sys
from ui import PoTiInterface
from timer_process import TimerProcces

# ---------------------------- SET WORKING DIRECTORY ------------------------------- #

sound_path = "./resources/bell.wav"
image_path = "./resources/tomato.png"
user_data_path = "./user_data"
stats_path = "./user_data/stats.json"
config_path = "./user_data/settings.json"

# determine if application is a script file or frozen exe
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

SOUND = os.path.join(application_path, sound_path)
IMAGE = os.path.join(application_path, image_path)
STATS = os.path.join(application_path, stats_path)
CONFIG = os.path.join(application_path, config_path)
USER_DATA_PATH = os.path.join(application_path, user_data_path)

if os.path.exists(USER_DATA_PATH):
    pass
else:
    os.makedirs(USER_DATA_PATH)

# ---------------------------- CONSTANTS ------------------------------- #
config = {}
try:
    with open(CONFIG, "r") as settings:
        config = json.load(settings)
except FileNotFoundError:
    with open(CONFIG, "w") as settings:
        config = {
            "work_min": 25,
            "break_min": 5,
            "long_break_min": 15,
            "background_color": "#d3eca7",
            "foreground_color": "#a1b57d",
            "break_font_color": "#19282f",
            "long_break_font_color": "#eb3303",
            "font_name": "Courier",
        }
        json.dump(config, settings, indent=4)
finally:
    config["sound"] = SOUND
    config["image"] = IMAGE
    config["stats"] = STATS
    config["config"] = CONFIG

timer_process = TimerProcces(config)
poti_ui = PoTiInterface(timer_process.config, timer_process)

timer_process.reset_timer()
