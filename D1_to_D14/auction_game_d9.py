'''
    This application implements a simple auction simulator. The application
    gets input about the user such as name and price, then asks if there are other
    participants. It will keep adding them to a python dict, then calculate the
    winner when the user says no.
'''

def find_winner(participants: dict) -> str:
    winner = ''
    winner_price = 0

    for participant, value in participants.items():
        if value > winner_price:
            winner_price = value
            winner = participant
    
    return winner

def main():
    auction_done = False
    participants = {}

    while not auction_done:
        participant = input("What is your name? ")
        price = input("What is your bid? $")

        participants[participant] = float(price)

        if input("Add participants (Y/N): ").lower() == 'n':
            auction_done = True
    
    winner = find_winner(participants)
    print(f"The winner is {winner} for a price of ${participants[winner]}. Congrats!")

if __name__ == "__main__":
    main()