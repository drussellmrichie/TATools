"""
Russell Richie
github.com/drussellmrichie
drussellmrichie@gmail.com

This script generates sentences in statement logic using a simple context-free grammar. It also generates
natural English sentences from SL frames and a handful of simple atomic English sentences. Right now, some
of the generated English sentences are ambiguous because of lack of punctuation, etc. Initially, I was 
thinking this was a 'bug', but maybe it's a feature, as we could ask students to give SL formulations for 
each possible interpretation of an ambiguous English sentence...

It would be good to then ask students to translate these English sentences back into SL. THEN, it would be 
nice to make a sister script that takes students' SL sentences, and attempt to parse and grade them. The 
beginnings of such a sister script are contained in equivalenceAndDeduction.py.

NOTE-TO-SELF: Clean up/scrap unused code at some point.
"""

import re
import nltk
import random
from nltk import CFG
from nltk.parse.generate import generate

logicalGrammar = """
S   -> '(' '-' S ')'
S   -> '(' S '&' S ')'
S   -> '(' S '|' S ')'
S   -> '(' S '->' S ')'
S   -> '(' S '<->' S ')'
S   -> 'P'
"""

logicalGrammar = CFG.fromstring(logicalGrammar)
complexLogicalSents = [' '.join(x) for x in generate(logicalGrammar, depth=4)]

for sent in complexLogicalSents[:10]:
    print(sent)

englishGrammar = """
S   -> 'it is not the case that' S 
S   -> S 'and' S ','
S   -> S 'or' S ','
S   -> 'if' S ', then' S ','
S   -> 'if' S ', only then' S ','
"""

#grammar += """
#S   -> 'P'
#"""
#extraLetters = """
#S   -> 'Q'
#S   -> 'R'
#"""

englishGrammar += """
S   -> 'Dogs chase cats'
S   -> 'Cats chase mice'
S   -> 'Mice eat cheese'
S   -> 'Cheese disappears'
"""

"""
statements = [
    'Dogs chase cats',
    'Dogs play',
    'Dogs sit',
    'Cats chase mice',
    'Cats play with toys',
    'Cats sleep',
    'Mice eat cheese',
    'Mice scurry',
    'Mice squeak',
    'Cheese disappears'
    ]
"""
englishGrammar = CFG.fromstring(englishGrammar)

complexEnglishSents = [' '.join(x) for x in generate(englishGrammar, depth=4)]

for sent in complexEnglishSents[:10]:
    print(sent)
#complexEnglishSents = [re.sub('[A-Z]',random.choice(statements),x) for x in complexLogicalSents]

"""
# unfortunately, the immediately above list comp uses the SAME random choice for every atom within
# a complex sentence. So you always get things like "(Dogs play & Dogs play) -> Dogs play". The below
# hack job was the workaround that immediately came to mind, but there must be a more elegant way...
complexEnglishSents = []
for logicalSent in complexLogicalSents:
    engSent = str(logicalSent)
    for _ in re.findall('P',logicalSent):
        engSent = re.sub('P',random.choice(statements),engSent, count=1)
    complexEnglishSents.append(engSent)

# now replace logical connectives with english connectives

log2EngConns = dict(
    '&':'and',
    '|':'or',
    '<->':'if and only if',
    '-','it is not the case that'
    )
"""
# I think the below isn't necessary because nltk has nice propositional logic functionality. Although
# seeing the tree is nice, potentially....
"""
parser = nltk.ChartParser(pureGrammar)

sent = '~ ( ( P & P ) > P )'
tree = parser.parse_one(sent.split())
tree.draw()
"""