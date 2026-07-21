'''
    This class implements the attributes and behaviors for a Car that randomly gets placed on the screen.
'''
from turtle import Turtle
import random

import direction

COLORS = ["red", "blue", "purple", "yellow", "orange"]

class Car(Turtle):
    def __init__(self, x_start: int, x_end: int, y_start: int, y_end: int, step: int = 20):
        ''' Initialize a car. '''
        super().__init__()
        self.penup()
        self.speed("fastest")
        self.shape("square")
        self.shapesize(1.0, 2.0, 1.0)
        self.color(random.choice(COLORS))
        self.__step = step

        self.setheading(direction.WEST)
        self.__x_start = x_start
        self.__x_end = x_end
        self.__y_start = y_start
        self.__y_end = y_end

        self.respawn()
    
    def respawn(self) -> None:
        ''' Respawn the car at a random (x,y) within its initial outer boundary range'''
        rand_x = random.randint(self.__x_start, self.__x_end)
        rand_y = random.randint(self.__y_start, self.__y_end)

        self.goto((rand_x, rand_y))

    def init_pos(self, x_start: int, x_end: int, y_start: int, y_end) -> None:
        ''' Initialize the starting position of the car at some random (x,y). '''
        rand_x = random.randint(x_start, x_end)
        rand_y = random.randint(y_start, y_end)

        self.goto((rand_x, rand_y))
    
    def update_speed(self, speed_add: int):
        ''' Update the speed of the car, which is equivalent to its step attribute. '''
        self.__step += speed_add
    
    def get_speed(self) -> int:
        ''' Return the speed attribute. '''
        return self.__step

    
    def move(self):
        ''' Move the car'''
        self.forward(self.__step)
