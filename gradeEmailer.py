"""
Russell Richie, 2016
github.com/drussellmrichie
drussellmrichie@gmail.com

This is largely cribbed from Automate the Boring Stuff with Python:

https://automatetheboringstuff.com/chapter16/

This reads a table of graded stats HW's and send emails to students with just their graded
homework.

It expects an excel table structured like the below. And, usually, you'll have additional 
columns for individual questions, students' responses to such questions, and your 
grades/comments on such responses. But, such additional columns aren't strictly necessary 
for the script to work.

First Name     Last Name        Email                              Total
Total possible points                                              10
Russell        Richie           drussellmrichie@gmail.com          9.5
Student        McStudentFace    student.mcstudentface@uconn.edu    10
Current        Meme             current.meme@uconn.edu             9.75

NOTE: You have to modify a couple lines for your use case. These are indicated with 
comment blocks below.
"""

import os, smtplib, re
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ADJUST WORKING FOLDER FOR YOUR MACHINE
folder = '/Users/russellrichie/Google Drive/UConn/Teaching/PSYC5104 shared/PSYC5104 Fall 2016 homework submissions'
os.chdir(folder)

"""
MODIFY grades TO WHATEVER HW FILE YOU ARE GIVING FEEDBACK FOR
Note that the name of this file will go in the subject line of the email, so be sure it is 
appropriate for the students to see this file name.
"""
grades = 'Fall 2016 Psyc 5104 -  HW1 EMAIL_TEST.xlsx'
hw = pd.read_excel(grades)
#hwid = hw.ix[1,'HWID']
hwid = re.search('HW[0-9]+',grades).group(0)[2:]
print("Now starting to send students feedback for {}".format(grades))

# Start to setup some of the email-sending machinery
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()

"""
MODIFY EMAIL TO THE SENDER'S EMAIL (you, the grader, most likely). 
*THIS SCRIPT ASSUMES A GMAIL ADDRESS.*
"""
sender = 'YourEmailHere'

"""
MODIFY WITH YOUR GMAIL PASSWORD. You may have to generate a pw from here:
https://security.google.com/settings/security/apppasswords?pli=1

See also, this:
https://automatetheboringstuff.com/chapter16/#calibre_link-46
"""
pw = 'YourPasswordHere'

smtpObj.login(sender, pw)

totalPossible = hw.ix[0,'Total']

def sendEmail(submission):
    recipient = submission['Email']
    grade     = submission['Total']
    name      = submission['First Name'] + " " + submission['Last Name']
    
    msg = MIMEMultipart()
    msg['Subject'] = os.path.splitext(grades)[0] + ": " + "Feedback"
    msg['From'] = sender
    
    # I 'magic numbered' 10 below, but we could always put a column in the grading sheet 
    # for total possible points, and then extract that on a hw-by-hw basis. Probably 
    # safer, although I'm pretty sure all the stats hw's are out of 10 points?
    bodyString = '{}, you received {} points out of {} on hw {}. Open attached csv for more.'.format(name,
                                                                                                     grade,
                                                                                                     totalPossible,
                                                                                                     hwid)
    bodyMime = MIMEText(bodyString, 'plain')
    msg.attach(bodyMime)
    
    fileToSend = '{}HW{}.csv'.format(name,hwid)
    submission.to_frame().transpose().to_csv(fileToSend)

    with open(fileToSend) as fp:
        attachment = MIMEText(fp.read(), _subtype='csv')

    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend) 
    msg.attach(attachment)
    
    smtpObj.sendmail(sender,recipient, msg.as_string())
    
    # We don't really need these one-student csv's anymore, and they clutter up the folder, 
    # so just delete them
    os.remove(fileToSend)

hw.apply(sendEmail,axis=1)

smtpObj.quit()
print("All done sending students feedback for {}".format(grades))