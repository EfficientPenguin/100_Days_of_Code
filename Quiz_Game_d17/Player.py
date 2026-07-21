"""
    This class defines the Player which has a current score attribute and a few
    methods for managing the score.
"""

class Player():
    def __init__(self):
        self.__score = 0
        self.__total_score = 0
    
    def get_score(self) -> int:
        return self.__score
    
    def update_score(self) -> None:
        self.__score += 1
    
    def get_total_score(self) -> int:
        return self.__total_score
    
    def update_total_score(self) -> None:
        self.__total_score += 1

    def print_current_score(self) -> None:
        print(f"Your current score is: {self.get_score()}/{self.get_total_score()}")
    
    def print_final_score(self) -> None:
        print("\nYou've completed the quiz.")
        print(f"Your final score is: {self.get_score()}/{self.get_total_score()}")
    