'''
    This application implements a caesar shift cipher based on user input:
        1. The secret word/phrase only as alpha (i.e., letters)
        2. Step size (int)
'''
digits = "0123456789"
alpha = "abcdefghijklmnopqrstuvwxyz"

def encoder_decoder(phrase: str, step_size : int, is_encode: bool) -> str:
    # Check if encoding or decoding
    step_size = step_size if is_encode else -step_size

    # Turn phrase into a list
    phrase = list(phrase)

    # Shift all chars in phrase by the step size
    for i, char in enumerate(phrase):
        if char not in alpha or char == " ":
            continue

        # Get the char index
        char_idx = alpha.index(char)+step_size
        while char_idx < 0:
            char_idx += len(alpha)

        # Shift the char by the step_size; ensure it falls within range(0,len(alpha))
        phrase[i] = alpha[(char_idx) % len(alpha)]
    
    return "".join(phrase)

def is_valid_step(step_size: str) -> bool:
    # Empty input
    if step_size is None:
        return False
    
    # Check if it's negative
    if len(step_size) > 1:
        if step_size[0] == '-':
            if step_size[1] == '0':
                return False
            if not step_size[1::].isnumeric():
                return False
        if step_size[0] == '0':
            return False
    
    return True

def main():
    # Get user input to encode
    phrase = input("What phrase would you like encoded? ").lower()
    step_size = input("What is the step_size? ")

    while not is_valid_step(step_size):
        print("Error: Invalid step_size!\n")
        step_size = input("What is the step_size? ")
    
    print(f"Encoded phrase is: {encoder_decoder(phrase, int(step_size), True)}")
    
    # Get user input to decode
    phrase = input("What phrase would you like decoded? ").lower()
    step_size = input("What is the step_size? ")
    
    while not is_valid_step(step_size):
        print("Error: Invalid step_size!\n")
        step_size = input("What is the step_size? ")
    
    print(f"Decoded phrase is: {encoder_decoder(phrase, int(step_size), False)}")

if __name__ == "__main__":
    main()