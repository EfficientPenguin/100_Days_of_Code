'''
    This application implements a simple password generator and manager for the user given a
    set of rules.
'''

from tkinter import *
from tkinter import messagebox
import random
import json

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

WRITE_FILE = "./data.json"

LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SYMBOLS = '!@#$%^&*()-_+='
DIGITS = '0123456789'

# -------------- Handlers -------------------
def gen_pass_handler():
    ''' Handler for when the Generate Password button is pressed. '''
    print('Generated password!')
    
    # Clear current password
    password_textbox.delete(0, END)

    num_letters = random.randint(8,10)
    num_symbols = random.randint(2,4)
    num_digits = random.randint(2,4)

    # Build the password
    password = [random.choice([letter for letter in LETTERS]) for _ in range(num_letters)]
    password.extend([random.choice([symbol for symbol in SYMBOLS]) for _ in range(num_symbols)])
    password.extend([random.choice([digit for digit in DIGITS]) for _ in range(num_digits)])
    random.shuffle(password)

    # Set the password in the text field
    password_textbox.insert(END, "".join(password))

def add_button_handler():
    ''' Handler for when the Add button is pressed. '''
    website = website_textbox.get()
    email = email_textbox.get()
    password = password_textbox.get()

    data = None

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) > 0 and len(password) > 0:
        ok_to_save = messagebox.askokcancel(title=website, message=f"These are the details entered: \n" 
                                            f"Email: {email}\nPassword: {password} \nIs it ok to save?")
        
        # Save to file
        if ok_to_save:
            try:
                with open(WRITE_FILE, "r") as file:
                    # Read old data
                    data = json.load(file)
            except FileNotFoundError:
                with open(WRITE_FILE, "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open(WRITE_FILE, "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_textbox.delete(0,END)
                password_textbox.delete(0,END)
    else:
        messagebox.showerror(title="Error!", message="Empty fields detected! Please try again.")

def search_handler():
    ''' Handler for the search button to read in the data.json and find the corresponding password for a website if it exists. '''
    # Read in teh text from search button
    website = website_textbox.get()

    if len(website) > 0:
        # Read in the file
        try:
            with open(WRITE_FILE, mode="r") as file:
                websites = json.load(file)
                password_textbox.delete(0, END)
                password_textbox.insert(index=END, string=websites[website]["password"])
        except FileNotFoundError:
            messagebox.showerror(title="Error!", message=f"{WRITE_FILE} doesn't exist!")
        except KeyError as key_message:
            messagebox.showerror(title="Error!", message=f"{key_message} doesn't exist in current file!")



# -------------- GUI ------------------------
# Window
window = Tk()
window.title("MyPass")
window.config(padx=30, pady=30)

# Lock image and canvas
lock_img = PhotoImage(file="./lock.gif")
canvas = Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 100,image=lock_img)
canvas.grid(column=2, row=1)

# Website Label and text
website_label = Label(text="Website:")
website_label.grid(column=1, row=2)
website_textbox = Entry(width=30)
website_textbox.grid(column=2,row=2, columnspan=1)
website_textbox.focus()

# Email/Username label and text
email_label = Label(text="Email/Username:")
email_label.grid(column=1, row=3)
email_textbox = Entry(width=30)
email_textbox.grid(column=2,row=3, columnspan=1)
email_textbox.insert(END, "user@gmail.com")

# Password Label and text
password_label = Label(text="Password:")
password_label.grid(column=1, row=4)
password_textbox = Entry(width=15)
password_textbox.grid(column=2,row=4, columnspan=1)

# Generate Password button
generate_button = Button(text="Generate Password", command=gen_pass_handler, width=20)
generate_button.grid(column=3, row=4)

# Add button
generate_button = Button(text="Add", command=add_button_handler, width=20)
generate_button.grid(column=2, row=5)

# Search button
search_button = Button(text="Search", command=search_handler, width=20)
search_button.grid(column=3, row=2)



window.mainloop()