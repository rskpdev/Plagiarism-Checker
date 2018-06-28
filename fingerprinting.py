import os
import pickle


def get_hash(doc, m, base):
    '''
        splits the document into k-grams and hashes the same into integer hash-values.
        The algorithms considers each window and uses dynamic programming to store the
        hash-values generated so far to calculate the hash of the surrent window.
    '''
    hash_val = []
    first = 0
    sub = 0
    add = m

    # get the hash-value of the first window.
    for i in range(0,m):
        first += ord(doc[i])*(base**(m-i-1))

    hash_val.append(first)

    # get the hash-value of subsequent windows by removing the first hash and adding
    # the next hash into the window
    for i in range(m,len(doc)-m):
        first = base*(first - ord(doc[sub])*(base**(m-1))) + ord(doc[add])
        hash_val.append(first)
        sub += 1
        add += 1

    return hash_val

def winnow(hash_val,w):
    '''
        Considers windows of the hash-values of each document. In each window the least
        hash-value is selected along with its position in the document and in case of
        clash, the hash-value which is rightmost, is selected.
    '''
    fingerprint = []
    prev = w-1
    # consider the first window.
    for i in range(w-1,-1,-1):
        if hash_val[i] < hash_val[prev]:
            prev = i

    d = prev #the position of the chosen hash_val in the window.

    # append the first window's smallest val to the fingerprint of the document.
    a = [hash_val[prev],d]
    fingerprint.append(a)

    r = w #right end of window
    l = 1 #left end of window
    co = 1 #count of the window under consideration

    while r < len(hash_val):
        # now consider the new entry to the window
        if hash_val[r] == hash_val[prev]:
            if (r-l) >= d:
                a = [hash_val[r],co+r-l]
                fingerprint.append(a)
                d = r-l
        else:
            if hash_val[r] < hash_val[prev]:
                prev = r
                d = r-l
                a = [hash_val[r],co+r-l]
                fingerprint.append(a)
            else: #the current minimum might have left the window
                if prev < l:
                    temp = r
                    prev = r
                    while temp >= l:
                        if hash_val[temp] < hash_val[prev]:
                            prev = temp
                        temp -= 1
                    d = prev - l
                    a = [hash_val[prev],co + d]
                    fingerprint.append(a)
        co += 1
        r += 1
        l += 1
    return fingerprint

# setting the window for the winnowing algorithm.
window = 5

# stores the fingerprints for each document.
fingerprints = {}

for i in os.listdir('./cleaned'):
    sr = []
    name = i.split(".")[0]
    with open('./cleaned/' + i, 'rb') as f:
        sr = pickle.load(f)
    doc = ''.join(sr)
    hash_val = get_hash(doc,5,10)
    #fingerprint is a list with each element of the form :
    #[hash-value selected,position in the doc].
    fingerprint = winnow(hash_val,window)
    fingerprints[name] = fingerprint

# save the generated fingerprints for each document.
with open('./fingerprints.pkl','wb') as f:
        pickle.dump(fingerprints,f)
