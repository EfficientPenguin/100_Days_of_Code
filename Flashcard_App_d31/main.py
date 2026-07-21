'''
    A flash card application using Tkinter.
    1. Show a card to the user, and give them 3sec to answer.
        If correct, then press "checkmark"; else, click "X"

'''

from tkinter import *
import json
import random

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

LANG_FILE = "chamorro.json"
lang_dict = None
words_as_keys = None
word = None
flip_timer = None

# -------------- Reading in Flashcards ------------
words = {
    "kannai": "hand",
    "chalan": "road",
    "niyok": "coconut",
    "tasi": "ocean",
    "golai": "vegetable"
}

with open(file=LANG_FILE, mode="r") as file:
    lang_dict = json.load(file)

def next_card() -> None:
    ''' Display the next Chamorro card. '''
    global words_as_keys
    global word
    global flip_timer

    window.after_cancel(flip_timer)

    if len(words_as_keys) > 0:
        # Select a random word from the read-in dict
        word = random.choice(words_as_keys)
    else:
        word = "Empty"

    # Update the text for the word to reflect the word
    canvas.itemconfigure(lang_id, text="Chamorro")
    canvas.itemconfigure(word_id, text=word)

    flip_timer = window.after(3000, func=display_new_word)

def display_new_word() -> None:
    ''' Generate a random word form the list of choices and display the new word.'''
    global words_as_keys
    global word
    global flip_timer

    window.after_cancel(flip_timer)

    # Start a timer for 3 sec, display english word, wait for button(s) to be pressed
    canvas.itemconfigure(lang_id, text="English")
    canvas.itemconfigure(word_id, text=words[word] if word != "Empty" else "Empty")

# -------------- Button Handlers ------------------------
def cross_button_handler():
    ''' Fetch a new word to display. Don't remove word from the list.'''
    display_new_word()

def check_button_handler():
    ''' Remove the word from the dict and list and fetch a new word to display.'''
    global words_as_keys
    global word

    if len(words_as_keys) <= 0 or word is None:
        return
    
    words_as_keys.remove(word)

    next_card()

# -------------- GUI ------------------------
# Window
window = Tk()
window.title("Flashy")
window.config(bg=GREEN)
window.config(padx=50, pady=50)

# White card image and canvas
flashcard_img = PhotoImage(file="./canvas.png")
canvas = Canvas(width=650, height=306, bg=GREEN, highlightthickness=0)
canvas.create_image(375, 153,image=flashcard_img)
lang_id = canvas.create_text(375, 60, text="Chamorro", font=(FONT_NAME, 40, "bold"), fill="black")
word_id = canvas.create_text(375, 180, text="Word", font=(FONT_NAME, 60, "bold"), fill="black")
canvas.grid(column=0, row=0, columnspan=2)

# Create the "checkmark" button and "X" button
check_button = Button(text="✅", bg=GREEN, highlightthickness=0, command=check_button_handler)
check_button.grid(column=0, row=1)

x_button = Button(text="❌", bg=GREEN, highlightthickness=0, command=cross_button_handler)
x_button.grid(column=1, row=1)

# --------- App code --------------------
# Select a random word from the read-in dict
words_as_keys = list(lang_dict.keys())

flip_timer = window.after(3000, func=next_card)

#display_new_word()

window.mainloop()