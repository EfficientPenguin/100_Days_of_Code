'''
    This application implements the Hangman game from a preset word bank. It is 
    command-line driven.
'''

import random

num_tries = 5
word_list = ["aardvark", "baboon", "camel"]
WELCOME_PROMPT = "Welcome to the CLI Hangman game! A random word from the word list has been chosen.\n"

# Randomly choose a word from the word list
random_word = random.choice(word_list)
displayed_letters = ['_' for _ in range(len(random_word))]
playing = True

while(playing):
    print(f'\nTries left: {num_tries}\n')
    print(f'Hidden Word: {"".join(displayed_letters)}\n')

    # Ask the user to guess a letter and assign their
    user_letter = input("Type in a letter: ").lower()

    # Check if valid alphanumeric and len
    if len(user_letter) > 1:
        print('Too many letters!')
    elif not user_letter.isalpha():
        print('Not a letter!')
    # Check if the letter the user guessed is right or wrong
    elif user_letter in random_word:
        # fill in letters to displayed_letters
        for i in range(len(displayed_letters)):
            if user_letter == random_word[i]:
                displayed_letters[i] = user_letter
    else:
        num_tries -= 1

    if '_' not in displayed_letters:
        playing = False
        print(f'You Win! The hidden word was: {"".join(displayed_letters)}')
    elif num_tries == 0:
        playing = False
        print('You Lose')