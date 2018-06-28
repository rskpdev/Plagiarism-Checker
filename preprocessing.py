from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import pickle

def preproc(sr):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    punk = ['.',',','=','?','!','(',')','[',']','&','@','+','\'\'','#']
    #tokenise the document
    word_tokens = word_tokenize(sr)

    #remove stop-words
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    #removed punctuation marks
    clean_sentence = [''.join(c for c in s if c not in punk) for s in filtered_sentence]

    #remove empty characters
    clean_sentence = [s for s in clean_sentence if s] #for removal of empty tokens.

    #stemming using PorterStemmer
    stemmed_sentence = []
    for u in clean_sentence:
        stemmed_sentence.append(ps.stem(u))
    return stemmed_sentence

for i in os.listdir('./corpus'):
    #i is the filename in the 'corpus' directory
    f = open('./corpus/' + i,"r")

    #raw contents of the Wiki article in 'sr'
    sr = f.read()

    stemmed_sentence = preproc(sr)
    #serialize the list so generated.
    with open('./cleaned/' + i + '.pkl','wb') as f:
        pickle.dump(stemmed_sentence,f)
