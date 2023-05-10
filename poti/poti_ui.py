import tkinter
import customtkinter

import poti.timer_process as ptp
from poti.stats import get_data
from poti.poti_settings_ui import PoTiSettings



# customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class PoTiUi(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.timer = None

        self.title("PoTi")
        self.geometry(f"{960}x{540}")
        self.minsize(960, 540)
        self.configure(padx=100, pady=30)

        self.main_frame = customtkinter.CTkFrame(self, width=960, height=540, fg_color=self._fg_color)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.stage_status = customtkinter.CTkLabel(
            self.main_frame,
            text="Timer",
            font=customtkinter.CTkFont(size=38)
        )
        self.stage_status.grid(column=1, row=0)

        self.timer_countdown = customtkinter.CTkLabel(
            self.main_frame,
            text="00:00",
            font=customtkinter.CTkFont(size=72)
        )
        self.timer_countdown.grid(column=1, row=1)
        self.timer_countdown.configure(pady=70)

        self.start_button = customtkinter.CTkButton(
            self.main_frame,
            text="Start",
            width=120,
            height=50,
            command=ptp.start_timer
        )
        self.start_button.grid(row=2, column=0)

        self.reset_button = customtkinter.CTkButton(
            self.main_frame,
            text="Reset",
            width=120,
            height=50,
            command=ptp.reset_timer
        )
        self.reset_button.grid(row=2, column=2)

        self.tick_label = customtkinter.CTkLabel(
            self.main_frame,
            text=get_data(),
            font=customtkinter.CTkFont(size=24),
        )
        self.tick_label.grid(row=3, column=1)

        self.settings_button = customtkinter.CTkButton(
            self.main_frame,
            text="⚙",
            height=24,
            width=24,
            font=customtkinter.CTkFont(size=20),
            command=self.settings
        )
        self.settings_button.place(relx=0.85, rely=0.01)

        self.toplevel_window = None

    def settings(self):
        self.toplevel_window = PoTiSettings()



app = PoTiUi()
app.mainloop()
