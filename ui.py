from tkinter import *
from timer_process import TimerProcces
from playsound import playsound


class PoTiInterface():

    def __init__(self, config: dict, timer_process: TimerProcces) -> None:
        self.config = config

        self.timer = None
        self.process = timer_process

        self.window = Tk()
        self.window.geometry("600x450")
        self.window.minsize(600, 450)
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=30,
                           bg=self.config["background_color"])

        self.frame = Frame(bg=self.config["background_color"])
        self.canvas = Canvas(self.frame,
                             width=200, height=223, highlightthickness=0, bg=self.config["background_color"])
        self.tomato_image = PhotoImage(file=self.config['image'])
        self.canvas.create_image(100, 111, image=self.tomato_image)
        self.timer_text = self.canvas.create_text(
            103, 130, text="00:00", fill="white", font=(self.config["font_name"], 29, "bold"))
        self.canvas.grid(column=1, row=1)

        self.name_label = Label(self.frame, text="Timer", fg=self.config["foreground_color"], bg=self.config["background_color"], font=(
            self.config["font_name"], 38))
        self.name_label.grid(column=1, row=0)
        self.name_label.config(pady=10)

        self.start_button = Button(self.frame, text="Start", height=1, width=8, bg=self.config["background_color"], font=(
            self.config["font_name"], 13, 'bold'), command=self.start_timer)
        self.start_button.grid(column=0, row=2)
        self.start_button.config(pady=10)

        self.reset_button = Button(self.frame, text="Reset", height=1, width=8, bg=self.config["background_color"], font=(
            self.config["font_name"], 13, 'bold'), command=self.reset_timer)
        self.reset_button.grid(column=2, row=2)
        self.reset_button.config(pady=10)

        self.tick_label = Label(self.frame, bg=self.config["background_color"], fg=self.config["foreground_color"], font=(
            self.config["font_name"], 16))
        self.tick_label.grid(column=1, row=3)
        self.tick_label.config(text=self.process.mark)
        self.frame.place(anchor=CENTER, relx=.5, rely=.5)

        self.window.mainloop()

    def reset_timer(self):
        self.process.reset_timer()
        self.window.after_cancel(self.timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.name_label.config(text="Timer")
        self.tick_label.config(text="")

    def start_timer(self):
        work_sec = self.config['work_min'] * 60
        short_break = self.config['break_min'] * 60
        long_break = self.config['long_break_min'] * 60

        self.process.reps += 1

        if self.process.reps % 8 == 0:
            self.name_label.config(
                text="Long Break", fg=self.config["long_break_font_color"])
            self.count_down(long_break)
        elif self.process.reps % 2 != 0:
            self.name_label.config(
                text="Work", fg=self.config["foreground_color"])
            self.count_down(work_sec)
        else:
            self.name_label.config(
                text="Break", fg=self.config['break_font_color'])
            self.count_down(short_break)

    def count_down(self, count):
        count_min = count // 60
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"

        self.canvas.itemconfig(
            self.timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            playsound(self.config['sound'])
            self.start_timer()
            if self.process.reps % 2 == 0:
                self.process.mark = f"{self.process.mark}" + "✓"
                self.tick_label.config(text=self.process.mark)
                self.process.update_stats()
