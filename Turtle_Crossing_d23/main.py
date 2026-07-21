"""
    This application implements a simple turtle crossing game. The player is a turtle that can only move forwards along a road
    where cars are coming from EAST -> WEST. If the turtle crosses the end of the road, then the turtle's position is reset
    back to the start, and the randomly generated cars have their speed increased to up the difficulty. The game ends when any car
    collides with the turtle.
"""
from turtle import Screen
import time

from Player import Player
from Car import Car
from Scorecard import Scorecard

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
PLAYER_START = (0.0, -SCREEN_HEIGHT/2 + 20)
PLAYER_STEP = 20

CAR_SPEED = 2
CAR_START_X = int(SCREEN_WIDTH/2) + 40
CAR_END_X = CAR_START_X + 2000
CAR_START_Y = -int(SCREEN_HEIGHT/2) + 80
CAR_END_Y = int(SCREEN_HEIGHT/2) - 40

# For init_pos
CAR_INIT_X = -int(SCREEN_WIDTH/2)

CAR_SPEED_ADD = 1
NUM_CARS = 50

GOAL_LINE = (0.0, SCREEN_HEIGHT/2 - 20)
SCORE_ORIGIN = (-SCREEN_WIDTH/2-20, SCREEN_HEIGHT/2-10)

def collided_with_car(player: Player, cars: list[Car]) -> bool:
    ''' Determines whether the player has collided with ANY car in the list of cars. '''
    player_pos = player.position()

    for car in cars:
        if car.distance(player) <= 25:
            return True
    
    return False

def main():
    # Create the screen
    screen = Screen()
    screen.screensize(canvwidth=SCREEN_WIDTH, canvheight=SCREEN_HEIGHT)
    screen.title("Turtle Crossing Game")
    screen.bgcolor("gray")
    screen.listen()
    screen.tracer(0)

    # Setup starting speeds / step sizes
    num_cars = NUM_CARS

    player = Player(start_pos=PLAYER_START, step=PLAYER_STEP)
    cars = [Car(x_start=CAR_START_X, x_end=CAR_END_X, y_start=CAR_START_Y, y_end=CAR_END_Y, step=CAR_SPEED) for _ in range(num_cars)]
    score = Scorecard(start_pos=SCORE_ORIGIN)

    # Randomize car positions
    [car.init_pos(x_start=CAR_INIT_X, x_end=CAR_END_X, y_start=CAR_START_Y, y_end=CAR_END_Y) for car in cars]

    # Game over text init
    game_over = Player((0.0, 0.0))
    game_over.hideturtle()
    game_over.pencolor("red")

    # Setup the event handlers for the player
    screen.onkey(fun=player.move, key="Up")

    # Game loop
    is_game_on = True

    screen.update()

    while is_game_on:
        # Move the cars
        [car.move() for car in cars]

        # Check if all cars crossed the left-most wall
        for car in cars:
            if car.xcor() <= -SCREEN_WIDTH/2-80:
                # Reset its position to right side of screen
                car.respawn()

        # Check if the player has crossed the goal line
        if player.ycor() >= GOAL_LINE[1]:
            # Clear current cars
            [car.init_pos(x_start=CAR_INIT_X, x_end=CAR_END_X, y_start=CAR_START_Y, y_end=CAR_END_Y) for car in cars]

            # Add another car to increase difficulty
            cars.append(Car(CAR_START_X, CAR_END_X, CAR_START_Y, CAR_END_Y, step=cars[0].get_speed()))

            # update the score
            score.update_score()

            # Increase the speed of the cars every 5 levels
            if score.score % 5 == 0:
                [car.update_speed(speed_add=CAR_SPEED_ADD) for car in cars]

            # reset player position
            player.reset_position()
        
        # Check if player collided with car
        if collided_with_car(player=player, cars=cars):
            # Game over screen
            is_game_on = False

        time.sleep(0.01)
        screen.update()
    
    # Game over
    game_over.write(f"Game Over!", False, "center", font=("Courier", 36, "normal"))

    screen.exitonclick()

if __name__ == "__main__":
    main()