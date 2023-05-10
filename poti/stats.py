from datetime import datetime
import json
from json import JSONDecodeError
import poti.timer_process as ptp
from poti.config import config


def get_data():
        try:
            with open(config.config["stats"], "r") as stats:
                data = json.load(stats)
                today = datetime.now().strftime("%Y-%m-%d")
                sessions = data[today]["work_sessions"]
                for _ in range(1, sessions + 1):
                    ptp.mark = ptp.mark + "✓"

                return ptp.mark
        except (JSONDecodeError, FileNotFoundError, KeyError):
            pass


def update_stats():
        if len(ptp.mark) != 0:
            today = datetime.now()
            today = today.strftime("%Y-%m-%d")
            work_sessions = len(ptp.mark)
            overal_hours = work_sessions * config.config["work_min"] // 60
            overal_mins = work_sessions * config.config["work_min"] % 60
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
                with open(config.config["stats"], "r") as stats:
                    data = json.load(stats)

            except (JSONDecodeError, FileNotFoundError):
                with open(config.config["stats"], "w") as stats:
                    json.dump(new_data, stats, indent=4)
            else:
                if today in data:
                    work_sessions = len(ptp.mark)
                    overal_hours = work_sessions * config.config["work_min"] // 60
                    overal_mins = work_sessions * config.config["work_min"] % 60
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
                with open(config.config["stats"], "w") as stats:
                    json.dump(data, stats, indent=4)
