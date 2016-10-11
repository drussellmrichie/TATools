__author__ = 'russellrichie'

import nltk, re
from nltk import CFG
import matplotlib.pyplot as plt

grammar = """

start -> 'a' S1
start -> 'a' S2
start -> 'a' S3
S1 -> 'really' S2
S2 -> 'really' S2
S2 -> 'tall' S3
S3 -> 'tree' S4
S4 -> 'fell'

"""

#grammar = re.sub(pattern = '([A-z]{3,})', repl = lambda m: m.group(0).lower(), string = grammar)
#grammar = re.sub(pattern = '([A-z]{3,})', repl = '\"\\1\"', string = grammar)
#grammar = re.sub(pattern = '"start"', repl = "START", string = grammar)

grammar = CFG.fromstring(grammar)
parser = nltk.ChartParser(grammar)

sents = [
    'a tree fell',
    'a tall tree fell',
    'a really tall tree fell',
    'a really really tall tree fell',
    'a really really really tall tree fell'
    ]

badSents = [
    'tree fell',
    'a fell',
    'a really tree fell',
    'really tall tree fell',
    'really a tall tree fell',
    'a tall really tree fell'
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