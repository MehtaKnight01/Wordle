from classes.WordleCorpus import Corpus
import numpy as np
from enum import Enum


class GameStates(Enum):
    NOTWON = 0
    WON = 242

#Definitions:
#Guess - a 5-letter word from the list of possible guesses
#Solution - a 5-letter word from the list of possible solutions
#Result/State - the response that wordle gives you for making a guess (i.e. "Green, Black, Black, Yellow, Black") which is a function of a guess and a solution


#handles playing of a single wordle game
class Game: 

	def __init__(self, corpus, trueSolution):

		self.solution = trueSolution
		self.resultsForSolution = self.__getResultsForSolution(corpus, trueSolution)
		self.turn = 1
		self.resultOfGuess = None #One of 3^5-1 possible results for making a given guess (as an int)
		self.guesses = corpus.guesses
		self.gameOver = False

	#resultsForSolution is the array of all possible results for all guesses for the true solution
	def __getResultsForSolution(self, corpus, trueSolution):
		#trueSolution is a word, not an index
		trueSolIndices = np.where(corpus.solutions == trueSolution) #returns a tuple, annoyingly
		assert len(trueSolIndices[0]) == 1 
		trueSolIndex = trueSolIndices[0][0] #flatten
		return corpus.stateArray[:,trueSolIndex]

	#equivalent of typing a guess into wordle and hitting enter
	def checkGuess(self, guessVal):
		#determine index of guess
		guessIndices = np.where(self.guesses == guessVal) #returns a tuple, annoyingly
		assert len(guessIndices[0]) == 1
		self.resultOfGuess = self.resultsForSolution[guessIndices[0][0]]
		if self.resultOfGuess == GameStates.WON.value:
			self.gameOver = True
		else:
			self.turn += 1
		# print "Result of guessing ", guessVal, " was ", self.resultOfGuess


	def gameOver():
		return self.gameOver
