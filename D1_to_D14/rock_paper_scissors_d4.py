'''
    This application is a simple rock, paper, scissors game that the user plays
    with a computer. The user is tasked with inputting a number between 0-2.
    The computer's move is randomly generated and the result is then determined.
    Rock beats Scissors; Scissors beats Paper; and Paper beats Rock.
'''

import random

OPTIONS = set({0, 1, 2})
PROMPT = "What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n"
USER_WIN = "You Win!"
COMP_WIN = "Computer Wins. You lose!"
DRAW = "It's a draw!"

user_choice = int(input(PROMPT))

while user_choice not in OPTIONS:
    print('ERROR: Please select either 0, 1, or 2.\n')
    user_choice = int(input(PROMPT))

comp_choice = random.randrange(0,3,1)
print(f'Computer chose: {comp_choice}')

if user_choice == 0 and comp_choice == 2:
    print(USER_WIN)
elif comp_choice == 0 and user_choice == 2:
    print(COMP_WIN)
elif comp_choice > user_choice:
    print(COMP_WIN)
elif user_choice > comp_choice:
    print(USER_WIN)
elif user_choice == comp_choice:
    print(DRAW)