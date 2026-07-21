'''
    Code to automate drafting an email based on a list of names from the starting_letter.txt file.
    For each [name] in invited_names.txt, replace the [name] placeholder with the actual name.
    Save the resulting letters in a folder called "ReadyToSend"
'''

def main():
    names = []
    letter = []

    # Read in the names from the invited_names.txt
    with open("invited_names.txt", "r") as file:
        for name in file:
            name = name[:-1] if name[-1] == '\n' else name
            names.append(name)
    
    # Read in the letter
    with open("starting_letter.txt", "r") as file:
        for line in file:
            letter.append(line)
    
    # Create each customized letter
    for name in names:
        with open(f"./ReadyToSend/{name}.txt", mode="w") as file:
            for line in letter:
                if "[name]" in line:
                    line = line.replace("[name]", name)
                file.write(line)
    
    print(letter)


if __name__ == "__main__":
    main()