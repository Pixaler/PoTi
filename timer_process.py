from datetime import datetime
import json
from json import JSONDecodeError


class TimerProcces:
    def __init__(self, config) -> None:
        self.reps = 0
        self.mark = ""
        self.config = config
        self.get_data()

    def get_data(self):
        try:
            with open(self.config["stats"], "r") as stats:
                data = json.load(stats)
                today = datetime.now().strftime("%Y-%m-%d")
                sessions = data[today]["work_sessions"]
                for _ in range(1, sessions + 1):
                    self.mark = self.mark + "✓"
        except (JSONDecodeError, FileNotFoundError, KeyError):
            pass

    def update_stats(self):
        if len(self.mark) != 0:
            today = datetime.now()
            today = today.strftime("%Y-%m-%d")
            work_sessions = len(self.mark)
            overal_hours = work_sessions * self.config["work_min"] // 60
            overal_mins = work_sessions * self.config["work_min"] % 60
            if overal_mins < 10:
                overal_mins = f"0{overal_mins}"
            overal_time = f"{overal_hours}:{overal_mins}"
            new_data = {
                today: {
                    "overall_time": overal_time,
                    "work_sessions": work_sessions,
                }
            }
            try:
                with open(self.config["stats"], "r") as stats:
                    data = json.load(stats)

            except (JSONDecodeError, FileNotFoundError):
                with open(self.config["stats"], "w") as stats:
                    json.dump(new_data, stats, indent=4)
            else:
                if today in data:
                    work_sessions = len(self.mark)
                    overal_hours = work_sessions * self.config["work_min"] // 60
                    overal_mins = work_sessions * self.config["work_min"] % 60
                    if overal_mins < 10:
                        overal_mins = f"0{overal_mins}"
                    overal_time = f"{overal_hours}:{overal_mins}"
                    new_data = {
                        today: {
                            "overall_time": overal_time,
                            "work_sessions": work_sessions,
                        }
                    }
                data.update(new_data)
                with open(self.config["stats"], "w") as stats:
                    json.dump(data, stats, indent=4)

    def reset_timer(self):
        self.reps = 0

    def save_config(self):
        with open(self.config["config"], "w") as config:
            new_config = {
                "work_min": self.config["work_min"],
                "break_min": self.config["break_min"],
                "long_break_min": self.config["long_break_min"],
                "background_color": self.config["background_color"],
                "foreground_color": self.config["foreground_color"],
                "break_font_color": self.config["break_font_color"],
                "long_break_font_color": self.config["long_break_font_color"],
                "font_name": self.config["font_name"],
            }
            json.dump(new_config, config, indent=4)

    def default_config(self):
        with open(self.config["config"], "w") as settings:
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
