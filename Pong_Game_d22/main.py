"""
    This applicaiton implements the famous pong game. It's a bit more complicated than snake, since there
    are ball physics with angles, collision detection, and two players with their own paddles.
"""

from turtle import Turtle, Screen
from Paddle import Paddle, STEP_SIZE
from Ball import Ball
import time

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SOUTH_WALL = -int(SCREEN_HEIGHT/2)
NORTH_WALL = int(SCREEN_HEIGHT/2)
EAST_WALL = int(SCREEN_WIDTH/2)
WEST_WALL = -int(SCREEN_WIDTH/2)+20

def main():
    # Create the screen and dimensions. Set bg to black
    screen = Screen()
    screen.bgcolor("black")
    screen.screensize(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.title("Pong Game")
    screen.tracer(0)
    screen.listen()

    # Create the paddles
    l_paddle = Paddle(pos=(WEST_WALL+20, 0.0), score_pos=(-70, NORTH_WALL-60))
    r_paddle = Paddle(pos=(EAST_WALL-20, 0.0), score_pos=(70, NORTH_WALL-60))
    ball = Ball()

    screen.onkey(fun=l_paddle.move_up, key="w")
    screen.onkey(fun=l_paddle.move_down, key="s")
    screen.onkey(fun=r_paddle.move_up, key="Up")
    screen.onkey(fun=r_paddle.move_down, key="Down")

    while(1):
        time.sleep(0.1)
        ball.move()

        # Detect collision with wall
        if ball.ycor() > NORTH_WALL+20 or ball.ycor() < SOUTH_WALL-20:
            ball.bounce_y()
  
        # Collision with r_paddle or l_paddle
        if ball.distance(r_paddle) < 50 and ball.xcor() > EAST_WALL-40 or ball.distance(l_paddle) < 50 and ball.xcor() < WEST_WALL+40:
            ball.bounce_x()

        # Detect out of bounds condition: one player gets the point
        if ball.xcor() <= WEST_WALL-30:
            r_paddle.update_score()
            ball.reset_ball()
        elif ball.xcor() >= EAST_WALL+30:
            l_paddle.update_score()
            ball.reset_ball()

        screen.update()


    # Prevent screen from closing until user clicks the screen or exits the application via X
    screen.exitonclick()

if __name__ == "__main__":
    main()