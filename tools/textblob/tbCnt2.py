# Basic tutorial: https://textblob.readthedocs.io/en/dev/quickstart.html
# Twenkid:
# + from textblob.blob import WordList
# + some intermediate variables, scan a dir, count, print
# Word (token) frequency
# Very slow query of the counts from the textblob? # 28.7.2021
# It seems b: TextBlob(...); counts[w] = b.words.count(w) is very slow: ~ 84 items/s in one run/i5 6500.
# Solved with NLTK
# Then some collecting, sorting etc.
# Sort: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value 

from textblob import TextBlob
from textblob.blob import WordList #if missing --> NameError: name 'WordList' is not defined

#wiki = TextBlob("Python is a high-level, general-purpose programming language.")
#wiki = TextBlob("Python is a high-level, general-purpose programming language.")
#print(wiki.tags)
#print(wiki.noun_phrases)
#w = WordList(['python'])
#print(w)

from pathlib import Path
import os
import random
#paths = [str(x) for x in Path("Z:\\19-7-corpus\\").glob("*.txt")] 
paths = [str(x) for x in Path("Z:\\small\\").glob("*.txt")] 
texts = {}
blobs = {}
counts = {}
sortedCounts = {}
output = ''
curr = ''
fo = open("outnltk.txt", "wt", encoding='utf-8')


import nltk
from nltk.corpus import webtext
from nltk.probability import FreqDist
     
#nltk.download('webtext') 
## Let's take the specific words only if their frequency is greater than 3.
#filter_words = dict([(m, n) for m, n in data_analysis.items() if len(m) > 3])
 
#for key in sorted(filter_words):
#    print("%s: %s" % (key, filter_words[key]))
 
#data_analysis = nltk.FreqDist(filter_words) 
#data_analysis.plot(25, cumulative=False)


for filename in paths:
   with open(filename, "r", encoding='utf-8') as f:   
     x = f.read()     
     texts[filename] = x          
     b = TextBlob(x)
     blobs[filename] = b
     print(b.word_counts['кола'])
     print(len(b.word_counts))
     #b.words.count('ekki', case_sensitive=True)
     analysis = nltk.FreqDist(b.words) 
     analysis.plot(100, cumulative=False)
     curr = ''
     for w in sorted(analysis): #alphabet     
       curr+=w + "\t" + str(analysis[w]) + "\n"  
       counts[w] = analysis[w]
     #sortedCounts = dict(sorted(counts, key=lambda item: item[1]))
     sortedCounts = dict(sorted(analysis.items(), key=lambda item: item[1]))
     for w in sortedCounts: #alphabet
       curr+=w + "\t" + str(sortedCounts[w]) + "\n"  
     
     fo.write(curr) #output += curr
     #OK!
'''     
     counts = {} #Clear
     #for w in b.words.keys()[:100]: #no
     #for w in b.words[:100]:
     #dict(sorted(x.items(), key=lambda item: item[1]))
     #for w in sorted(b.words, reverse=True)[:100]:
     n=0
     #b.words.sort() - but not by freq
     for w in b.words:         
       counts[w] = b.words.count(w)
       print(n,w,end=','); n+=1
       #output+=w + "\t" + str(b.words.count(w)) + "\n"
       #print(str(w) +"\t" + str(b.words.count(w)) + "\n")
       #print(w, b.words.count(w))
     sortedCounts = dict(sorted(counts.items(), key=lambda item: item[1]))
     print("\nSORTED?",len(sortedCounts))
     curr = ''
     for w in sortedCounts:
       #curr+=w + "\t" + str(b.words.count(w)) + "\n"
       curr+=w + "\t" + str(sortedCounts[w]) + "\n"
     print(curr)
     output += curr
'''
               
fo.close()      

#exit(0)