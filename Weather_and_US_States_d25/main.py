'''
    This application reads in the weather data from weather.csv and places them in a list for futher
    processing. The other half of the day was spent on creating a US state guessing game, where the user enters
    a state, and if they guess one that's correct
    then the game will write the state name on the state itself. The game ends when the user guesses all of the states.
    The remaining states are printed out after every correct guess for quick testing/lookup.
'''
import csv
import pandas
import turtle
from State import State

def squirrel_data_processing():
    # Read in the data line by line into a data list
    data = []

    with open("weather.csv") as data_file:
        data = csv.reader(data_file)
        temperatures = []
        for row in data:
            print(row)
            if row[1] != 'temp':
                temperatures.append(int(row[1]))
        
        print(temperatures)

    data = pandas.read_csv("weather.csv")

    # Challenge: Calculate the average temperature in the list of temps
    temp_list = data['temp']

    print(f"Avg temp: {temp_list.mean():0.2f}")
    print(f"Max temp: {temp_list.max()}")

    # Challenge: Pull out weather data (i.e., the full row) where temp was at its maximum
    print(data[data.temp == data.temp.max()])

    monday = data[data.day == "Monday"]
    print(f"{monday.temp[0] * 9/5 + 32}F")

    # Read in the squirrel data
    data = pandas.read_csv("2018_squirrel_data.csv")

    # Create a squirrel_count.csv that has Fur Color and Count columns
    # First extract the fur color data from teh data
    gray = len(data[data["Primary Fur Color"] == "Gray"])
    red = len(data[data["Primary Fur Color"] == "Cinnamon"])
    black = len(data[data["Primary Fur Color"] == "Black"])

    print(gray)
    print(red)
    print(black)

    squirrels_dict = {
        "Fur Color": ["Gray", "Red", "Black"],
        "Count": [gray, red, black]
    }

    squirrel_df = pandas.DataFrame(squirrels_dict)
    squirrel_df.to_csv("squirrel_count.csv")

def states_game():
    ''' Implement the states guessing game from day 25. '''
    screen = turtle.Screen()
    screen.title("U.S. States Game")
    image = "resized_USA_empty_map.gif"
    screen.addshape(image)
    turtle.shape(image)

    screen.tracer(0)

    state_writer = State()

    # Read in the states as a dataframe
    df = pandas.read_csv("states.csv")
    states_list = df.state.to_list()
    states_correct = 0
    total_states = len(states_list)

    while len(states_list) > 0:
        answer_state = screen.textinput(title=f"{states_correct}/{total_states} States Correct", prompt="What's another state's name?").title()
        if answer_state in states_list:
            row = df[df.state == answer_state]

            state_writer.write_state(answer_state, (row.x.item(), row.y.item()))

            states_list.remove(answer_state)
            states_correct += 1
            print(f"States remaining: {states_list}")
        screen.update()


    # Only way we get here is if player guesses them all
    state_writer.write_state("Congrats, you got 'em all!", state_pos=(-150, 250), font=("Arial", 30, "normal"))
    turtle.mainloop()

if __name__ == "__main__":
    # squirrel_data_processing()
    states_game()