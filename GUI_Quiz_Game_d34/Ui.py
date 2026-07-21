'''
    This implements the Tkinter GUI front-end logic for the Quiz application that I coded up on day 17.
'''

from tkinter import *
from QuizManager import QuizManager

FONT = ('Arial', 20, 'italic')

class QuizGui():
    def __init__(self, quiz_manager: QuizManager):
        self.quiz_manager = quiz_manager
        self.player_score = 0
        self.total_score = 0
        self.timer = None

        self.window = Tk()
        self.window.title('Quizzler')
        self.window.config(padx=20, pady=20)
        self.window.config(background='DeepSkyBlue4')

        # Create the canvas
        self.canvas = Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.question_text = self.canvas.create_text(
            150, 
            125,
            width=280,
            text="Some Question Text.", 
            fill='black', font=FONT)
        self.canvas.grid(column=0,row=1, columnspan=2, pady=50)

        # Create the True button
        self.check_button = Button(text='✅', highlightthickness=0, command=self.__check_button_handler)
        self.check_button.grid(column=0,row=2)

        # Create the False button
        self.false_button = Button(text='❌', highlightthickness=0, command=self.__false_button_handler)
        self.false_button.grid(column=1,row=2)

        # Create the Score text in upper right-hand corner
        self.score_text = Label(text=f'Score: {0}')
        self.score_text.grid(column=1,row=0)

        self.get_next_question()

        self.window.mainloop()
    
    def __check_button_handler(self) -> None:
        ''' User's answer is "True", so check answer.'''
        self.update_gui(player_ans='True')

    def __false_button_handler(self) -> None:
        ''' User's answer is "False", so check answer.'''
        self.update_gui(player_ans='False')

    def get_next_question(self) -> None:
        ''' Get the next quiz question from the quiz manager. '''
        self.canvas.config(bg="white")
        question = self.quiz_manager.get_question_and_answer()

        if question != {}:
            self.canvas.itemconfig(self.question_text, text=question['question'])
        else:
            self.canvas.itemconfig(self.question_text, text=f'You finished the quiz!\n\
                                   You got {self.quiz_manager.get_player_score()}/{self.quiz_manager.get_total_score()}')
            # Disable the buttons
            self.check_button.config(state="disabled")
            self.false_button.config(state="disabled")
    
    def update_gui(self, player_ans: str) -> None:
        ''' Updates the GUI based on the player's answer input. '''
        # Check if it's right, tally the scores, and repeat
        is_correct_ans = self.quiz_manager.is_correct_answer(player_ans=player_ans, correct_answer=self.quiz_manager.current_question['answer'])
        self.quiz_manager.update_player_score(is_correct_ans=is_correct_ans)

        self.score_text.config(text=f'Score: {self.quiz_manager.get_player_score()}')

        # Print the current results
        self.canvas.config(bg="Green" if is_correct_ans else "Red")
        self.canvas.itemconfig(self.question_text, text=f'You got it right!' if is_correct_ans else 'Wrong answer!')

        # Get a new question and repeat
        self.timer = self.window.after(1000, func=self.get_next_question)

if __name__ == "__main__":
    quiz_manager = QuizManager()
    quiz_gui = QuizGui(quiz_manager=quiz_manager)