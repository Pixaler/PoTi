import customtkinter
from CTkMessagebox import CTkMessagebox

from poti.config import config


class PoTiSettings(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("PoTi Settings")
        # self.geometry("550x430")
        self.resizable(False, False)
        self.config(padx=20, pady=20)

        self.work_min_label = customtkinter.CTkLabel(
            self,
            text="Work duration(min): ",
        )
        self.work_min_label.grid(column=0, row=2, sticky="e")
        self.work_min_label.configure(pady=10)

        self.work_min_entry = customtkinter.CTkEntry(self, width=30)
        self.work_min_entry.insert(0, string=config.config["work_min"])
        self.work_min_entry.grid(column=1, row=2)

        self.break_min_label = customtkinter.CTkLabel(
            self,
            text="Break duration(min): ",
        )
        self.break_min_label.grid(column=0, row=3, sticky="e")
        self.break_min_label.configure(pady=10)

        self.break_min_entry = customtkinter.CTkEntry(self, width=30)
        self.break_min_entry.insert(0, string=config.config["short_break_min"])
        self.break_min_entry.grid(column=1, row=3)

        self.long_break_min_label = customtkinter.CTkLabel(
            self,
            text="Long break duration(min): ",
        )
        self.long_break_min_label.grid(column=0, row=4, sticky="e")
        self.long_break_min_label.configure(pady=10)

        self.long_break_min_entry = customtkinter.CTkEntry(self, width=30)
        self.long_break_min_entry.insert(0, string=config.config["long_break_min"])
        self.long_break_min_entry.grid(column=1, row=4)

        self.apply_btn = customtkinter.CTkButton(
            self,
            text="Apply",
            height=1,
            width=8,
            command=self.change_config,
        )
        self.apply_btn.grid(column=0, row=8, pady=10)

        self.reset_default_btn = customtkinter.CTkButton(
            self,
            text="Default",
            height=1,
            width=8,
            command=self.change_default,
        )
        self.reset_default_btn.grid(column=1, row=8, pady=10)

    def change_config(self):
               config.config["work_min"] = int(self.work_min_entry.get())
               config.config["short_break_min"] = int(self.break_min_entry.get())
               config.config["long_break_min"] = int(self.long_break_min_entry.get())
               config.save_config(config)

               self.destroy()
               CTkMessagebox(
                   title="Done",
                   message="Settings are applied"
               )

    def change_default(self):
        config.config["work_min"] = 25
        config.config["short_break_min"] = 5
        config.config["long_break_min"] = 15
        config.save_config(config)

        self.destroy()
        CTkMessagebox(
            title="Done",
            message="Default settings are restored"
        )
