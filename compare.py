from preprocessing import preproc
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import operator
import numpy as np
import os
import pickle
import sys

class Compare(object):
	"""This class is used to compare the query string with the current
	corpus documents using the vectors for each of these documents and the
	cosine similarity to assess their closeness."""
	def __init__(self, arg):
		#deserialise the saved document vectors.
		doc_vectors = {}
		with open('doc_vectors.pkl','rb') as f:
		    doc_vectors = pickle.load(f)

		#deserialise the saved terms and the correspoding inverted-index.
		all_terms = {}
		with open('all_terms.pkl','rb') as f:
		    all_terms = pickle.load(f)

		#deserialise the saved inverted-document frequency
		term_df = []
		with open('term_df.pkl','rb') as f:
		    term_df = pickle.load(f)

		#deserialise the saved documents mapped to their IDs.
		with open('doc_id.pkl','rb') as f:
		    doc_id = pickle.load(f)


		#open the file and perform preprocessing
		name = arg
		f = open(name,"r")
		sr = f.read()
		final_doc = preproc(sr)

		#get all the terms of the query doc. with their respective frequencies.
		mp = Counter(final_doc)

		#initialise the document vector for the query document, with all zeroes
		q_vector = [0]*len(all_terms)
		idx = 0
		for i in sorted(all_terms.keys()):
			if i in final_doc:
		        #update the document vector with the frquencies of all the terms
				q_vector[idx] += mp[i]
			idx+=1

		q_vector = np.log(np.add(1,q_vector))       #lg(1+tf)
		q_vector = np.multiply(q_vector,term_df)    #lg(1+tf)*lg(N/df)
		q_vector /= np.linalg.norm(q_vector)        #normalize the document-vector


		#perform dot-product multiplication with the document vectors of the corpus documents
		dot_scores = {}
		for i in doc_vectors:
			score = np.dot(q_vector,doc_vectors[i])
			dot_scores[i] = score

		#sort the dictionary of docid : dot_prod according to the dot-product values.
		sorted_dot_scores = sorted(dot_scores.items(),key = operator.itemgetter(1), reverse = True)

		f = open('compare.txt','wt')
		no= 0
		#print the most-similar-document ranking
		for i in sorted_dot_scores :
			docid = i[0]
			score = i[1]
			for k,v in doc_id.items():
				if v == docid:
					name = k
			name = name.split(".")[0]

			if no < 5 :
				f.write(name + " : " + str(score) + "\n")
				no = no +1
