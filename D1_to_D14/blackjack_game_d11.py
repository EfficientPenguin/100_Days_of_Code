'''
    This application implements the card game blackjack with a simple CLI. It doesn't incorporate any betting.
'''

# Rules:
# First to 21 wins.
# If you go over, then computer tries to get a higher number than you or push to 21.
# At start, you are given two cards with the option to get another card or stand down.
# You are shown 1 card from the computer.

import random
from collections import Counter

ascii_art = """
 _     _            _    _            _    
| |   | |          | |  (_)          | |   
| |__ | | __ _  ___| | ___  __ _  ___| | __
| '_ \\| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
| |_) | | (_| | (__|   <| | (_| | (__|   < 
|_.__/|_|\\__,_|\\___|_|\\_\\ |\\__,_|\\___|_|\\_\\
                       _/ |                
                      |__/           
"""

win_ascii = """
 __   __           __        ___       _ 
 \\ \\ / /__  _   _  \\ \\      / (_)_ __ | |
  \\ V / _ \\| | | |  \\ \\ /\\ / /| | '_ \\| |
   | | (_) | |_| |   \\ V  V / | | | | |_|
   |_|\\___/ \\__,_|    \\_/\\_/  |_|_| |_(_)
"""

lose_ascii = """
 __   __            _                   _ 
 \\ \\ / /__  _   _  | |    ___  ___  ___| |
  \\ \\V / _ \\| | | | | |   / _ \\/ __|/ _ \\ |
   | | (_) | |_| | | |__| (_) \\__ \\  __/_|
   |_|\\___/ \\__,_| |_____\\___/|___/\\___(_)
"""

# Create the deck. A deck has 52 cards with 4 suits for each card. 1-10, then J, Q, K, A.
face_card_map = {
    'A': 11,
    'K': 10,
    'Q': 10,
    'J': 10
}

DEFAULT_DECK = 4*[i for i in range(1,11)]
DEFAULT_DECK.extend(4*[key for key in face_card_map])

NUM_TO_WIN = 21

def draw_card(deck: list, hand: list) -> None:
    '''
        Draws a card from the deck. Can return either be a str if face card or an int if num card.
    '''
    card = deck.pop()
    hand.append(card)

def calc_sum(cards_in_hand: list) -> int:
    ''' Function to calculate the sum of the cards in the hand.
    '''
    calc_sum = 0

    for card in cards_in_hand:
        if card in face_card_map:
            calc_sum += face_card_map[card]
        else:
            calc_sum += card

    return adjust_sum_for_aces(cards_in_hand, calc_sum) 

def adjust_sum_for_aces(cards_in_hand: list, calculated_sum: int) -> int:
    ''' Function to handle any aces in the hand. Find the max
        value that does NOT exceed 21. If multiple aces, then keep
        subtracting 10.
    '''
    if calculated_sum > NUM_TO_WIN:
        temp_hand = list(cards_in_hand)
        while 'A' in temp_hand:
            calculated_sum -= 10
            temp_hand.remove('A')
            if calculated_sum <= NUM_TO_WIN:
                return calculated_sum
    
    return calculated_sum

def is_bust(cards_in_hand: list) -> bool:
    ''' Function to determine whether the calculated sum has exceeded the blackjack rule of 21.
    '''
    if calc_sum(cards_in_hand) > NUM_TO_WIN:
        return True
    return False

def is_win(cards_in_hand: list) -> bool:
    ''' Function to determine if the current hand has won by achieving a sum of 21.
    '''
    if calc_sum(cards_in_hand) == NUM_TO_WIN:
        return True

    return False

def is_greater_hand(usr: list, com: list) -> bool:
    ''' Function to determine if the computer has a greater hand than the usr.
        Returns True if com has greater hand; else, False.
    '''
    if calc_sum(com) > calc_sum(usr):
        return True
    return False

def init_game(deck: list, player: list, computer: list) -> list:
    ''' Function to initialize the game at start. Create a new deck, shuffle it, create initial hands.
        Return the current deck after initial game setup.
    '''
    print(ascii_art)

    # Reset the deck and player and computer hands
    deck.clear()
    player.clear()
    computer.clear()

    # Create and shuffle the deck
    deck.extend(list(DEFAULT_DECK))
    random.shuffle(deck)

    # Initialize usr and com hands
    draw_card(deck, player)
    draw_card(deck, player)
    draw_card(deck, computer)
    draw_card(deck, computer)

    # Print out initial hands
    print_init_hands(player, computer)

    # Return the deck to use for the remainder of the game
    return deck

def print_init_hands(player: list, computer: list) -> None:
    ''' Function to print out the initial hands at the start of the game.
    '''
    print(f"Your cards: {player}")
    print(f"Computer's first card: {computer[0]}")

def print_results(player: list, computer: list, player_wins: bool) -> None:
    ''' Function to print out the results of the game.
    '''
    print(f"Your final hand: {player}")
    print(f"Computer's final hand: {computer}")

    if player_wins:
        print(win_ascii)
    else:
        print(lose_ascii)

def main():
    deck = []
    usr_hand = []
    com_hand = []
    keep_playing = True

    while keep_playing:
        is_player_wins = False
        is_player_bust = False
        init_game(deck=deck, player=usr_hand, computer=com_hand)

        while not is_player_wins and not is_player_bust and \
            input("Type 'y' to get another card, type 'n' to pass: ").lower() == 'y':
            # Draw a card, determine if player busts or gets to 21
            draw_card(deck, usr_hand)
            if is_bust(usr_hand):
                is_player_bust = True
            elif is_win(usr_hand):
                is_player_wins = True
            print(f"Your hand: {usr_hand}")

        if is_player_bust or is_player_wins:
            print_results(usr_hand, com_hand, is_player_wins)
        else:
            while not is_greater_hand(usr_hand, com_hand):
                draw_card(deck, com_hand)
                if is_bust(com_hand):
                    is_player_wins = True
                    break

            print_results(usr_hand, com_hand, is_player_wins)

        if input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower() != 'y':
            keep_playing = False

    print("Exiting the application... Thanks for playing!")
if __name__ == "__main__":
    main()
