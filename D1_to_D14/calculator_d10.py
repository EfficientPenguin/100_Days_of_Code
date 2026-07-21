'''
    This application implements a simple text-based calulator. Inputs are received from
    the user, and the application calculates the result.
'''

def calculate_result(a : float, b : float, operator : str) -> str:
    ''' 
        It will calculate the result of two floats a and b and return a str.
        For divide by 0 case, an error is printed out and an empty string is returned.
    '''
    result = ''

    if operator == '+':
        result = a+b
    elif operator == '-':
        result = a-b
    elif operator == '/':
        if b == 0:
            print('Error: Cannot divide by 0!')
        else:
            result = a/b
    elif operator == '*':
        result = a*b

    return result

def format_num(result : float) -> str:
    ''' Make an int if we have trailing 0's in result;
        else, format to two decimal places
    '''
    if result and result % 1 == 0:
        result = str(int(result))
    else:
        result = f'{result:0.2f}'
    
    return result

def get_operator() -> str:
    '''
        Get the operator from the user. Do basic error checking if it's not one of the 4 valid operators
        for this application.
    '''
    OPERATOR_PROMPT = "What is the operator? Please enter any of these operators: + - / *\n"
    operator = input(OPERATOR_PROMPT)
    while operator not in "+-/*" and operator != ' ' and operator != '':
        print('Error: Invalid operator!')
        operator = input(OPERATOR_PROMPT)

    return operator

def get_operand(is_operand1 : bool) -> float:
    '''
        Get an operand from the user. Print the text according to the operand type (i.e., "first" or "second")
        for this application.
    '''
    OPERAND_PROMPT = f"What is the {"first" if is_operand1 else "second"} number? "
    operand = input(OPERAND_PROMPT)

    # TODO: Error checking.

    return float(operand)




def main():
    # Get first number, operator, then second number, and print result
    # Ask y/n for next number or new calculation
    choice = ''
    result = ''
    use_num1 = False
    perform_calculation = True

    while perform_calculation:
        num1 = get_operand(is_operand1=True)
        operator = get_operator()
        use_num1 = True

        while use_num1:
            num2 = get_operand(is_operand1=False)
            result = format_num(calculate_result(num1, num2, operator))

            # Valid result
            if result != '':
                choice = input(f"The result is {result}. Continue using {result} (y/n)? Type 'e' to exit the application. ").lower()
                while choice != 'y' and choice != 'n' and choice != 'e':
                    choice = input(f"Error: Invalid choice. Continue using {result} (y/n)? Type 'e' to exit the application. ").lower()

            # Continue using previous calculation (i.e., num1 becomes curr result); else, restart calc 
            if choice == 'y':
                num1 = float(result)
            elif choice == 'n':
                use_num1 = False
            elif choice == 'e':
                use_num1 = False
                perform_calculation = False
    
    print('Done performing calculations. The application will now exit.')        

if __name__ == "__main__":
    main()