"""
    This class implements the behaviors and functionality of the turtle that crosses the road.
"""

from turtle import Turtle
import direction

class Player(Turtle):
    def __init__(self, start_pos: tuple[float, float], step: int = 20):
        ''' Initialize the player as a turtle, set heading, and other attributes. '''
        super().__init__()
        # Initialize a turtle player
        # Have it start at the bottom of the screen
        self.color("green")
        self.penup()
        self.shape("turtle")
        self.setheading(direction.NORTH)
        self.speed("fastest")
        self.__step = step
        self.__start_pos = start_pos
        self.goto(self.__start_pos)

    def move(self) -> None:
        ''' Move the player forward by a preset amount.'''
        self.forward(self.__step)
    
    def reset_position(self) -> None:
        ''' Reset the player's position to their original starting position. '''
        self.goto(self.__start_pos)

    
