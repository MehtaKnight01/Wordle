import sys
import numpy as np
from classes.WordleSolver import Solver
from classes.WordleCorpus import Corpus
import WordleAlgs
import os
from enum import Enum

#Definitions:
#Guess - a 5-letter word from the list of possible guesses
#Solution - a 5-letter word from the list of possible solutions
#Result/State - the response that wordle gives you for making a guess (i.e. "Green, Black, Black, Yellow, Black") which is a function of a guess and a solution


#For getting help from the computer when playing a single game of Wordle


class LetterStates(Enum):
    NOTPRESENT = 0
    INCORRECTPOSITION = 1
    CORRECTPOSITION = 2

#Uncomment if passing guesses, solutions, and statearray manually
# GUESSES_FILE_PATH = sys.argv[1]
# SOLUTIONS_FILE_PATH = sys.argv[2]
# STATE_ARRAY_FILE_PATH = sys.argv[3]
ROOT_DIR = os.path.dirname(__file__)
GUESSES_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'guesses.txt')
SOLUTIONS_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'solutions.txt')
STATE_ARRAY_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'state_array')

#Load characteristics of algorithm you want to use
obj_fn = WordleAlgs.knuth_Fn
bestStart = WordleAlgs.KNUTH_BEST_START 
maximize = False

#Initialize corpus of guesses, solutions, and results
corpus = Corpus(GUESSES_FILE_PATH, SOLUTIONS_FILE_PATH, STATE_ARRAY_FILE_PATH) #I don't understand python well enough to know if this is performant
firstGuessResultsArray = corpus.stateArray[bestStart[0]] #Array of all possible outputs for the first guess
solver = Solver(bestStart[0], firstGuessResultsArray, corpus, obj_fn, maximize)

#turns enumeration of guess outcome into a value out of 243
def getStateValue(characterStates):
	value = 0
	for index, state in enumerate(characterStates):
		value += state.value * pow(3, index)
	return value



for y in range(1,7):
	states = []
	print "Guess ", solver.bestGuess[1]
	solver.makeGuess()
	for i in range(1,6):
		result = input("Enter result for letter " + str(i) + ": ")
		states.append(LetterStates(result))
	stateValue = getStateValue(states)
	if stateValue == 242:
		solver.printGuessedWords()
		print "Winner!"
		quit()
	solver.obtainNextGuess(stateValue)
	nSolutions = len(solver.corpus.solutions)
	print "There are only " + str(nSolutions) + " possible solutions remaining."
	if nSolutions <= 170:
		print "These solutions are ", solver.corpus.solutions

print "You lose! :("
