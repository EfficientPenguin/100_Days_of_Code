'''
    This application converts a simple string into a list of NATO words corresponding to each
    letter in the given string.
'''

import pandas

def main():
    # Ask for a string from the user
    word = input("Enter a word: ").lower()

    # Create the list using list comprehension
    # Look up the letter in the NATO alphabet
    nato = pandas.read_csv("NATO_alphabet.csv")

    # Create a dict of the nato alphabet by using dict comprehension on the read-in DataFrame nato
    nato_dict = {row.character:row.word for (index,row) in nato.iterrows()}
    
    # Create the list of nato words for each char in the input word from user
    chars_as_nato = [nato_dict[char] for char in word if char in nato_dict.keys()]

    print(chars_as_nato)

    

if __name__ == "__main__":
    main()