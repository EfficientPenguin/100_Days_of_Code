"""
    This class provides functionality for a paddle in the famous Pong game.
"""

from turtle import Turtle

NORTH = 90
SOUTH = 270
EAST = 0
WEST = 180

# Block step size of the paddle. Based on dimensions. Default is 20, since square is 20x20
STEP_SIZE = 20

class Paddle(Turtle):
    def __init__(self, pos: tuple[float, float], score_pos: tuple[float, float]):
        super().__init__()
        self.shape("square")
        self.shapesize(5,1,1)
        self.penup()
        self.color("white")
        self.speed("fastest")
        self.setposition(pos)
        self.y_move = 20
        self.score_as_num = 0
        self.init_score(score_pos)
    
    def move_up(self):
        """ Function to move the paddle up. """
        self.y_move = 20
        self.goto(self.xcor(), self.ycor() + self.y_move)
    
    def move_down(self):
        """ Function to move the paddle down. """
        self.y_move = -20
        self.goto(self.xcor(), self.ycor() + self.y_move)
    
    def init_score(self, score_pos: tuple[float, float]):
        self.score = Turtle()
        self.score.hideturtle()
        self.score.penup()
        self.score.pencolor("white")
        self.score.goto(score_pos)
        self.score.write(f"{self.score_as_num}", False, align="center", font=('Courier', 80, 'normal'))
    
    def update_score(self):
        self.score.clear()
        self.score_as_num += 1
        self.score.write(f"{self.score_as_num}", False, align="center", font=('Courier', 80, 'normal'))



