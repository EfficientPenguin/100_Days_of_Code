'''
    This application implements a simple 10 question quiz game.
'''
import Player
import QuizManager

def main():
    # Build up the player and question manager objects
    player = Player.Player()
    quiz_manager = QuizManager.QuizManager()
    is_correct_ans = False

    # Get a question and answer pair to begin the quiz
    quiz = quiz_manager.get_question_and_answer()

    while(quiz != {}):
        # Present question and get the player's answer
        player_ans = quiz_manager.get_player_ans(quiz)
        correct_ans = quiz_manager.format_correct_answer(quiz)

        # Check if it's right, tally the scores, and repeat
        is_correct_ans = quiz_manager.is_correct_answer(player_ans, correct_ans)

        if is_correct_ans:
            player.update_score()
        player.update_total_score()

        # Print the current results
        quiz_manager.print_results(is_correct_ans, quiz)
        player.print_current_score()

        # Get a new question and repeat
        quiz = quiz_manager.get_question_and_answer()
    
    player.print_final_score()

if __name__ == "__main__":
    main()