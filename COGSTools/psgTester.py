__author__ = 'russellrichie'

import nltk, re

# grammar = nltk.parse_cfg("""
# Start -> 'the' 'captain' S1
# Start -> 'the' 'pirate' S1
# S1 -> 'pursued' S2
# S1 -> 'scared' S2
# S1 -> 'chased' S2
# S1 -> 'that' S3
# S2 -> 'the' 'captain' END
# S2 -> 'the' 'pirate' END
# S2 -> 'the' 'captain'
# S2 -> 'the' 'pirate'
# S3 -> 'scared' S4
# S3 -> 'chased' S4
# S3 -> 'pursued' S4
# S4 -> 'the' 'captain' S5
# S4 -> 'the' 'pirate' S5
# END -> 'that' S6
# S6 -> 'scared' S7
# S6 -> 'chased' S7
# S6 -> 'pursued' S7
# S7 -> 'the' 'pirate' S8
# S7 -> 'the' 'captain' S8
# """)

grammar = """

Start    ->	The	S1
S1    ->	Pirate	S3
S1    ->	Captain	S2
S2    ->	Pursued	S4
S2    ->	That	S6
S3    ->	Scared	S4
S3    ->	Pursued	S4
S3    ->	That	S6
S3    ->	Chased	S9
S4    ->	The pirate
S4    ->	The captain
S6    ->	Scared	S7
S7    ->	The pirate	S8
S7    ->	The captain	S8
S8    ->	Chased	S4
S9    ->	The captain	S10
S10    ->	That scared	S4
S12    ->	That chased	S13
S13    ->	The pirate	S14
S14    ->	Scared	S15
S15    ->	The pirate	S16
S16    ->	That	S8

"""

#grammar = re.sub(pattern = '([A-z]{3,})', repl ="\\1".lower(), string = grammar)
grammar = re.sub(pattern = '([A-z]{3,})', repl = lambda m: m.group(0).lower(), string = grammar)
grammar = re.sub(pattern = '([A-z]{3,})', repl = '\"\\1\"', string = grammar)
grammar = re.sub(pattern = '"start"', repl = "START", string = grammar)

grammar = nltk.parse_cfg(grammar)

#print grammar

# grammar = nltk.parse_cfg("""
# S -> NP VP
# NP -> D N
# NP -> NP CP
# CP -> C VP
# VP -> V NP
# D -> "the"
# N -> "pirate"
# N -> "captain"
# V -> "pursued"
# V -> "scared"
# V -> "chased"
# C -> "that"
# """)

#sent = ["the captain", "that", "pursued", "the pirate", "pursued" ,"the pirate"]
#sent = 'the captain pursued the pirate'.split()
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

#parser = nltk.RecursiveDescentParser(grammar)
parser = nltk.ChartParser(grammar)
print "Should do these"
for sent in sents:
    print "\n" + sent
    if any(parser.nbest_parse(sent.split())):
        print "Yes, the grammar generates this."
    else:
        print "No, the grammar does not generate this."
#    for p in parser.nbest_parse(sent.split()):
#       #print p
#        if p:
#            print "Yes, the grammar generates."
#        else:
#            print "No, the grammar does not generate."

print "\n \n \nShould not do these"
for sent in badSents:
    print "\n" + sent
    if any(parser.nbest_parse(sent.split())):
        print "Yes, the grammar generates this."
    else:
        print "No, the grammar does not generate this."
#    print sent
#    for p in parser.nbest_parse(sent.split()):
#        #print p
#        if p:
#            print "Yes, the grammar generates."
#        else:
#            print "No, the grammar does not generate."

# grammar = nltk.parse_cfg("""
#  S -> NP VP
#  VP -> V NP | V NP PP
#  V -> "saw" | "ate"
#  NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
#  Det -> "a" | "an" | "the" | "my"
#  N -> "dog" | "cat" | "cookie" | "park"
#  PP -> P NP
#  P -> "in" | "on" | "by" | "with"
#  """)
#
# sent = "Mary saw Bob".split()
# rd_parser = nltk.RecursiveDescentParser(grammar)
# for p in rd_parser.nbest_parse(sent):
#       print p
# #(S (NP Mary) (VP (V saw) (NP Bob)))