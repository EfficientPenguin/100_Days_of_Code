'''
    This application includes some challenges from d18 in the 100 days of code.
'''

from turtle import Turtle, Screen
import time

tim = Turtle()
tim.shape("turtle")
screen = Screen()
screen.colormode(255)

def get_random_color() -> int:
    import random
    return random.randint(0, 255)

# Challenge 1: Draw a square across the screen. Can go in any order
# Go >, v, <, ^
def challenge_1():
    for _ in range(4):
        tim.forward(100)
        tim.right(-90)

# Challenge 2: Draw a dashed line
def challenge_2():
    for _ in range(50):
        tim.pendown()
        tim.forward(10)
        tim.penup()
        tim.forward(10)

# Challenge 3: Draw a triangle, square, pentagon, hexagon, heptagon, octagon, nonagon, and decagon
# Each side's length = 100
def challenge_3():
    # Draw triangle
    num_sides = 3
    while num_sides < 11:
        # Set the pen color to something random
        tim.pencolor(get_random_color(), get_random_color(), get_random_color())
        for _ in range(num_sides):
            tim.forward(100)
            tim.right(360/num_sides)
        num_sides += 1

# Challenge 4: Random walk
def challenge_4():
    import random
    tim.hideturtle()
    tim.pensize(10)
    tim.speed("fastest")
    for _ in range(200):
        # Set the pen color to something random
        tim.pencolor(get_random_color(), get_random_color(), get_random_color())
        tim.right((random.randint(0,4)*90))
        tim.forward(20)

# Challenge 5: Make a Spirograph. Random colors and rotate circle around with radius = 100.
def challenge_5():
    # Rotate certain degrees
    # Select random color for pen
    # Draw circle
    # repeat
    tim.speed("fastest")
    tim.hideturtle()
    for degrees in range(0, 360, 6):
        tim.pencolor(get_random_color(), get_random_color(), get_random_color())
        tim.circle(100)
        tim.right(6)

# Call the challenge you want displayed
# challenge_1()
# challenge_2()
# challenge_3()
# challenge_4()
challenge_5()

screen.exitonclick()