''' This application implements a higher lower game, where the user is presented with two entities
    whoe are either celebrities, musicians, actors/actresses, businesses, etc. The goal is to guess which
    entity has more followers. Each correct answer earns the player 1 point, and the correct answer becomes the option A
    while a new option B is fetched from a dictionary at random. The player loses if they guess incorrectly. The total
    score is reported at the end.
'''

# import from the random library to generate a random number
import random

# create the dictionary to pull options from
data = [
    {
        'name': 'Instagram',
        'follower_count': 346,
        'description': 'Social media platform',
        'country': 'United States'
    },
    {
        'name': 'Cristiano Ronaldo',
        'follower_count': 215,
        'description': 'Footballer',
        'country': 'Portugal'
    },
    {
        'name': 'Ariana Grande',
        'follower_count': 183,
        'description': 'Musician and actress',
        'country': 'United States'
    },
    {
        'name': 'Dwayne Johnson',
        'follower_count': 181,
        'description': 'Actor and professional wrestler',
        'country': 'United States'
    },
    {
        'name': 'Selena Gomez',
        'follower_count': 174,
        'description': 'Musician and actress',
        'country': 'United States'
    },
    {
        'name': 'Kylie Jenner',
        'follower_count': 172,
        'description': 'Reality TV personality and businesswoman and Self-Made Billionaire',
        'country': 'United States'
    },
    {
        'name': 'Kim Kardashian',
        'follower_count': 167,
        'description': 'Reality TV personality and businesswoman',
        'country': 'United States'
    },
]

# Print functions to report the current two options being compared in the vs.
def print_entity_details(entity: dict, is_option_A: bool) -> None:
    ''' Prints the details of the entity such as name, description, and country
    '''
    if entity:
        print(f'Compare {'A' if is_option_A else 'B'}: {entity['name']}, a {entity['description']}, from {entity['country']}.')
    else:
        print('Error printing entity!')

# Implement checker function to compare the two options' follower count and return the one with a greater
# num of followers
def get_higher_followers(a: dict, b: dict) -> str:
    if a['follower_count'] > b['follower_count']:
        return 'a'
    return 'b'

# Implement function to get user's choice: A or B
def get_user_option() -> str:
    choice = input("Who has more followers? Type 'A' or 'B': ").lower()

    if choice != 'a':
        return 'b'
    return choice

# Function to get option at random from the data list
def get_entity_from_data(data: list[dict]) -> dict:
    # Edge case: if list is empty, user wins. Return None
    if len(data) == 0:
        return None
    
    # Generate a random int within the length of data
    index = random.randint(0, len(data)-1)

    # Copy the data into a variable
    entity = dict(data[index])

    # Remove the data from the data list
    data.remove(data[index])

    # Return the entity
    return entity

def play_game() -> None:
    # Keep track of the current user score
    usr_score = 0
    is_usr_win = True

    # Setup the game: Fetch two options from the data dict at random
    option_A = get_entity_from_data(data)
    option_B = get_entity_from_data(data)

    # Keep playing until user loses or wins
    while option_B:
        print_entity_details(entity=option_A, is_option_A=True)
        print('VS')
        print_entity_details(entity=option_B, is_option_A=False)

        usr_option = get_user_option()

        if usr_option == get_higher_followers(option_A, option_B):
            option_A = option_B
            option_B = get_entity_from_data(data)
            usr_score += 1
        else:
            is_usr_win = False
            break
    
    if is_usr_win:
        print(f'You Win! ', end='')
    else:
        print(f'Sorry, that\'s wrong. ', end='')
    print(f'Final score: {usr_score}')

def main():
    play_game()

if __name__ == "__main__":
    main()