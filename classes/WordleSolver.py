from __future__ import division
import sys
from enum import Enum
import numpy as np
import random
import math
from classes.WordleCorpus import Corpus

#Definitions:
#Guess - a 5-letter word from the list of possible guesses
#Solution - a 5-letter word from the list of possible solutions
#Result/State - the response that wordle gives you for making a guess (i.e. "Green, Black, Black, Yellow, Black") which is a function of a guess and a solution

#solves one game of Wordle using a specified algorithm
class Solver: 

	def __init__(self, initial_best_guess_index, initial_results_for_guess_array, corpus, obj_fn, maximize, tieBreakObjFn = None):

		self.corpus = corpus

		#Make the first "move" right away since it is pre-computed
		self.bestGuess = [initial_best_guess_index, self.corpus.getGuessValue(initial_best_guess_index)] #index, value
		self.guessesMade = [self.bestGuess[1]]

		self.obj_fn = obj_fn #which function to use to evaluate the best guess
		self.maximize = maximize #if true, obj fun should be maximized, otherwise minimized

		self.tieBreakObjFn = tieBreakObjFn #if our function results in ties, we may need a second function to tiebreak

		self.resultsForGuess = initial_results_for_guess_array #set of results for a given guess for faster lookup #pre-computed

	def makeGuess(self):
		# self.printPossibleSolutions()
		# print "Guessing " + str(self.bestGuess[1])
		return
		

	def obtainNextGuess(self, prevResult, guess = None):
		#remove previous guess from the list of not-yet-guessed words
		self.__removeGuess(self.bestGuess[0])

		#The indices in resultsForGuess that do not correspond to the actual result seen correspond to solutions that are no longer possible and can be removed
		indices = np.where((self.resultsForGuess != prevResult)) 
		self.__removeSolutions(indices)

		if guess == None: 
			self.bestGuess = self.__getBestGuess()
		else: 
			self.bestGuess = self.setBestGuess(guess)
		self.guessesMade.append(self.bestGuess[1])
		self.resultsForGuess = self.__getResultsForGuess(self.bestGuess[0])


	def __getBestGuess(self):
		if len(self.corpus.solutions) <= 2:
			#Base case optimal algorithm for when remaining solutions are two or less
			#If there are only two solutions, pick one at random, and if you're wrong, you'll win next turn by picking the other
			#If there is only one solution, pick it and you'll win this turn
			val = self.corpus.solutions[0]
			i = self.corpus.getGuessIndex(val)
			return [i, val]
		else: 
			#When remaining solutions are 3 or higher, use the algorithm that was provided to determine the best guess
			bestObjective = 0.0 if self.maximize else 100000000
			indicesOfBestGuesses = []
			i = 0
			for states in self.corpus.stateArray:
				objective = self.obj_fn(states)
				comparison = (objective > bestObjective) if self.maximize else (objective < bestObjective)
				if comparison: #if our guess is better than the best one so far, make our guess the best one so far
					indicesOfBestGuesses = [i]
					bestObjective = objective
				elif objective == bestObjective: #if our guess is comparable to the best one so far, add it to the list of best guesses
					indicesOfBestGuesses.append(i)
				i += 1

		#choose a single best guess from the list of candidate best guesses to become the next chosen guess
		return self.__pickBestGuessFromList(indicesOfBestGuesses)

	def printPossibleSolutions(self):
		print "Only remaining possible solutions are: ", self.corpus.solutions

	def printGuessedWords(self):
		print "The words that were guessed over this game were: ", self.guessesMade

	def setBestGuess(self, guess):
		#forcibly set the best guess to something else
		index = self.corpus.getGuessIndex(guess)
		return [index, guess] 

	def __pickBestGuessFromList(self, indices):
		#First priority is to pick any that's in the set of solutions
		for index in indices:
			guess = self.corpus.getGuessValue(index)
			if guess in self.corpus.solutions:
				return [index, guess]
		#If there are multiple "best guesses", we can use a different objective function to rank them if we want
		if self.tieBreakObjFn != None:
			bestObjective = 0.0 if self.maximize else 100000000
			for index in indices: 
				states = self.corpus.stateArray[index]
				objective = self.tieBreakObjFn(states)
				comparison = (objective > bestObjective) if self.maximize else (objective < bestObjective)
				if comparison: #if our guess is better than the best one so far, make our guess the best one so far
					indexOfBestGuess = index
					bestObjective = objective
			return [index, self.corpus.getGuessValue(index)]
		#Otherwise, just pick the first one from the list
		return [indices[0], self.corpus.getGuessValue(indices[0])] 


	def __removeGuess(self, guessIndex):
		self.corpus.removeGuess(guessIndex)

	def __removeSolutions(self, solutionIndices):
		self.corpus.removeSolutions(solutionIndices)

	#resultsForGuess is the array of all possible results for all solutions for a given guess
	def __getResultsForGuess(self, guess):
		return self.corpus.stateArray[guess]