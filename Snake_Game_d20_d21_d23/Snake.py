"""
    This class implements the functionality for maintaining, creating, the snake body parts and head.
"""
from turtle import Turtle, Screen

class Snake():
    def __init__(self, start: tuple[float, float] = (0.0, 0.0)):
        self.create_body(start)
    
    def create_body(self, start: tuple[float, float] = (0.0, 0.0)) -> list[Turtle]:
        # Create the head
        self.body = []
        position = start

        for i in range(0, 3):
            segment = Turtle(shape="square")
            segment.color("white", "white")
            segment.penup()
            segment.speed("fastest")
            segment.setposition(position)
            position = (position[0]-20.0, position[1])
            self.body.append(segment)
    
    def move_up(self) -> None:
        """ Move the snake according to the key pressed: W, A, S, D. """
        # Change heading of head
        self.body[0].setheading(90)

    def move_down(self) -> None:
        """ Move the snake according to the key pressed: W, A, S, D. """
        # Change heading of head
        self.body[0].setheading(270)
    
    def move_left(self) -> None:
        """ Move the snake according to the key pressed: W, A, S, D. """
        # Change heading of head
        self.body[0].setheading(180)

    def move_right(self) -> None:
        """ Move the snake according to the key pressed: W, A, S, D. """
        # Change heading of head
        self.body[0].setheading(0)
    
    def add_segment(self) -> None:
        """ Function to add a segment to the snake after eating food. """
        new_tail = Turtle(shape="square")
        new_tail.color("white", "white")
        new_tail.penup()
        new_tail.speed("fastest")
        old_tail_pos = self.body[-1].position()
        new_tail.setposition((old_tail_pos[0]-20, old_tail_pos[1]))
        self.body.append(new_tail)
    
    def update_segments(self):
        """ Update the segments after the head has moved. Use head_pos to update the remaining segments' positions. """
        # Move the body parts in tandem
        for segment in range(len(self.body)-2, -1, -1):
            head_pos = self.body[segment].position()
            self.body[segment+1].setposition(head_pos)

    def is_body_collision(self):
        """ Function to True if the head of the snake collides with any portion of the body. """
        # Get the head pos
        head_x = round(self.body[0].xcor())
        head_y = round(self.body[0].ycor())

        # Compare it to each body part
        for segment in range(1, len(self.body)):
            segment_x = round(self.body[segment].xcor())
            segment_y = round(self.body[segment].ycor())

            if head_x == segment_x and head_y == segment_y:
                return True

        return False

    def reset(self) -> None:
        ''' Clear all of the segments. '''
        position = (0.0, 0.0)
        self.body[0].setheading(0)
        for segment in self.body:
            segment.goto(-1000, -1000)
            segment.clear()
        self.body = self.body[0:3]

        for segment in self.body:
            segment.goto(position)
            position = (position[0]-20, position[1])
