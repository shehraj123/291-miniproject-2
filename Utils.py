# This file contains functions useful for clearing screen and printing prompt
import os

"""
The function clears the shell for the new screen.
Arguments:
None
"""
def shellClear():
        if os.name == 'nt':
            os.system('cls')

        elif os.name == 'posix':
            os.system('clear')


"""
The function clears the shell for the new screen and makes it ready for the next prompt.
Arguments:
None
"""
def printPrompt(header, prompt):
    shellClear()
    print(header)
    print(prompt) 

"""
The function takes input from the user and validates it along with error handling
Arguments:
None
"""
def takeOption(num_options):
    op = [i+1 for i in range(num_options)]
    i = 0
    done = False
    while not done:
        try:
            while i not in op:
                i = int(input("Choose: "))
            done = True 
        except ValueError:
            print("\nEnter valid number")
            i = 0

    return i                