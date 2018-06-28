import wikipedia

l = ['Data Mining', 'Machine Learning', 'Neural Networks']

for i in l:
    f = open('./corpus/' + i + '.txt','wt')
    p = wikipedia.page(i).content
    f.write(p)
