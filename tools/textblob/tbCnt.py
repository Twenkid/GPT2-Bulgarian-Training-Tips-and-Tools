# Basic tutorial: https://textblob.readthedocs.io/en/dev/quickstart.html
# Twenkid:
# + from textblob.blob import WordList
# + some intermediate variables, scan a dir, count, print
# Word (token) frequency
# Very slow query of the counts from the textblob? # 28.7.2021
# It seems b: TextBlob(...); counts[w] = b.words.count(w) is very slow: ~ 84 items/s in one run/i5 6500.
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
fo = open("outblob.txt", "wt", encoding='utf-8')
for filename in paths:
   with open(filename, "r", encoding='utf-8') as f:   
     x = f.read()     
     texts[filename] = x          
     b = TextBlob(x)
     blobs[filename] = b
     print(b.word_counts['кола'])
     print(len(b.word_counts))
     #b.words.count('ekki', case_sensitive=True)
     counts = {} #Clear
     #for w in b.words.keys()[:100]: #no
     #for w in b.words[:100]:
     #dict(sorted(x.items(), key=lambda item: item[1]))
     #for w in sorted(b.words, reverse=True)[:100]:
     n=0     
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
     fo.write(output)
fo.close()      

#exit(0)