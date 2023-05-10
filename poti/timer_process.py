from pydub import AudioSegment
from pydub.playback import play

import poti.poti_ui as pu
from poti.config import config
from poti.stats import update_stats


reps = 0
mark = ""


def start_timer():
    work_sec = config.config['work_min'] * 60
    short_break = config.config['short_break_min'] * 60
    long_break = config.config['long_break_min'] * 60

    global reps
    reps += 1

    if reps % 8 == 0:
        pu.app.stage_status.configure(
            text="Long Break"
        )
        count_down(long_break)
    elif reps % 2 != 0:
        pu.app.stage_status.configure(text="Work")
        count_down(work_sec)
    else:
        pu.app.stage_status.configure(text="Break")
        count_down(short_break)


def count_down(seconds):
    '''Run countdown'''
    count_min = seconds // 60
    count_sec = seconds % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    pu.app.timer_countdown.configure(text=f"{count_min}:{count_sec}")
    if seconds > 0:
        pu.app.timer = pu.app.after(1000, count_down, seconds - 1)
    else:
        sound = AudioSegment.from_file(config["sound"])
        play(sound)
        start_timer()

        global reps
        if reps % 2 == 0:
            global mark
            mark += "✓"
            pu.app.tick_label.configure(text=mark)
            update_stats()


def reset_timer():
    global reps
    reps = 0

    pu.app.after_cancel(pu.app.timer)
    pu.app.timer_countdown.configure(text="00:00")
    pu.app.stage_status.configure(text="Timer")
    pu.app.tick_label.configure(text="")

