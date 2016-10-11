"""
Russell Richie 2016
github.com/drussellmrichie
drussellmrichie@gmail.com

This allows evaluation of students' answers for excitatory and inhibitory weights such 
that an output neuron does and doesn't fire given certain conditions. Can easily be 
modified according to those conditions.
"""

import pandas as pd
import os
import matplotlib.pyplot as plt 
plt.style.use('ggplot')


# will use chain function to compute powerset, which will let us look at different 
# combinations of activation of input neurons in problem 5
from itertools import chain, combinations

currDir = '/Users/russellrichie/Google Drive/UConn/Teaching/COGS 2201 (Spring 2016)/Problem Set Student Submissions/PS4'
os.chdir(currDir)

responsesFile = 'COGS 2201 -- Problem Set 4 -- Student Submission Form (Responses) - Form Responses 1.xlsx'

responses = pd.read_excel(responsesFile)
responses = responses[['First name', 'Last name', '5a','5b','5c','5d','5e','5f']]

"""
Will give half credit for giving proper excitatory weights on a, c, and d such that z just
fires when a, c, and d are firing (i.e., doesn't fire when a, c, or d fire alone or in 
just pairs).

Will give the other half credit for giving proper inhibitory weights on b, e, and f such 
that z DOESN'T FIRE when b, e, or f are firing. (i.e., even if a, c, and d are firing, any 
single inhibitory neuron firing should stop z from firing)
"""

excNeurons = ['5a','5c','5d']
inhNeurons = ['5b','5e','5f']
zThresh = 1.0

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# I know using iterrows is generally considered....sloppy?...but it was the first solution 
# that came to my mind, and I ain't here to be elegant

grades = []
for row in responses.iterrows():
    grade = 0
    
    """
    Row is an (index, Series)-tuple, and we just want the Series with the data/answers
    """
    row = row[1]
    
    """
    On next line, skip first and last because these are empty and all three neurons, 
    respectively (and we do want all three neurons together to fire off Z, i.e. we want 
    those three to work)
    """
    badExcNeuronCombos = list(powerset(excNeurons))[1:-1]
    
    """
    The next group of lines basically does the following: 
    if all bad excitatory neuron combos are below Z's threshold AND 
    the good combo is ABOVE threshold, then the person gets half a point
    """
    badComboPassage = True
    for badCombo in badExcNeuronCombos:
        badCombo = list(badCombo) # because apparently can only slice pd.Series with lists?
        if sum(row[badCombo]) > zThresh:
            badComboPassage = False
            break
    if (badComboPassage == True) and (sum(row[excNeurons]) > zThresh):
        grade = 0.5
    """
    Now check, for every inhibitory neuron, whether firing that neuron makes Z's input fall 
    back below threshold. If so, they get another 0.5 points
    """
    inhCheck = True
    for inhNeuro in inhNeurons:
        if (sum(row[excNeurons]) + row[inhNeuro]) > zThresh:
            inhCheck = False
            break
    if inhCheck == True:
        grade += 0.5
    
    grades.append(grade)

# Again, if I were a real pandas guru / were taking my time, I probably could have 
# figured out a way to use the apply method to directly go from their answers to 5a-f to 
# a grade....
responses['5_grade'] = grades

# Can now just copy and paste the '5_grade' column back into the excel sheet where you're
# grading....OR, you could edit the excel sheet programmatically.