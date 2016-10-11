"""
Russell Richie
github.com/drussellmrichie
drussellmrichie@gmail.com

This script reads a csv of doodle poll responses of students availability to attend office
hours, and finds the set of office hours dates/times that maximize the number of students
that can attend at least one.

This should most definitely be cleaned-up/refactored at some point
"""

import pandas as pd
import os, itertools

os.chdir('/Users/russellrichie/Google Drive/UConn/Teaching/Spring 2016 Cogs 2201 TAship')

"""
Before reading in the doodle csv, go to administration tab of the doodle poll and
export to csv. Then, eliminate the top few rows so the dates are on the top row. Then, fill
out the top cells so each column has a date at the top.
"""

doodle = pd.read_csv('officeHoursDoodle.csv', header=[0,1], index_col = 0)
doodle.drop('Count', inplace=True)
doodle.drop_duplicates(inplace=True)

officeHoursDict = dict()
numOfficeHours = 2  # right now the below loop can only handle numOfficeHours = 2, but it
                    # could be modified to handle an arbitrary number of office hours

"""
For every pair of columns
    compute the union of names that have 'OK' in the columns
    Save the size of the union

"""

for col1, col2 in itertools.combinations(doodle.iteritems(), numOfficeHours):
    col1Yes = col1[1].dropna()  # dropping rows with NaN is an easy way to just get those
                                # names that can attend that particular day/time
    col2Yes = col2[1].dropna()
    yesUnion = set(col1Yes.index).union(set(col2Yes.index))
    yesUnionSize = len(yesUnion)
    
    dayTime1 = col1[0]
    dayTime2 = col2[0]
    officeHoursDict[(dayTime1,dayTime2)] = yesUnionSize

# Now sort the pairs of days and times in officeHoursDict by value. The pairs at the end
# enable the most students to attend at least one office hour session

possible = sorted(officeHoursDict.items(), key=(lambda key: key[1]))

# Now remove Mondays (these became impossible for me since I created the Doodle) and make
# sure a Tuesday is in there (Tuesdays are the most consistently free day for me)

newPoss = []

for pair in possible:
    if (pair[0][0][0][:3] == 'Tue' or pair[0][1][0][:3] == 'Tue') and pair[0][0][0][:3] != 'Mon' and pair[0][1][0][:3] != 'Mon':
        newPoss.extend(pair)

# I ultimately chose the second best pair in this final list, as the Wed 3-5 time was not
# consistently available for me