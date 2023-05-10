import json
import os

SOUND_PATH = "resources/bell.wav"
USER_DATA_FOLDER = "user_data"
STATS_PATH = USER_DATA_FOLDER + "/stats.json"
CONFIG_PATH = USER_DATA_FOLDER + "/settings.json"

if os.path.exists(USER_DATA_FOLDER):
    pass
else:
    os.makedirs(USER_DATA_FOLDER)

def get_config():
        config = {}
        try:
            with open(CONFIG_PATH, "r") as settings:
                config = json.load(settings)
        except FileNotFoundError:
            with open(CONFIG_PATH, "w") as settings:
                config = {
                    "work_min": 25,
                    "short_break_min": 5,
                    "long_break_min": 15,
                }
                json.dump(config, settings, indent=4)
        finally:
            config["sound"] = SOUND_PATH
            config["stats"] = STATS_PATH
        return config

class PoTiConfig():
    def __init__(self, startup_config: dict):
        self.config = startup_config

    def save_config(self, config):
       with open(CONFIG_PATH, "w") as config:
           new_config = {
               "work_min": self.config["work_min"],
               "short_break_min": self.config["short_break_min"],
               "long_break_min": self.config["long_break_min"],
           }
           json.dump(new_config, config, indent=4)

startup_config = get_config()
config = PoTiConfig(startup_config)
