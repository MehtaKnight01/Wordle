from __future__ import division
import timeit
import sys
from enum import Enum
import numpy as np
import random
import math
from classes.WordleCorpus import Corpus
from classes.WordleGame import Game
from classes.WordleSolver import Solver
import WordleAlgs
import copy
import os 


#Definitions:
#Guess - a 5-letter word from the list of possible guesses
#Solution - a 5-letter word from the list of possible solutions
#Result/State - the response that wordle gives you for making a guess (i.e. "Green, Black, Black, Yellow, Black") which is a function of a guess and a solution


#For testing an algorithm against every single possible Wordle solution and seeing how well it does


#Uncomment if passing guesses, solutions, and statearray manually
# GUESSES_FILE_PATH = sys.argv[1]
# SOLUTIONS_FILE_PATH = sys.argv[2]
# STATE_ARRAY_FILE_PATH = sys.argv[3
ROOT_DIR = os.path.dirname(__file__)
GUESSES_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'guesses.txt')
SOLUTIONS_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'solutions.txt')
STATE_ARRAY_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'state_array')

file = open(SOLUTIONS_FILE_PATH)
ALL_SOLUTIONS = file.read().splitlines()
file.close()

def averageTurnsToWin(turnsArray):
	total = 0
	for index, value in enumerate(turnsArray):
		total += (index+1) * value
	return total / sum(turnsArray)

#Load characteristics of algorithm you want to use
obj_fn = WordleAlgs.log_Fn
tieBreakFn = None #WordleAlgs.log_Fn #only if necessary
bestStart = WordleAlgs.LOG_BEST_START
maximize = False

#Initialize corpus of guesses, solutions, and results
CORPUS = Corpus(GUESSES_FILE_PATH, SOLUTIONS_FILE_PATH, STATE_ARRAY_FILE_PATH) #I don't understand python well enough to know if this is performant
firstGuessResultsArray = CORPUS.stateArray[bestStart[0]] #Array of all possible outputs for the first guess, precomputed for better performance

nTurnsToWin = [0]*9
start = timeit.default_timer()

#main loop
for trueSolution in ALL_SOLUTIONS:

	corpus = copy.deepcopy(CORPUS) 
	game = Game(corpus, trueSolution)
	solver = Solver(bestStart[0], firstGuessResultsArray, corpus, obj_fn, maximize)
	# print "Beginning new game to try and guess: ", game.solution

	while True:
		solver.makeGuess()
		game.checkGuess(solver.bestGuess[1])
		if game.turn > 5: 
			print "Particularly bad solution for this algorithm", game.solution, solver.bestGuess, game.resultOfGuess, game.turn
		if game.gameOver:
			# solver.printGuessedWords()
			break
		else:
			assert game.turn < 10, "Took longer than 10 turns"
			solver.obtainNextGuess(game.resultOfGuess)

	nTurnsToWin[game.turn - 1] += 1
	# print "This game, the solution was " + game.solution + " and I won in " + str(game.turn) + " turns"

print nTurnsToWin
print "Average number of turns to win: " + str(averageTurnsToWin(nTurnsToWin))
print "Completed in ", timeit.default_timer() - start, " seconds"




