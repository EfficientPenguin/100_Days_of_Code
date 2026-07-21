"""
    This class manages the questions to be used in a quiz format. By default there
    are 10 questions that must be used.
"""
import random

DEFAULT_QUIZ = {
    1 : {
        "question": "The first computer bug was formed by faulty wires.",
        "answer": False
    },
    2 : {
        "question": "FLAC stands for 'Free Lossless Audio Condenser.",
        "answer": False
    },
    3 : {
        "question": "All program codes have to be compiled into an executable file in order to run. This file can then be executed on any machine.",
        "answer": False
    },
    4 : {
        "question": "The HTML5 standard was published in 2014.",
        "answer": True
    },
    5 : {
        "question": "Linus Torvalds created Linux and Git.",
        "answer": True
    },
    6 : {
        "question": "The programming language 'Python' is based off a modified version of 'JavaScript'.",
        "answer": False
    },
    7 : {
        "question": "AMD created the first consumer 64-bit processor.",
        "answer": True
    },
    8 : {
        "question": "'HTML' stands for Hypertext Markup Language.",
        "answer": True
    },
    9 : {
        "question": "In most programming languages, the operator ++ is equivalent to the statement '+= 1'.",
        "answer": True
    },
    10 : {
        "question": "The IBM PC used an Intel 8008 microprocessor clocked at 4.77 MHz and 8 kilobytes of memory.",
        "answer": False
    },
}

class QuizManager():
    def __init__(self, quiz: dict = DEFAULT_QUIZ):
        self.__quiz = dict(quiz)
        self.__question_num = 0

    def get_question_and_answer(self) -> dict:
        """ Pull a question at random from the quiz dict."""
        if len(self.__quiz.keys()) == 0:
            return {}
        
        question = random.choice(list(self.__quiz.keys()))
        self.__question_num += 1

        return self.__quiz.pop(question)

    def is_correct_answer(self, player_ans: str, correct_answer: str) -> bool:
        """ Check the player's answer compared to the correct response. Return true if match; else, false."""
        if player_ans != correct_answer:
            return False

        return True
    
    def format_correct_answer(self, question_ans: dict) -> str:
        """ Function to format the correct answer to the question as a str instead of a bool. """
        return 'true' if question_ans['answer'] else 'false'
    
    def print_results(self, is_correct_ans: bool, question_ans: dict) -> None:
        if is_correct_ans:
            print("You got it right!")
        else:
            print("That's wrong.")
        print(f"The correct answer was: {'True' if question_ans['answer'] else 'False'}.")

    def get_player_ans(self, question_ans: dict) -> str:
        """ Get the player's response from the command line. """
        return input(f"\nQ.{self.__question_num}: {question_ans['question']} (True/False): ").lower()