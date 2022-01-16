import sqlite3, sys
import numpy as np
from enum import Enum
import pickle

#Definitions:
#Guess - a 5-letter word from the list of possible guesses
#Solution - a 5-letter word from the list of possible solutions
#Result/State - the response that wordle gives you for making a guess (i.e. "Green, Black, Black, Yellow, Black") which is a function of a guess and a solution


#Creates a lookup table of results for every single combination of (Guess, Solution). Should be approx 12000x2300 in size.

kWordLength = 5

# Download solutions
SOLUTIONSFILEPATH = sys.argv[2]
file = open(SOLUTIONSFILEPATH)
ALLSOLUTIONS = file.read().splitlines()
file.close()
ALLSOLUTIONS = [solution.upper() for solution in ALLSOLUTIONS if len(solution) == kWordLength]
# ALLSOLUTIONS = list(set(ALLSOLUTIONS))
print(len(ALLSOLUTIONS))

# Download guesses
GUESSESFILEPATH = sys.argv[1]
file = open(GUESSESFILEPATH)
GUESSES = file.read().splitlines()
file.close()
GUESSES = [guess.upper() for guess in GUESSES if len(guess) == kWordLength]
print(len(GUESSES))


TABLEFILEPATH = "./state_array"

class LetterStates(Enum):
    NOTPRESENT = 0
    INCORRECTPOSITION = 1
    CORRECTPOSITION = 2

# def build_sql_table():
# 	# Create SQL table
# 	conn = sqlite3.connect(':memory:')
# 	c = conn.cursor()
# 	c.execute("""CREATE TABLE letters (
# 	  word_id INTEGER,
# 	  letter INTEGER,
# 	  letter_idx INTEGER
# 	)""")
# 	c.execute('CREATE INDEX foo ON letters(letter, letter_idx, word_id);')
# 	for i, solution in enumerate(ALLSOLUTIONS):
# 	  for j, letter in enumerate(solution):
# 	    c.execute('INSERT INTO letters (word_id, letter, letter_idx) VALUES (?, ?, ?)', (i, ord(letter), j))

def check_guess(guess, solution):
        # https://mathspp.com/blog/solving-wordle-with-python
        # pool is set of letters in the solution available for INCORRECTPOSITION
        pool = {}
        for g, s in zip(guess, solution):
            if g == s:
                continue
            if s in pool:
                pool[s] += 1
            else: 
                pool[s] = 1

        states = []
        for guess_letter, solution_letter in zip(guess, solution):
            if guess_letter == solution_letter:
                states.append(LetterStates.CORRECTPOSITION)
            elif guess_letter in solution and guess_letter in pool and pool[guess_letter] > 0:
                states.append(LetterStates.INCORRECTPOSITION)
                pool[guess_letter] -= 1
            else:
                states.append(LetterStates.NOTPRESENT)
        return states

def build_state_array(guesses, solutions):
	return [all_solutions_for_guess(guess, solutions) for guess in guesses]
 
def all_solutions_for_guess(guess, solutions):
	return [value_for_solution(guess,solution) for solution in solutions] 
	
#turns enumeration of guess outcome into a value out of 243
def value_for_solution(guess, solution):
	characterStates = check_guess(guess, solution)
	value = 0
	for index, state in enumerate(characterStates):
		value += state.value * pow(3, index)
	return value

# print GUESSES[6117]
# print ALLSOLUTIONS[868]
# print value_for_solution(GUESSES[6117], ALLSOLUTIONS[868])

a = [None]*len(GUESSES)
for i, guess in enumerate(GUESSES):
    # print i, guess
    b = [None]*len(ALLSOLUTIONS)
    for j, solution in enumerate(ALLSOLUTIONS):
        b[j] = value_for_solution(guess, solution)
        if guess == "LATEN" and solution == "ROVER":
            print guess, solution, i, j, b[j]
    a[i] = b




# array = np.array(build_state_array(GUESSES, ALLSOLUTIONS))
array = np.array(a, dtype=np.uint8)
assert value_for_solution("LATEN", "ROVER") == array[6117, 868], str(value_for_solution("LATEN", "ROVER")) + str(array[6117, 868])
array.dump(TABLEFILEPATH)
print array.shape
