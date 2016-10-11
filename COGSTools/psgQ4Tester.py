__author__ = 'russellrichie'

import nltk, re
from nltk.tree import *
from nltk.draw import tree
from random import choice
from nltk import CFG

"""
Paste the students' grammar between the quotes below. Use the site below to turn

http://textmechanic.com/Find-and-Replace-Text.html

"""

grammar = """

CP  -> VP DP PP
VP  -> V
DP  -> D NP
PP  -> P DP
PP  -> P DP PP
NP  -> N
PP  -> P DP
V  -> "put"
D  -> "the"
N  -> "table"
N  -> "box"
N  -> 'apple'
P  -> 'on'
P  -> 'near'

"""

#grammar = re.sub(pattern = '([A-z]{3,})', repl = lambda m: m.group(0).lower(), string = grammar)
#words = ['put','the','apple','box','near','on','table']
#grammar = re.sub(pattern = '([A-z]{3,})', repl = '\"\\1\"', string = grammar)
#grammar = re.sub(pattern = '"start"', repl = "START", string = grammar)

grammar = CFG.fromstring(grammar)
parser = nltk.ChartParser(grammar)

sent = 'put the box on the apple near the table'

tree = parser.parse(sent.split())

# If using NLTK 3.0, use this line. The parse method returns a generator rather than a list of parses, in true
# Python 3.0 style
tree.next().draw()

# if using NLTK 2.x, use this next block
# need this if statement because there may be more than one tree in 'tree'
# if tree is a list of trees, then just draw the first one. Otherwise,
# draw the only tree there is!
"""
if type(tree) == list:
    tree[0].draw()
else:
    tree.draw()
"""

