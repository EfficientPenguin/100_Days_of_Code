"""
    This application implements a simple turtle racing game. The user is prompted to enter a turtle's color who they
    believe will win the race. The application then runs the game and determines the first turtle to cross to the end
    as the winner.
"""

from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)

user_bet = screen.textinput(title="Turtle Race Game", prompt="Who will win the race? Enter a color: ").lower()
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [x for x in range(-90, 90, 30)]
# Create 6 turtles at start of race
turtles = {}

for turtle_index in range(0, 6):
    turtle = Turtle(shape="turtle")
    turtle.color(colors[turtle_index])
    turtle.penup()
    turtle.goto(x=-230, y=y_positions[turtle_index])
    turtles[colors[turtle_index]] = turtle

is_race_on = False
winning_turtle = ''

if user_bet:
    is_race_on = True

while is_race_on:
    # Check if there's a winner by checking all turtle positions
    for color in turtles:
        if int(turtles[color].pos()[0]) == 230:
            winning_turtle = color
            is_race_on = False
            break
    if winning_turtle:
        print(f"{winning_turtle} wins! {"You win!" if winning_turtle == user_bet else "You Lose!"}")

    # Move a random turtle forward
    color_to_move = random.choice(list(turtles.keys()))

    # Move the turtle forward
    turtles[color_to_move].forward(5)


screen.exitonclick()