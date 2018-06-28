from preprocessing import preproc
from fingerprinting import winnow, get_hash
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import operator
import numpy as np
import os
import pickle
import sys
import operator

class Compare1(object):
	"""This class is used to compare the query string with the current
	corpus documents using their unique fingerprints."""
	def __init__(self, arg):
		
		# deserialise the saved fingerprints of the corpus documents
		fingerprints = {}
		with open('fingerprints.pkl', 'rb') as f:
		    fingerprints = pickle.load(f)

		# open the file and perform preprocessing
		name = arg
		f = open(name, "r")
		sr = f.read()
		final_doc = preproc(sr)

		# set the parameters for Rabin-Karp hashing
		k = 5
		base = 10

		# set the window for the winnowing algorithm
		window = 10

		# split the cleaned document into k-grams and find their hash-values
		sr = ''.join(final_doc)
		hash_val = get_hash(sr, k, base)

		# select only a few of the hash-values using the winnowing technique
		fingerprint = winnow(hash_val, window)

		# find the number of fingerprints that match between the query document and the corpus
		# documents
		no_of_matches = {}
		s1 = set(row[0] for row in fingerprint)
		f = open('compare1.txt','wt')
		for k, v in fingerprints.items():
		    s2 = set(row[0] for row in v)
		    no_of_matches[k] = len(s1.intersection(s2))
		
		sorted_matches = sorted(no_of_matches.items(), key=operator.itemgetter(1),reverse = True)

		
		no = 0
		for x in sorted_matches:	
			if no < 5 :
				f.write(x[0] + " : "+ str(x[1]) + "\n")
				no = no + 1
