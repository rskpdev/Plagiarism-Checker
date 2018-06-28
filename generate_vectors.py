from collections import Counter
import pickle
import numpy as np
import math
import os

#storing the inverted index.
#all_terms[term] is a list of all the DocId's of the documents that
#the term appears in. 
all_terms = {}

#mp[docid] stores a dictionary of the form - 'term' : 'frequency'
mp = {} 

#storing the DocID of each document.
docid = {} 

#co : the current doc-id
co = 1
for i in os.listdir('./cleaned'):
    sr = []
    docid[i] = co
    with open('./cleaned/' + i, 'rb') as f:
        sr = pickle.load(f)
    #Counter returns the no. of occurences of each term in the document as a
    #dictionary.
    mp[co] = Counter(sr) 
    for k in mp[co].keys():
        if not k in all_terms:
            all_terms[k] = []
        all_terms[k].append(co)
    co = co + 1

#stores the document-vectors for each document
vectors = {}

no_of_docs = len(docid)
no_of_terms = len(all_terms)

for i in range(no_of_docs):
    vectors[i+1] = [0]*no_of_terms

#eventually, stores the inverted-document frquency of all terms under consideration.
#The terms are associated with the keys of the all_terms dictionary and are
#indexed in 'df' in a sorted order.
df = []

co = 0
for i in sorted(all_terms.keys()):
    df.append(len(all_terms[i]))
    df[co] = math.log(no_of_docs/df[co]) #stores the idf value of the term
    for j in all_terms[i]:
        vectors[j][co] = mp[j][i]
    co = co + 1

for i in vectors:
    vectors[i] = np.log(np.add(1,vectors[i]))  #lg(1+tf)
    vectors[i] = np.multiply(vectors[i],df)    #lg(1+tf)*lg(N/df)
    vectors[i] /= np.linalg.norm(vectors[i])  #normalize the document-vector

#serialise all the maps and lists.
with open('doc_id.pkl','wb') as f:
    pickle.dump(docid,f)

with open('doc_vectors.pkl','wb') as f:
    pickle.dump(vectors,f)

with open('all_terms.pkl','wb') as f:
    pickle.dump(all_terms,f)

with open('term_df.pkl','wb') as f:
    pickle.dump(df,f)

