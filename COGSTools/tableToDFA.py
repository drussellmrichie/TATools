"""
Russell Richie 2016
github.com/drussellmrichie
drussellmrichie@gmail.com

Super klugey code to convert DFA transition tables to the format for DFA's required by 

http://ivanzuzak.info/noam/webapps/fsm2regex/
"""

import csv, os

path = "/Users/russellrichie/Google Drive/UConn/Teaching/COGS 2201 (Spring 2016)/Problem Set Answers"

os.chdir(path)

table = []

with open('currentTable.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        table.append(row)
        

#table = """
#	0	1
#Q0	Q3	Q1
#Q1	Q2	Q3
#Q2	Q2	Q1
#Q3	Q3	Q3
#"""

alphabet = table[0][1:]
states   = []
transitions = []

for row in table[1:]:                             # skip first row since it's a header row
    states.append(row[0])                         # put a new state into the states list
    for symbolIndex, symbol in enumerate(alphabet):
        transition = "{}:{}>{}".format(row[0], symbol, row[symbolIndex + 1])
        transitions.append(transition)
        
with open("DFATemplate.txt", 'w') as f:
    f.write("#states\n")
    for state in states:
        f.write(state)
        f.write("\n")
    f.write("#initial\n")
    f.write(states[0])
    f.write("\n")
    f.write("#accepting\n")
    f.write("#alphabet\n")
    for symbol in alphabet:
        f.write(symbol)
        f.write("\n")
    f.write("#transitions\n")
    for transition in transitions[:-1]:
        f.write(transition)
        f.write("\n")
    f.write(transitions[-1]) #do this one outside the loop so we don't write a new-line char at the end