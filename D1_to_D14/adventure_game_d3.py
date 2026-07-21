'''
    This application is a small adventure game that is filled with decisions
    at every turn that the user must make. The goal is to get to the treasure.
'''

WELCOME = 'Welcome to Treasure Island.\nYour mission is to find the treasure.'
DIRECTION_PROMPT = 'Would you like to go "left" or "right"? '
SWIM_PROMPT = 'Would you like to "swim" or "wait"? '
DOOR_PROMPT = 'Which door: (red, blue, or yellow)? '
WIN = 'You Win!'
GAME_OVER = 'Game Over.'

if input(DIRECTION_PROMPT).lower() == "left":
    if input(SWIM_PROMPT).lower() == "wait":
        door = input(DOOR_PROMPT).lower()
        if door == "yellow":
            print(WIN)
        elif door == "red":
            print('Burned by fire.\n' + GAME_OVER)
        elif door == "blue":
            print('Eaten by beasts.\n' + GAME_OVER)
        else:
            print(GAME_OVER)
    else:
        print('Attacked by trout.\n' + GAME_OVER)
else:
    print('Fall into hole.\n' + GAME_OVER)