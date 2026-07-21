"""
    This application implements the classic snake game with a basic score and wall-checking behavior.
    I could move the food into its own class that inherits from turtle like the day 21 showed.
    I could also create a Scorecard class to manage the score more easily -- perhaps display game over in the middle
    of the screen instead of just printing it out.
"""

from turtle import Turtle, Screen
from Snake import Snake
from Scoreboard import Scoreboard
import time
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SCORE_INIT_X = -150
SCORE_INIT_Y = int(SCREEN_HEIGHT/2)-40

def read_high_score(file: str="highscore.txt") -> int:
    ''' Reads a file containing the high score and returns the value.'''
    try:
        with open(file, mode="r") as file:
            for line in file:
                return int(line)
    except FileNotFoundError:
        print(f'"{file}" doesn\'t exist. Creating it and initalizing with high_score = 0...')
        write_high_score(high_score=0, file=file)

    return 0

def write_high_score(high_score: int, file: str="highscore.txt") -> None:
    ''' Write the high score to the file'''
    with open(file, mode="w") as file:
        file.write(str(high_score))

def get_rand_coord(dimension: int) -> int:
    num = random.randint((-int(dimension/2)+20), int(dimension/2)-20)
    # Adjust to make it in 20x20 granularity on the grid
    num -= (num%20)
    return num

def generate_random_food(screen_width: int = SCREEN_WIDTH, screen_height: int = SCREEN_HEIGHT) -> Turtle:
    """ Generate a random food on the screen with same default dimensions as a snake body part. """
    food = Turtle(shape="square")
    food.color("green", "green")
    food.penup()
    food.setposition(get_rand_coord(screen_width), get_rand_coord(screen_height))
    return food

def update_food_position(food: Turtle, snake: Snake) -> None:
    """ Function to move the food to a random position on the screen. It will keep moving the food if the random
        position generated overlaps with the snake body in any way. """
    rand_x = get_rand_coord(SCREEN_WIDTH)
    rand_y = get_rand_coord(SCREEN_HEIGHT)

    snake_positions = [(round(snake.body[i].xcor()), round(snake.body[i].ycor())) for i in range(len(snake.body))]

    # While the random coord is in the set of snake body part positions, keep generating a new x,y
    while (rand_x, rand_y) in snake_positions:
        rand_x = get_rand_coord(SCREEN_WIDTH)
        rand_y = get_rand_coord(SCREEN_HEIGHT)
    food.setposition(rand_x, rand_y)

def is_food_eaten(snake: Snake, food: Turtle) -> bool:
    """ Function to determine whether the food on the screen was eaten by the head of the snake. """
    if round(snake.xcor()) == round(food.xcor()) and round(snake.ycor()) == round(food.ycor()):
        return True
    return False

def is_wall_collision(snake: Snake) -> bool:
    """ Function to determine wall collisions. """
    # Get the had of the snake and its pos
    # If the pos of the head hits our screen boundaries, return True; else, False
    head = snake.body[0]

    if round(head.xcor()) <= -(int(SCREEN_WIDTH/2)) or round(head.xcor()) >= int(SCREEN_WIDTH/2):
        return True
    elif round(head.ycor()) <= -(int(SCREEN_WIDTH/2)) or round(head.ycor()) >= int(SCREEN_WIDTH/2):
        return True
    
    return False

# Screen setup
screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

# Challenge: Create the snake body consisting of 3 square segements each 20x20 with no gaps. Square must be white
snake = Snake()
score = Scoreboard(start_pos=(SCORE_INIT_X, SCORE_INIT_Y), score=0)

# Enable listen of events
screen.listen()

# Enable event handlers
screen.onkey(key="w", fun=snake.move_up)
screen.onkey(key="a", fun=snake.move_left)
screen.onkey(key="s", fun=snake.move_down)
screen.onkey(key="d", fun=snake.move_right)

is_game_on = True

# Create a random food
food = generate_random_food()

screen.update()

while is_game_on:
    snake.update_segments()
    snake.body[0].forward(20)
    screen.update()
    time.sleep(0.07)

    # Check for wall collisions
    if is_wall_collision(snake) or snake.is_body_collision():
        score.reset()
        snake.reset()

    # Check if we ate the food
    if is_food_eaten(snake.body[0], food):
        score.increase_score()
        update_food_position(food, snake)
        snake.add_segment()
    

# Report game stats
score.game_over()


screen.exitonclick()