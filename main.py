from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#d3eca7"
RED = "#eb3303"
GREEN = "#a1b57d"
BLACK = "#19282f"
FONT_NAME = "Courier"
WORK_MIN = 40
SHORT_BREAK_MIN = 10
LONG_BREAK_MIN = 10
SOUND = "bell.mp3"
reps = 0
mark = "" 
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global mark 
    mark = ""
    global reps
    reps = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    name_label.config(text="Timer")
    tick_label.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    work_sec = WORK_MIN * 60
    short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60
    
    reps += 1

    if reps % 8 == 0:
        name_label.config(text="Long Break", fg=RED)
        count_down(long_break)
    elif reps % 2 != 0: 
        name_label.config(text="Work", fg=GREEN)
        count_down(work_sec)
    else:
        name_label.config(text="Break", fg=BLACK)
        count_down(short_break)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0: 
        global timer 
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        if reps % 2 == 0:
            global mark 
            mark = f"{mark}" + "✓"
            tick_label.config(text=mark)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=30, bg=WHITE)

canvas = Canvas(width=200, height=223, highlightthickness=0, bg=WHITE)
tomato_image = PhotoImage(file="tomato.png")
canvas.create_image(100, 111, image=tomato_image)
timer_text = canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 29, "bold"))
canvas.grid(column=1, row=1)

name_label = Label(text="Timer", fg=GREEN, bg=WHITE, font=(FONT_NAME, 38))
name_label.grid(column=1, row=0)
name_label.config(pady=10)

start_button = Button(text="Start", height=1, width=8, bg=WHITE, font=(FONT_NAME, 13, 'bold'), command=start_timer)
start_button.grid(column=0, row=2)
start_button.config(pady=10)

reset_button = Button(text="Reset", height=1, width=8, bg=WHITE, font=(FONT_NAME, 13, 'bold'), command=reset_timer)
reset_button.grid(column=2, row=2)
reset_button.config(pady=10)

tick_label = Label(bg=WHITE, fg=GREEN, font=(FONT_NAME, 16))
tick_label.grid(column=1, row=3)

window.mainloop()
