"""
    Class to keep track of the score for the game.
"""

from turtle import Turtle

class Scorecard(Turtle):
    def __init__(self, start_pos: tuple[float, float], score: int=0):
        ''' Initialize the scorecard.'''
        super().__init__()
        self.hideturtle()
        self.penup()
        self.pencolor("black")
        self.speed("fastest")
        self.goto(start_pos)
        self.score = score
        self.write(f"Score: {self.score}", False, "left", font=("Courier", 24, "normal"))
    
    def update_score(self) -> None:
        ''' Update the score on the screen. '''
        self.clear()
        self.score += 1
        self.write(f"Score: {self.score}", False, "left", font=("Courier", 24, "normal"))