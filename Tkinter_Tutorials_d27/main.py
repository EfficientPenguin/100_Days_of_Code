'''
    This application implements a simple miles to kilometer converter using
    Python's Tkinter module for buildling the GUI.
'''

from tkinter import *

FONT = ("Arial", 20)

def convert_miles_to_km():
    ''' Convert the miles in the text filed to km. '''
    miles = float(input.get())
    km = miles*1.60934

    # Update the results label
    conversion_label.config(text=f"{km:0.2f}")


window = Tk()
window.title("Mile to Km Converter")
window.minsize(width=300, height=300)

# Create the text box
input = Entry(width=10)
input.grid(column=10, row=2)

# Create a label for Miles
miles_label = Label(text="Miles", font=FONT)
miles_label.config(padx=20, pady=20)
miles_label.grid(column=11, row=2)

# Create a label for "is equal to"
equal_label = Label(text="is equal to", font=FONT)
equal_label.config(padx=10, pady=0)
equal_label.grid(column=1, row=3)

# Create a label to display the converted results
conversion_label = Label(text="0", font=FONT)
conversion_label.grid(column=10, row=3)

# Create a label for Km units
km_label = Label(text="Km", font=FONT)
km_label.config(padx=20, pady=20)
km_label.grid(column=11, row=3)

# Create a Calculate button
calculate_button = Button(text="Calculate", command=convert_miles_to_km)
calculate_button.grid(column=10, row=4)


window.mainloop()