'''
    This documents several exercises and challenges throughout day 27 of the 100 days of Python coding.
'''

from tkinter import *

def add(*args) -> int:
    ''' Function that adds any number of arguments. NOTE: It's given as a tuple.'''
    total = 0
    for arg in args:
        total += arg
    return total

def button_clicked():
    ''' Button click handler. '''
    my_label.config(text=input.get())


window = Tk()
window.title("My app")
window.minsize(width=500, height=300)

# label
my_label = Label(text="I am a label", font=("Arial", 24))
my_label.grid(column=0, row=0)

# button
my_button = Button(text="Click Me", command=button_clicked)
my_button.grid(column=1, row=1)

# New button
new_button = Button(text="New Button", command=button_clicked)
new_button.grid(column=2, row=0)

# Entry

input = Entry(width=10)
input.grid(column=3, row=3)

window.mainloop()

if __name__ == "__main__":
    pass