"""
Russell Richie
github.com/drussellmrichie
drussellmrichie@gmail.com

***VERY MUCH A WORK-IN-PROGRESS.*** I may refactor (e.g., pack things into functions) later.

This takes a sentence in statement logic (a student's submission), and checks its equivalence against 
another statement (the answer key).

It can handle submissions that use different atoms from the answer key, by creating a set of all the
possible atom:atom mappings from submission to answer, and then checking equivalence for all of those.

I think ultimately we'll want to (as Iris and I agreed) flag ill-formed and non-equivalent submissions so 
that the TA can manually check them and try to assign partial credit? The nice thing about read_expr is 
that, if the formula is ill-formed, it tells you what went wrong. So, we can catch 
`LogicalExpressionException` where the formula is ill-formed and flag those.

Also demonstrates the use of a theorem prover to check a few deductions in SL.
"""

from nltk import *
from nltk.sem import Expression
from itertools import permutations

read_expr = Expression.fromstring

submission = 'Q | -P'
answer     = 'P -> Q'

a = read_expr(submission)
b = read_expr(answer)
# if don't specify prover, Python tries to use Prover9, which it has trouble finding on my machine
print(a.equiv(b, prover = TableauProver()))

# On to catching the equivalence of 'P -> Q' and 'R | -S'.

submission = '(P -> Q) & M'
answer = '(R | -S) & N'

#submission = 'P & Q'
#answer     = 'R & S'

submission_letters = {x for x in submission if x.isalpha()}
answer_letters     = {x for x in answer if x.isalpha()}

mappingDicts = [dict(zip(submission_letters, x)) for x in permutations(answer_letters)]
answerExpr = read_expr(answer)
for mappingDict in mappingDicts:
    mappedSubmission = ''.join(mappingDict.get(char, char) for char in submission)
    mappedSubExpr = read_expr(mappedSubmission)
    if answerExpr.equiv(mappedSubExpr, prover = TableauProver()):
        print('Equivalent under submission:answer mapping:', mappingDict)

# check some simple inferences...`verbose = True` shows the truth tree!

# VALID
p1 = read_expr('P -> Q')
p2 = read_expr('P')
c  = read_expr('Q')
print(TableauProver().prove(c,[p1,p2], verbose=True))

# NOT VALID
p1 = read_expr('P -> Q')
p2 = read_expr('Q')
c  = read_expr('P')
print(TableauProver().prove(c,[p1,p2], verbose=True))

# slightly more complex, but still VALID inference
p1 = read_expr('P -> Q')
p2 = read_expr('(P -> Q) -> (S | R)')
p3 = read_expr('-R')
c  = read_expr('S')
print(TableauProver().prove(c,[p1,p2,p3], verbose=True))

"""
Interesting thing about the tableau prover is that it fully decomposes sentences before looking for 
contradictions -- in this case, once it had deduced -(P -> Q) and later (P -> Q), it could have closed 
the branch, but it instead decomposed (P -> Q) into branches for -P and Q, and then found contradictions
between these atoms and earlier deductions.
"""