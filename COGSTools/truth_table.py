"""
Russell Richie, 2016
https://github.com/drussellmrichie
drussellmrichie@gmail.com

This first utilizes a hack I found on stackexchange to create new logical operators for the 
biconditional and material conditional.

Then, I built a function to build a partial truth table for complex propositions. It only has columns 
for the atoms and the complex proposition -- not for the intermediate propositions. Would have to parse
(with NLTK or something) complex proposition for that...

Then, a function for checking consistency among propositions, and another function for checking deductive
validity.

These functions are too complicated to ask COGS students to recreate from scratch....is there any way to 
provide students with pieces and ask them to fill them in a little bit, or answer questions about them?

Some or all of this could be improved by relying on NLTK's logic functionality.
"""

from itertools import product 

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

IFF   = Infix(lambda x,y: (x and y) or not (x or y))
THEN  = Infix(lambda x,y: not(x) or y)
AND   = Infix(lambda x,y: x and y)
OR    = Infix(lambda x,y: x or y)

def demo_truth_functions():
    print("Truth table for if and only if")
    print("True |IFF| True\n",True |IFF| True)
    print("True |IFF| False\n",True |IFF| False)
    print("False |IFF| True\n",False |IFF| True)
    print("False |IFF| False\n",False |IFF| False)

    print("\nTruth table for if-then (material conditional)")
    print("True |THEN| True\n",True |THEN| True)
    print("True |THEN| False\n",True |THEN| False)
    print("False |THEN| False\n",False |THEN| False)
    print("False |THEN| True\n",False |THEN| True)

def truth_table(proposition="((p |IFF| q) |THEN| r)"):
    """
    Function to build a truth table for proposition made up of atoms
    
    proposition: string boolean expression. atoms must be single, lower-case letters OTHER THAN
    'n','o', or 't', which are reserved for the negation operator 'not'
    
    """
    atom_tuple = tuple([symbol for symbol in proposition if (symbol.islower() 
                                                             and symbol not in {'n','o','t'}
                                                             )
                        ]
                       )
    
    truth_conditions = list(product((True, False), repeat=len(atom_tuple)))
    table = pd.DataFrame(truth_conditions, columns=atom_tuple)

    atom_string = ', '.join(atom_tuple)
    for index, row in table.iterrows():
        exec(atom_string + " =" + str(list(row)))
        table.ix[index,proposition] = eval(proposition)
    
    print("This is a truth table for", proposition)
    return table

def demo_truth_table():
    print(truth_table(proposition='((p |IFF| q) |THEN| r)'))

def consistency(*propositions):
    """
    Function to check whether propositions are consistent with each other (i.e., can all be
    true at the same time.)
    
    propositions: string(s), like '((p |IFF| q) |THEN| r)'
    
    atomic propositions represented with lower-case letters, EXCEPT 'n','o', and 't', which
    are reserved for the negation operator 'not'
    """
    
    atom_set = {symbol for symbol in ''.join(propositions) if (symbol.islower() 
                                                               and symbol not in {'n','o','t'}
                                                               )
                }
    atom_tuple = sorted(tuple(atom_set))                   
    
    truth_conditions = list(product((True, False), repeat=len(atom_tuple)))
    table = pd.DataFrame(truth_conditions, columns=atom_tuple)

    atom_string = ', '.join(atom_tuple)
    
    for index, row in table.iterrows():
        exec(atom_string + " =" + str(list(row)))
        for prop in propositions:
            table.ix[index,prop] = eval(prop)
    
    table.set_index(list(atom_tuple), inplace=True)
    table['all true?'] = table.apply(all,axis=1)
    table.reset_index(inplace=True)
    
    if any(table['all true?']):
        print("\nThese propositions are consistent. There is at least one True in "
              "'all true?' column of table.")
    else:
        print("\nThese propositions are not consistent. There is no True in 'all true?' "
              "column of table.")
    
    return table

def demo_consistency():
    print(consistency('not (p |AND| q)', 
                      '(p |OR| r)',
                      'not(r |IFF| q)'
                      )
          )
    
def validity(conclusion='q', premises=['p |THEN| q', 'p']):
    """
    Function to check whether conclusion is entailed by premises, via truth-table method.
    
    conclusion: string, like '((p |IFF| q) |THEN| r)'
    premises: string(s), like '((p |IFF| q) |THEN| r)'
    
    atomic propositions represented with lower-case letters, EXCEPT 'n','o', and 't', which
    are reserved for the negation operator 'not'
    """
    all_statements = premises + [conclusion]
    
    atom_set = {symbol for symbol in ''.join(all_statements) if (symbol.islower() 
                                                                and symbol not in {'n','o','t'}
                                                                 )
                }
    atom_tuple = sorted(tuple(atom_set))                   
    
    truth_conditions = list(product((True, False), repeat=len(atom_tuple)))
    table = pd.DataFrame(truth_conditions, columns=atom_tuple)

    atom_string = ', '.join(atom_tuple)
    
    for index, row in table.iterrows():
        exec(atom_string + " =" + str(list(row)))
        for prop in all_statements:
            table.ix[index,prop] = eval(prop)
    
    # now check rows where premises are true...is conclusion true?
    table['premises true?'] = table[premises].apply(all,axis=1)
    true_premises = table[table['premises true?']]
    
    # rename columns to clearly indicate premises and conclusion
    renaming_dict = {premise: 'P' + str(prem_numb) + ':' + premise 
                     for prem_numb, premise 
                     in enumerate(premises)
                     }
    renaming_dict[conclusion] = 'C:' + conclusion
    table.rename(columns=renaming_dict, inplace=True)
    
    # now sort -- best would be atoms, premises, 'premises true?', conclusion...but when atoms
    # are premises or conclusions....not sure how that'd work....
    table.sort_index(axis=1, ascending=False, inplace=True)
    
    if all(true_premises[conclusion]):
        print("\nThe premises entail the conclusion. When the premises are true, "
              "the conclusion is true.")
    else:
        print("\nThe premises do not entail the conclusion. There is at least one"
              "setting of truth conditions where the premises are true and the "
              "conclusion false.")

    return table    

def demo_validity():
    print(validity(conclusion='q |OR| r', 
                   premises=['p |THEN| q', 'p', 'r']
                   )
          )
    print(validity(conclusion='p', 
                   premises=['p |THEN| q', 'q']
                   )
          )
    
if __name__ == '__main__':
    demo_truth_functions()
    demo_truth_table()
    demo_consistency()
    demo_validity()
