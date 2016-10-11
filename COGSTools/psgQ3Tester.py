__author__ = 'russellrichie'

import re, nltk
from nltk import CFG
from nltk.tree import *
from nltk.draw import tree
import matplotlib.pyplot as plt
grammar = """

S -> NP VP
NP -> D N
NP -> NP CP
CP -> C VP
VP -> V NP

D -> "the"
N -> "pirate" |  "captain"
V -> "pursued" | "scared" |  "chased"
C -> "that"

"""

#grammar = re.sub(pattern = '([A-z]{3,})', repl ="\\1".lower(), string = grammar)
#grammar = re.sub(pattern = '([A-z]{4,})', repl = lambda m: m.group(0).lower(), string = grammar)
#grammar = re.sub(pattern = '([A-z]{3,})', repl = '\"\\1\"', string = grammar)
#grammar = re.sub(pattern = '"start"', repl = "START", string = grammar)

grammar = CFG.fromstring(grammar)
parser = nltk.ChartParser(grammar)

sents =     [
    'the captain pursued the pirate',
    'the pirate pursued the captain',
    'the pirate scared the pirate',
    'the pirate that scared the captain chased the pirate',
    'the captain that scared the pirate chased the captain',
    'the pirate chased the captain that scared the pirate',
    'the captain that scared the pirate that chased the pirate scared the pirate that chased the captain'
            ]

badSents =  [
    'scared the captain',
    'pirate chased the captain',
    'the pirate that chased the captain',
    'the pirate the scared the captain chased the captain',
    'the captain chased the pirate scared the pirate',
    'the captain scared the pirate chased'
            ]

print "Should do these"
for sent in sents:
    print "\n" + sent
    if any(parser.parse(sent.split())):
        print "Yes, the grammar generates this."
    else:
        print "No, the grammar does not generate this."

print "\n \n \nShould not do these"
for sent in badSents:
    print "\n" + sent
    if any(parser.parse(sent.split())):
        print "Yes, the grammar generates this."
    else:
        print "No, the grammar does not generate this."

sent = 'the captain that scared the pirate scared the pirate that chased the captain'

tree = parser.parse(sent.split())

# now that I'm in NLTK 3.0, the parse method returns a generator rather than a list of parses, in true Python 3.0
# style
tree.next().draw()
