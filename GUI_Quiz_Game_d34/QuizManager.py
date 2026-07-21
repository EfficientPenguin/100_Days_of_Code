"""
    This class manages the questions to be used in a quiz format. By default there
    are 10 questions that must be used.
"""
import random
import requests
import json
import html

# Constants
QUESTIONS_FILE = "./questions.json"
QUIZ_SOURCE_URL = "https://opentdb.com/api.php?amount=10&type=boolean"

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
        self.__quiz = self.read_in_questions()
        self.__question_num = 0
        self.current_question = None
        self.__player_score = 0
        self.__total_score = len(self.__quiz)

    def read_in_questions(self) -> None:
        ''' Read in the questions using an API request using requests lib'''
        response = requests.get(url=QUIZ_SOURCE_URL)
        response.raise_for_status()

        data = response.json()['results']

        with open(file=QUESTIONS_FILE, mode="w") as file:
            json.dump(data, file, indent=4)
        
        # Create the quiz dict -- only get values we need
        fmt_dict = {}
        question_num = 0

        # Make sure we unescape the questions, since HTML source has it in different format than python (e.g., ', "", etc.)
        for el in data:
            fmt_dict[f'{question_num}'] = {
                'question': html.unescape(el['question']),
                'answer': el['correct_answer']
            }
            question_num += 1
        
        return fmt_dict

    def get_question_and_answer(self) -> dict:
        """ Pull a question at random from the quiz dict."""
        if len(self.__quiz.keys()) == 0:
            return {}
        
        question = random.choice(list(self.__quiz.keys()))
        self.__question_num += 1

        self.current_question = self.__quiz.pop(question)
        return self.current_question

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

    def update_player_score(self, is_correct_ans: bool) -> None:
        """ Updates the player's score internally. """
        if is_correct_ans:
            self.__player_score += 1
    
    def get_player_score(self) -> None:
        """ Get the player's current score. """
        return self.__player_score

    def get_total_score(self) -> None:
        """ Get the total score of quiz. """
        return self.__total_score