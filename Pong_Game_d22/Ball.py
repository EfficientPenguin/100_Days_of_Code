"""
    This class implements the behavior and functionality of the ball.
"""
from turtle import Turtle
import random

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(1, 1, 1)
        self.penup()
        self.color("white", "white")
        self.speed("fastest")
        self.setheading(random.randint(a=0, b=360))
        self.x_move = 10
        self.y_move = 10
    
    def move(self):
        # Check if we hit any of the walls or a paddle
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto((new_x, new_y))
    
    def bounce_y(self):
        """ Bounce the ball when it collides with something in y."""
        self.y_move *= -1.1
    
    def bounce_x(self):
        """ Bounce the ball when it collides with something in x."""
        self.x_move *= -1.1

    def reset_ball(self):
        self.setposition((0.0, 0.0))
        if self.x_move >= 0:
            self.x_move = 10
        else:
            self.x_move = -10
        if self.y_move >= 0:
            self.y_move = 10
        else:
            self.y_move = -10
        self.bounce_x()
        self.bounce_y()
