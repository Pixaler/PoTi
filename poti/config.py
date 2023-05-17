import json
import os
import sys

if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.getcwd()

USER_DATA_FOLDER = os.path.join(application_path, "user_data")
RESOURCES_FOLDER = os.path.join(application_path, "resources")

if os.path.exists(USER_DATA_FOLDER):
    pass
else:
    os.makedirs(USER_DATA_FOLDER)

print(os.getcwd())
SOUND_PATH = os.path.join(RESOURCES_FOLDER, "bell.wav")
STATS_PATH = os.path.join(USER_DATA_FOLDER, "stats.json")
CONFIG_PATH = os.path.join(USER_DATA_FOLDER, "settings.json")
print(SOUND_PATH)
print(STATS_PATH)
print(CONFIG_PATH)


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
