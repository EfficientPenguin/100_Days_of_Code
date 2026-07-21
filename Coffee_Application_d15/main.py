'''
    This application implements a simple virtual coffee machine. The user can select a coffee type from a 
    displayed menu, and the coffee machine can make the coffee for them. The coffee machine is coin
    operated, and it is capable of reporting its current resources (e.g., amount of water, milk, etc.).
    This is a direct implementation of the 100 days of code by Dr. Angela Yu course on Udemy, day 15.
'''

# dict of items on the menu. "off" is used to indicate the intention to shut off the machine.
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

# Dict to maintain default resources of the coffee machine
DEFAULT_RESOURCES = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0.0
}

# Create a coin hash map
COIN_MAP = {
    "quarter": 0.25,
    "dime": 0.10,
    "nickle": 0.05,
    "penny": 0.01,
}

class CoffeeMachine():
    def __init__(self, resources: dict):
        self.resources = dict(resources)
        self.is_on = True

    # Prompt user by asking "What would you like? (espresso/latte/cappuccino):"
    def get_drink_selection(self) -> str:
        drink = input("What would you like? (espresso/latte/cappuccino): ").lower()

        # Error checking. Keep requesting a drink until valid choice. NOTE: 'off' and 'report' are secret words for
        # maintainer of the coffee machine.
        while drink not in MENU.keys() and drink != 'off' and drink != 'report':
            print("Invalid option!")
            drink = input("What would you like? (espresso/latte/cappuccino): ").lower()

        return drink

    # TODO: Turn off the coffee machine by entering "off" to the prompt
    def turn_off(self) -> None:
        self.is_on = False

    # Create a function to format the units of the resources
    def format_resources(self) -> str:
        fmt_str = ""
        fmt_str += f"Water: {self.resources['water']}ml\n"
        fmt_str += f"Milk: {self.resources['milk']}ml\n"
        fmt_str += f"Coffee: {self.resources['coffee']}g\n"
        fmt_str += f"Money: ${self.resources['money']:0.2f}"
        return fmt_str

    # Print a report showing the current resources of the coffee machine
    def print_resources(self) -> None:
        print(self.format_resources())
    
    # Create a function to print an insufficient resource
    def print_insufficient_resource(self, resource: str) -> None:
        print(f'Sorry, there is not enough {resource}.') 

    # Create a function to check whether the user requested option can be supported by the coffee machine's
    # current resources.
    def check_resources_sufficient(self, drink: str) -> bool:
        enough_resources = True

        if drink not in MENU.keys():
            return not enough_resources
        
        # Check if there's enough resources for every ingredient
        for resource in MENU[drink]['ingredients']:
            if self.resources[resource] - MENU[drink]['ingredients'][resource] < 0:
                self.print_insufficient_resource()
                return not enough_resources
        
        return enough_resources

    # Create a function to get the coin type
    def get_coin_qty(self, coin: str) -> int:
        qty = input(f"How many {coin if coin != 'penny' else 'pennie'}s?: ")
        
        while not qty.isnumeric():
            print(f'Error: Please enter an integer value for the {coin}.')
            qty = input(f"How many {coin if coin != 'penny' else 'pennie'}s?: ")
        return int(qty)

    # Create a function to process the coins and return the total based on user inputted
    # quarters, dimes, nickles, and pennies
    def process_coins(self) -> float:
        total_amount = 0.0

        for coin in COIN_MAP:
            total_amount += (self.get_coin_qty(coin)*COIN_MAP[coin])
        return total_amount

    # Create a function to check whether the transaction was successful or not
    def transaction_successful(self, amount_provided: float, drink_cost: float) -> bool:
        # Check if user coins is sufficient to pay for the drink
        if amount_provided < drink_cost:
            print("Sorry that's not enough money. Money refunded.")
            return False
        
        # Dispense refund of excess amount. add drink cost to money in machine.
        elif amount_provided > drink_cost:
            print(f"Here is ${(amount_provided - drink_cost):0.2f} in change.")

        return True
    
    def deduct_resources(self, ingredients: dict) -> None:
        for ingredient in ingredients:
            self.resources[ingredient] -= ingredients[ingredient]

    # Create a function to make the coffee
    def make_coffee(self, usr_cash: float, drink: str, cost: float) -> None:
        if self.transaction_successful(amount_provided=usr_cash, drink_cost=cost) and \
        self.check_resources_sufficient(drink=drink):
            self.resources['money'] += cost
            self.deduct_resources(MENU[drink]['ingredients'])
            print(f"Here is your {drink}. Enjoy!")

def main():
    # Make the coffee machine
    coffee_machine = CoffeeMachine(resources=DEFAULT_RESOURCES)

    # While the machine is on
    while coffee_machine.is_on:
        # Get user drink selection
        drink = coffee_machine.get_drink_selection()

        if drink == "off":
            coffee_machine.turn_off()
            continue
        elif drink == "report":
            coffee_machine.print_resources()
            continue
            
        cash_inserted = coffee_machine.process_coins()

        coffee_machine.make_coffee(usr_cash=cash_inserted, drink=drink, cost=MENU[drink]['cost'])

if __name__ == "__main__":
    main()