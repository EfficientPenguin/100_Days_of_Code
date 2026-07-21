'''
    This application will take user inputs and generate a password based on:
        letters,
        symbols,
        numbers
'''

import random

symbols_set = '!@#$%^&*()-_+='
alpha_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digit_set = '0123456789'

print('\nWelcome to the PyPassword Generator!\n------------------------------------\n')
num_letters = int(input('How many letters would you like in your password?\n'))
num_symbols = int(input('How many symbols would you like?\n'))
num_digits = int(input('How many numbers would you like?\n'))
password = []

# Generate random letters, then symbols, then digits
for _ in range(num_letters):
    password.append(alpha_set[random.randint(0, len(alpha_set)-1)])
for _ in range(num_symbols):
    password.append(symbols_set[random.randint(0, len(symbols_set)-1)])
for _ in range(num_digits):
    password.append(digit_set[random.randint(0, len(digit_set)-1)])

# shuffle and report back password
random.shuffle(password)

print(f'Your password is: ' + "".join(password))