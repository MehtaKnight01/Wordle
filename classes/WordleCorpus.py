import sys
import numpy as np

def read_array_from_file(path):
	file = open(path)
	array = file.read().splitlines()
	nparray = np.array(array)
	file.close()
	return nparray

#Definitions:
#Guess - a 5-letter word from the list of possible guesses
#Solution - a 5-letter word from the list of possible solutions
#Result/State - the response that wordle gives you for making a guess (i.e. "Green, Black, Black, Yellow, Black") which is a function of a guess and a solution


#Corpus of guesses, solutions and possible-results-for-each-guess
class Corpus:

	def __init__(self, guesses_file_path, solutions_file_path, state_file_path):
		
		ALL_SOLUTIONS = read_array_from_file(solutions_file_path)

		#Load arrays
		self.guesses = read_array_from_file(guesses_file_path)
		self.solutions = ALL_SOLUTIONS
		self.stateArray = np.load(state_file_path)
		assert (len(self.guesses), len(self.solutions)) == self.stateArray.shape
		assert (54 == self.stateArray[6117, 868]), str(self.stateArray[6117, 868])


	def removeGuesses(self, guesses):
		if isinstance(guesses[0], int):
			self.__removeGuessesByIndex(guesses)
		if isinstance(guess[0], str):
			print "TODO removing guesses by value"

	def removeGuess(self, guess):
		if isinstance(guess, int):
			self.__removeGuessesByIndex(guess)
		if isinstance(guess, str):
			self.__removeGuessesByValue(guess)

	def getGuessValue(self, index):
		return self.guesses[index]

	def getGuessIndex(self, value):
		tup = np.where(self.guesses == value)
		assert len(tup[0]) == 1
		return tup[0][0]


	def removeSolutions(self, listToRemove):
		#remove from both solutions list and stateArray
		self.solutions = np.delete(self.solutions, listToRemove)
		self.stateArray = np.delete(self.stateArray, listToRemove, axis=1)
		assert self.solutions.shape[0] == self.stateArray.shape[1], self.stateArray.shape

	def pruneGuesses(self):
		#if a guess has no states, get rid of it
		mask = np.invert(self.stateArray.any(axis=1))
		indices = self.__get_indices_of_empty(mask)
		self.removeGuesses(indices)

	def __removeGuessesByIndex(self, indices):
		self.guesses = np.delete(self.guesses, indices)
		self.stateArray = np.delete(self.stateArray, indices, axis=0)
		assert self.guesses.shape[0] == self.stateArray.shape[0], self.stateArray.shape


	def __removeGuessesByValue(self, vals):
		print "TODO"
		quit()

	def __get_indices_of_empty(mask):
		indices = [index for index, value in mask if value == True]



		