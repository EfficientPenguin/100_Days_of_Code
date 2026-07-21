'''
    This application implements a simple pomodoro timer with a reset and start button. Pomodoro is an effective
    studying technique that works in phases: 25min on work, 5min break, then repeat 4x, followed by a longer 20min break.
    This application is a direct implementation of Day 28 in the 100 days of code by Dr. Angela Yu
'''

from tkinter import *
import time

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 20
NUM_POMODORO_SESSIONS = 4
CHECKMARK_START_ROW = 2
CHECKMARK_COL = 1

checkmark_row = CHECKMARK_START_ROW
checkmarks = []

timer = None
reps = 0

# ----------- Button Handlers -----------
def start_button_handler():
    start_timer()

def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        timer_label.config(text="BREAK", fg=RED)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        timer_label.config(text="BREAK", fg=PINK)
        count_down(short_break_sec)
        create_checkmark()
    else:
        timer_label.config(text="WORK", fg=GREEN)
        create_checkmark()
        count_down(work_sec)

def count_down(count):
    global timer

    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_id, text=f"{count_min}:{count_sec}")

    if count > 0:
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()


def pomodoro_sequence(start_time: int) -> None:
    ''' Execute a pomodoro sequence/timer that keeps counting down according to on_work bool.'''
    
    time_in_seconds = start_time * 60

    while time_in_seconds > 0:
        min_fmt = str(time_in_seconds//60)
        min_fmt = min_fmt if len(min_fmt) == 2 else "0"+min_fmt
        sec_fmt = str(time_in_seconds%60)
        sec_fmt = sec_fmt if len(sec_fmt) == 2 else "0"+sec_fmt

        canvas.itemconfigure(timer_id, text=f"{min_fmt}:{sec_fmt}")
        window.update()
        
        window.after(1000, None)
        time_in_seconds -=1

def create_checkmark():
    ''' Create a checkmark and append it to the global list of checkmarks. '''
    global checkmark_row

    checkmark = Label(text="✅", fg=YELLOW, bg=YELLOW)
    checkmark.grid(column=CHECKMARK_COL, row=checkmark_row)
    checkmark_row += 1
    checkmarks.append(checkmark)

def reset_button_handler():
    ''' Reset the timer back to its start time, remove checkmarks on screen. '''
    global reps
    global checkmarks
    global checkmark_row

    if timer:
        window.after_cancel(timer)
        canvas.itemconfigure(timer_id, text=f"00:00")
        timer_label.config(text="Timer", fg=GREEN)
        reps = 0

        # Clear checkmarks
        for checkmark in checkmarks:
            checkmark.config(text="", fg=YELLOW, bg=YELLOW)
        checkmark_row = CHECKMARK_START_ROW
    

# ----------- UI Setup ------------
window = Tk()
window.title("Pomodoro App")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=426, height=470, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="./tomato.png")
canvas.create_image(213, 235,image=tomato_img)
timer_id = canvas.create_text(213, 300, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Create the Timer label above the tomato
timer_label = Label(text="Timer", font=(FONT_NAME, 54, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

# Create a Start button
start_button = Button(text="Start", bg=YELLOW, command=start_button_handler, highlightthickness=0)
start_button.grid(column=0, row=2)

# Create a Reset button
reset_button = Button(text="Reset", bg=YELLOW, command=reset_button_handler, highlightthickness=0)
reset_button.grid(column=2, row=2)

# Create a checkmark for every successful pomodoro sequence (i.e., 25min + 5min break, checkmark should be created)

window.mainloop()