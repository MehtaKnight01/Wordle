from __future__ import division
import sys
import numpy as np
import math
import os
from classes.WordleCorpus import Corpus

#For defining algorithms that can be used to optimally solve Wordles


#----------------------- BEGIN defining algorithms ----------------------- 

#I'm taking a 2315-length array that contains numbers from 1 to 243, and turning it into a 243-length array that contains the counts of each value in the original array
#These are the sizes of the "branches" of a particular guess in the search tree
def getBranches(states):
	return np.bincount(states)

#computes expected size of possible remaining solutions 
def rishil_Fn(states):
	n = states.size
	branches = np.bincount(states)
	expectedCost = 0.0
	for branchSize in branches:
		if branchSize > 0:
			cost = branchSize
			prob = branchSize/n
			expectedCost += cost * prob
	return expectedCost

#computes expected log(size) of possible remaining solutions
#In theory, minimizing log(size) ought to be more "accurate" because each iteration of guessing reduces the solution set to a fraction of its previous size
def log_Fn(states):
	n = states.size
	branches = getBranches(states)
	expectedCost = 0.0
	for branchSize in branches:
		if branchSize > 0:
			cost = math.log(branchSize)
			prob = branchSize/n
			expectedCost += cost * prob
	return expectedCost

#Knuth's minimax is proven to have the best worst-case performance
def knuth_Fn(states):
	branches = getBranches(states)
	return branches.max()

#TODO, not currently working
def greedy_Fn(states):
	branches = getBranches(states)
	return np.count_nonzero(branches)

#----------------------- END defining algorithms -----------------------


#Set pre-computed best first words for a given algorithm. Index corresponds to location in guess list.
LOG_BEST_START = [10364, "SOARE"]
RISH_BEST_START = [8859, "RAISE"] #[9247, "ROATE"]
KNUTH_BEST_START = [8859, "RAISE"]


#For pre-computing of the best first word for a given algorithm. Run this each time a new function is developed.

#Uncomment if passing guesses, solutions, and statearray manually
# GUESSES_FILE_PATH = sys.argv[1]
# SOLUTIONS_FILE_PATH = sys.argv[2]
# STATE_ARRAY_FILE_PATH = sys.argv[3]
ROOT_DIR = os.path.dirname(__file__)
GUESSES_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'guesses.txt')
SOLUTIONS_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'solutions.txt')
STATE_ARRAY_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'state_array')

def sortSecond(val):
	return val[1]

#Runs one iteration of the best-guess-finding code, returning the top n results
def getBestFirstWords(obj_fn, maximize, tieBreakFn = None):
	n = 10
	corpus = Corpus(GUESSES_FILE_PATH, SOLUTIONS_FILE_PATH, STATE_ARRAY_FILE_PATH)
	#obtain next guess
	payoffsOfGuesses = []
	i = 0
	for states in corpus.stateArray:
		expectedPayoff = obj_fn(states)
		val = [corpus.guesses[i], expectedPayoff]
		if tieBreakFn != None:
			expectedPayoff = tieBreakFn(states)
			val.append(expectedPayoff)
		payoffsOfGuesses.append(val)
		i += 1
	payoffsOfGuesses.sort(key=sortSecond)
	return payoffsOfGuesses[:n]

# print getBestFirstWords(knuth_Fn, False, log_Fn)


