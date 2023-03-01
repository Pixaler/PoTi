from datetime import datetime
import json
from json import JSONDecodeError


class TimerProcces():

    def __init__(self, config) -> None:
        self.reps = 0
        self.mark = ""
        self.config = config

    def reset_timer(self):
        if len(self.mark) != 0:
            today = datetime.now()
            today = today.strftime("%Y-%m-%d")
            work_sessions = len(self.mark)
            overal_hours = work_sessions * self.config["work_min"] // 60
            overal_mins = work_sessions * self.config["work_min"] % 60
            if overal_mins < 10:
                overal_mins = f"0{overal_mins}"
            overal_time = f"{overal_hours}:{overal_mins}"
            new_data = {today:
                        {
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
                    work_sessions = work_sessions + \
                        data[today]["work_sessions"]
                    overal_hours = work_sessions * \
                        self.config["work_min"] // 60
                    overal_mins = work_sessions * self.config["work_min"] % 60
                    if overal_mins < 10:
                        overal_mins = f"0{overal_mins}"
                    overal_time = f"{overal_hours}:{overal_mins}"
                    new_data = {today:
                                {
                                    "overall_time": overal_time,
                                    "work_sessions": work_sessions,
                                }
                                }
                data.update(new_data)
                with open(self.config["stats"], "w") as stats:
                    json.dump(data, stats, indent=4)
            finally:
                self.mark = ""
                self.reps = 0
