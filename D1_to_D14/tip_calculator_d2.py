'''
    This application calculates the amount due for each person based on a total
    bill amount and a tip percentage.
'''
WELCOME = "Welcome to the tip calculator!"
TOTAL_BILL_PROMPT = "What was the total bill? $"
TIP_PROMPT = "How much tip would you like to give? 10, 12, or 15? "
BILL_SPLIT_PROMPT = "How many people to split the bill? "

print(WELCOME)
total_bill = float(input(TOTAL_BILL_PROMPT))
tip = int(input(TIP_PROMPT))
split_num = int(input(BILL_SPLIT_PROMPT))
bill_split_amount = (total_bill * (1+(tip/100))) / split_num

print(f"Each person should pay: ${bill_split_amount:0.2f}")