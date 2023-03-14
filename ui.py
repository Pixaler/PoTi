from tkinter import *
from tkinter import messagebox
from timer_process import TimerProcces
from playsound import playsound


class PoTiInterface:
    def __init__(self, config: dict, timer_process: TimerProcces) -> None:
        self.config = config

        self.timer = None
        self.process = timer_process

        self.window = Tk()
        self.window.geometry("600x450")
        self.window.minsize(600, 450)
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=30, bg=self.config["background_color"])

        self.frame = Frame(bg=self.config["background_color"])
        self.canvas = Canvas(
            self.frame,
            width=200,
            height=223,
            highlightthickness=0,
            bg=self.config["background_color"],
        )
        self.tomato_image = PhotoImage(file=self.config["image"])
        self.canvas.create_image(100, 111, image=self.tomato_image)
        self.timer_text = self.canvas.create_text(
            103,
            130,
            text="00:00",
            fill="white",
            font=(self.config["font_name"], 29, "bold"),
        )
        self.canvas.grid(column=1, row=1)

        self.name_label = Label(
            self.frame,
            text="Timer",
            fg=self.config["foreground_color"],
            bg=self.config["background_color"],
            font=(self.config["font_name"], 38),
        )
        self.name_label.grid(column=1, row=0)
        self.name_label.config(pady=10)

        self.start_button = Button(
            self.frame,
            text="Start",
            height=1,
            width=8,
            bg=self.config["background_color"],
            font=(self.config["font_name"], 13, "bold"),
            command=self.start_timer,
        )
        self.start_button.grid(column=0, row=2)
        self.start_button.config(pady=10)

        self.reset_button = Button(
            self.frame,
            text="Reset",
            height=1,
            width=8,
            bg=self.config["background_color"],
            font=(self.config["font_name"], 13, "bold"),
            command=self.reset_timer,
        )
        self.reset_button.grid(column=2, row=2)
        self.reset_button.config(pady=10)

        self.settings_button = Button(
            self.frame,
            text="⚙",
            height=1,
            width=1,
            bg=self.config["background_color"],
            font=(self.config["font_name"], 13, "bold"),
            command=self.settings,
        )
        self.settings_button.place(relx=0.85, rely=0.01)

        self.tick_label = Label(
            self.frame,
            bg=self.config["background_color"],
            fg=self.config["foreground_color"],
            font=(self.config["font_name"], 16),
        )
        self.tick_label.grid(column=1, row=3)
        self.tick_label.config(text=self.process.mark)
        self.frame.place(anchor=CENTER, relx=0.5, rely=0.5)

        self.window.mainloop()

    def reset_timer(self):
        self.process.reset_timer()
        self.window.after_cancel(self.timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.name_label.config(text="Timer")
        self.tick_label.config(text="")

    def start_timer(self):
        work_sec = self.config["work_min"] * 60
        short_break = self.config["break_min"] * 60
        long_break = self.config["long_break_min"] * 60

        self.process.reps += 1

        if self.process.reps % 8 == 0:
            self.name_label.config(
                text="Long Break", fg=self.config["long_break_font_color"]
            )
            self.count_down(long_break)
        elif self.process.reps % 2 != 0:
            self.name_label.config(text="Work", fg=self.config["foreground_color"])
            self.count_down(work_sec)
        else:
            self.name_label.config(text="Break", fg=self.config["break_font_color"])
            self.count_down(short_break)

    def count_down(self, count):
        count_min = count // 60
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"

        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            playsound(self.config["sound"])
            self.start_timer()
            if self.process.reps % 2 == 0:
                self.process.mark = f"{self.process.mark}" + "✓"
                self.tick_label.config(text=self.process.mark)
                self.process.update_stats()

    def settings(self):
        def change_config():
            self.config["work_min"] = int(work_min_entry.get())
            self.config["break_min"] = int(break_min_entry.get())
            self.config["long_break_min"] = int(long_break_min_entry.get())
            self.config["background_color"] = bg_color_entry.get()
            self.config["foreground_color"] = fg_color_entry.get()
            self.config["break_font_color"] = break_font_color_entry.get()
            self.config["long_break_font_color"] = long_break_font_color_entry.get()
            self.config["font_name"] = font_name_entry.get()
            self.process.save_config()
            settings_window.destroy()
            messagebox.showinfo(
                title="Done",
                message="Settings are applied",
            )

        def change_default():
            self.config["work_min"] = 25
            self.config["break_min"] = 5
            self.config["long_break_min"] = 15
            self.config["background_color"] = "#d3eca7"
            self.config["foreground_color"] = "#a1b57d"
            self.config["break_font_color"] = "#19282f"
            self.config["long_break_font_color"] = "#eb3303"
            self.config["font_name"] = "Courier"
            self.process.save_config()
            settings_window.destroy()
            messagebox.showinfo(
                title="Done",
                message="Default settings are restored",
            )

        settings_window = Toplevel(self.window)
        settings_window.title("PoTi Settings")
        settings_window.geometry("550x430")
        settings_window.resizable(False, False)
        settings_window.config(padx=20, pady=20, bg=self.config["background_color"])

        work_min_label = Label(
            settings_window,
            text="Work duration(min): ",
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
        )
        work_min_label.grid(column=0, row=2, sticky="e")
        work_min_label.config(pady=10)
        work_min_entry = Entry(settings_window, width=15)
        work_min_entry.insert(0, self.config["work_min"])
        work_min_entry.grid(column=1, row=2)

        break_min_label = Label(
            settings_window,
            text="Break duration(min): ",
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
        )
        break_min_label.grid(column=0, row=3, sticky="e")
        break_min_label.config(pady=10)
        break_min_entry = Entry(settings_window, width=15)
        break_min_entry.insert(0, self.config["break_min"])
        break_min_entry.grid(column=1, row=3)

        long_break_min_label = Label(
            settings_window,
            text="Long break duration(min): ",
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
        )
        long_break_min_label.grid(column=0, row=4, sticky="e")
        long_break_min_label.config(pady=10)
        long_break_min_entry = Entry(settings_window, width=15)
        long_break_min_entry.insert(0, self.config["long_break_min"])
        long_break_min_entry.grid(column=1, row=4)

        bg_color_label = Label(
            settings_window,
            text="Background color: ",
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
        )
        bg_color_label.grid(column=0, row=0, sticky="e")
        bg_color_label.config(pady=10)
        bg_color_entry = Entry(settings_window, width=15)
        bg_color_entry.insert(0, self.config["background_color"])
        bg_color_entry.grid(column=1, row=0)

        fg_color_label = Label(
            settings_window,
            text="Foreground color: ",
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
        )
        fg_color_label.grid(column=0, row=1, sticky="e")
        fg_color_label.config(pady=10)
        fg_color_entry = Entry(settings_window, width=15)
        fg_color_entry.insert(0, self.config["foreground_color"])
        fg_color_entry.grid(column=1, row=1)

        break_font_color_label = Label(
            settings_window,
            text="Break font color: ",
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
        )
        break_font_color_label.grid(column=0, row=5, sticky="e")
        break_font_color_label.config(pady=10)
        break_font_color_entry = Entry(settings_window, width=15)
        break_font_color_entry.insert(0, self.config["break_font_color"])
        break_font_color_entry.grid(column=1, row=5)

        long_break_font_color_label = Label(
            settings_window,
            text="Long break font color: ",
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
        )
        long_break_font_color_label.grid(column=0, row=6, sticky="e")
        long_break_font_color_label.config(pady=10)
        long_break_font_color_entry = Entry(settings_window, width=15)
        long_break_font_color_entry.insert(0, self.config["long_break_font_color"])
        long_break_font_color_entry.grid(column=1, row=6)

        font_name_label = Label(
            settings_window,
            text="Font family name: ",
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
        )
        font_name_label.grid(column=0, row=7, sticky="e")
        font_name_label.config(pady=10)
        font_name_entry = Entry(settings_window, width=15)
        font_name_entry.insert(0, self.config["font_name"])
        font_name_entry.grid(column=1, row=7)

        apply_btn = Button(
            settings_window,
            text="Apply",
            height=1,
            width=8,
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
            command=change_config,
        )
        apply_btn.grid(column=0, row=8, pady=10)
        reset_default_btn = Button(
            settings_window,
            text="Default",
            height=1,
            width=8,
            bg=self.config["background_color"],
            font=(self.config["font_name"], 14, "bold"),
            command=change_default,
        )
        reset_default_btn.grid(column=1, row=8, pady=10)
