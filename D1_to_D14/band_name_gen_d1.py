'''
    This file is for day 1 of the 100 days of code. It simply requests two inputs
    from the user and reports the suggested band name then terminates.
'''
GREETING = "Welcome to the Band Name Generator."
CITY_PROMPT = "What's teh name of the city you grew up in?\n "
PET_PROMPT = "What's your pet's name?\n "

def main():
    suggested_band_name = ""
    # Present greeting
    print(GREETING)

    # ask for the city
    suggested_band_name = input(CITY_PROMPT) + " "

    # ask for the pet
    suggested_band_name += input(PET_PROMPT)

    # report the suggested band name
    print("Your band name could be " + suggested_band_name)

if __name__ == "__main__":
    main()