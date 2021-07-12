# Original: https://textblob.readthedocs.io/en/dev/quickstart.html
# + from textblob.blob import WordList
# + some intermediate variables and print by Twenkid 12.7.2021
# It requires to download also the NLTK corpora in order to run properly:
# python -m textblob.download_corpora

from textblob import TextBlob
wiki = TextBlob("Python is a high-level, general-purpose programming language.")
from textblob import TextBlob

wiki = TextBlob("Python is a high-level, general-purpose programming language.")
wiki.tags
wiki.noun_phrases
testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
testimonial.sentiment
testimonial.sentiment.polarity
zen = TextBlob("Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex.")
print(zen.words)
print(zen.sentences)
for sentence in zen.sentences:
  print(sentence.sentiment)
sentence = TextBlob('Use 4 spaces per indentation level.')
sentence.words
sentence.words[2].singularize()
sentence.words[-1].pluralize()
from textblob import Word
w = Word("octopi")
lem = w.lemmatize()
print(w.lemmatize())
#'octopus'
w = Word("went")
l = w.lemmatize("v") 
print(l)
#WordNet Integration

#You can access the synsets for a Word via the synsets property or the get_synsets method, optionally #passing in a part of speech.

from textblob import Word
from textblob.wordnet import VERB
word = Word("octopus")
print(word.synsets)
#[Synset('octopus.n.01'), Synset('octopus.n.02')]
print(Word("hack").get_synsets(pos=VERB))
#[Synset('chop.v.05'), Synset('hack.v.02'), Synset('hack.v.03'), Synset('hack.v.04'), Synset('hack.v.05'), Synset('hack.v.06'), Synset('hack.v.07'), Synset('hack.v.08')]
print(Word("octopus").definitions)
#['tentacles of octopus prepared as food', 'bottom-living cephalopod having a soft oval body with eight long tentacles']

from textblob.wordnet import Synset
from textblob.blob import WordList #if missing --> NameError: name 'WordList' is not defined
octopus = Synset('octopus.n.02')
shrimp = Synset('shrimp.n.03')
print(octopus.path_similarity(shrimp))
#0.1111111111111111
animals = TextBlob("cat dog octopus")
print(animals.words)
w = WordList(['cat', 'dog', 'octopus'])
print(WordList(['cat', 'dog', 'octopus']))
print(animals.words.pluralize())
print(WordList(['cats', 'dogs', 'octopodes']))
b = TextBlob("I havv goood speling!")
print(b.correct())
#I have good spelling!
from textblob import Word
w = Word('falibility')
print(w.spellcheck())
#[('fallibility', 1.0)]
monty = TextBlob("We are no longer the Knights who say Ni. We are now the Knights who say Ekki ekki ekki PTANG.")
n1 = monty.word_counts['ekki']
n2 = monty.words.count('ekki')
n3 = monty.words.count('ekki', case_sensitive=True)
print(n1,n2,n3)
n4 = wiki.noun_phrases.count('python')
print(n4)
b = TextBlob("And now for something completely different.")
print(b.parse())
print(zen[0:19])
print(zen.upper())
print(zen.find("Simple"))
#TextBlob("BEAUTIFUL IS BETTER THAN UGLY. EXPLICIT IS BETTER THAN IMPLICIT. SIMPLE IS BETTER THAN COMPLEX.")
apple_blob = TextBlob('apples')
banana_blob = TextBlob('bananas')
s1 = apple_blob < banana_blob
print(s1)
#True
s2 = apple_blob == 'apples'
print(s2)
#True
s3 = apple_blob + ' and ' + banana_blob
print(s3)
TextBlob("apples and bananas")
s4 = "{0} and {1}".format(apple_blob, banana_blob)
print(s4)
#'apples and bananas'
blob = TextBlob("Now is better than never.")
ng = blob.ngrams(n=3)
print(ng)
#[WordList(['Now', 'is', 'better']), WordList(['is', 'better', 'than']), WordList(['better', 'than', 'never'])]
for s in zen.sentences:
  print(s)
  print("---- Starts at index {}, Ends at index {}".format(s.start, s.end))
