"""
    Class to keep track of the score for the snake game.
"""
from turtle import Turtle

FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self, start_pos: tuple[int, int], score: int=0):
        ''' Initialize the scoreboard with attributes.'''
        super().__init__()
        self.__score = score
        try:
            with open("highscore.txt", mode="r") as file:
                for line in file:
                    self.__high_score = int(line)
        except FileNotFoundError:
            print(f'"highscore.txt" doesn\'t exist. Creating it and initalizing with high_score = 0...')
            with open(file, mode="w") as file:
                file.write("0")
            self.__high_score = 0
        self.hideturtle()
        self.penup()
        self.color("white")
        self.speed("fastest")
        self.goto(start_pos)
        self.update_scoreboard()
    
    def reset(self):
        ''' Update the high score and display. '''
        if self.__score > self.__high_score:
            self.__high_score = self.__score
                    
            # Write new high score to file
            with open("highscore.txt", mode="w") as file:
                file.write(f"{self.__high_score}")
                
        self.__score = 0
        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        ''' Update the scoreboard. '''
        self.clear()
        self.write(f"Score: {self.__score} High Score: {self.__high_score}", False, font=FONT)

    def increase_score(self) -> None:
        ''' Update the score attribute by 1 and write score to screen.'''
        self.__score += 1
        self.update_scoreboard()

    def game_over(self) -> None:
        ''' Display the game over text. '''
        self.goto((-60, 0.0))
        self.write(f"Game Over!", False, font=FONT)
    
    def get_high_score(self) -> int:
        ''' Return the high score attribute. '''
        return self.__high_score
