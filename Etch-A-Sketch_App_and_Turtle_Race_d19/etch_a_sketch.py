"""
    This application implements an etch-a-sketch like the old game.
"""

from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()

# Challenge: Create an etch-a-sketch game
# W = forwards
# S = backwards
# A = counter-clockwise
# D = clockwise
# C = clear drawing

def move_forwards():
    tim.forward(10)

def move_backwards():
    tim.backward(10)

def move_counter_cw():
    tim.left(10)

def move_cw():
    tim.right(10)

def clear_screen():
    tim.reset()

screen.listen()
screen.onkey(key="w", fun=move_forwards)
screen.onkey(key="s", fun=move_backwards)
screen.onkey(key="a", fun=move_counter_cw)
screen.onkey(key="d", fun=move_cw)
screen.onkey(key="c", fun=clear_screen)

screen.exitonclick()