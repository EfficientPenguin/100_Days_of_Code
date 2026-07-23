'''
    Day 54 introduces Flask, a lightweight back-end web development framework and library.
'''

from time import sleep

# Decorator function practice

def delay_decorator(function):
    def wrapper_function():
        sleep(2)
        # Add functionality before say_hello
        function()
        # Add functionality after say_hello
        # You can even call say_hello multiple times
        # function()
    return wrapper_function

@delay_decorator
def say_hello():
    print('hello')


# Call say_hello function with the delay
say_hello()