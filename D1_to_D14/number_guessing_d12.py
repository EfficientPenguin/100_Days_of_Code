'''
    This application implements a number guessing game.
'''

import random

def number_guessing():
    # Initialize game and print prompts
    tries = 0
    number = random.randint(1, 100)

    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print(f"Pssst, the correct answer is {number}.")
    mode = input("Choose a difficulty. Type 'easy' or 'hard': ")

    # Set tries depending on easy or hard
    if mode == 'easy':
        tries = 5
    else:
        tries = 10

    # Get the guess from the user
    guess = int(input("Make a guess: "))

    while guess != number and tries > 0:
        tries -= 1
        print(f'Too {"high" if guess > number else "low"}.')
        print(f'You have {tries} attempts remaining to guess the number.')
        guess = int(input("Make a guess: "))
    
    if tries == 0:
        print('Out of attempts!')
    else:
        print('Congrats! You win!')
    print(f'The number was {number}.')

def main():
    number_guessing()

if __name__ == "__main__":
    main()
        