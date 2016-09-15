"""
Russell Richie, 2016

This is cribbed from Automate the Boring Stuff with Python:

https://automatetheboringstuff.com/chapter16/

This reads a table of graded stats HW's and send emails to students with just their graded homework.

It expects an excel table structured like so. And, usually, you'll have additional columns for individual questions, students'
responses to such questions, and your grades/comments on such responses. But, such additional columns aren't strictly necessary 
for the script to work.

First Name     Last Name     Email                         Total_points
Russell        Richie        drussellmrichie@gmail.com     9.5
Eric           Lundquist     eric.lundquist@uconn.edu      10
Henry          Harrison      henry.harrison@uconn.edu      9.75
"""

import os, smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ADJUST FOLDER FOR YOUR MACHINE
folder = '/Users/russellrichie/Google Drive/UConn/Teaching/PSYC5104 shared/PSYC5104 Fall 2016 homework submissions'
os.chdir(folder)

# MODIFY GRADES TO WHATEVER HW FILE YOU ARE GIVING FEEDBACK FOR
grades = 'Fall 2016 Psyc 5104 -  HW1 EMAIL_TEST.xlsx'
hw = pd.read_excel(grades)
hwid = hw.ix[1,'HWID']
print("Now starting to send students feedback for {}".format(grades))

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()

# MODIFY EMAIL TO THE SENDER'S EMAIL (you, the grader, most likely). THIS SCRIPT ASSUMES A GMAIL ADDRESS.
sender = 'senderEmailHere'

# MODIFY YOUR GMAIL PASSWORD. You may have to generate a pw from here:
# https://security.google.com/settings/security/apppasswords?pli=1
pw = 'MyPasswordHere'

smtpObj.login(sender, pw)

def sendEmail(submission):
    recipient = submission['Email']
    grade     = submission['Total_points']
    name      = submission['First Name'] + " " + submission['Last Name']
    
    msg = MIMEMultipart()
    msg['Subject'] = 'Psyc 5104 -- Feedback on HW{} attached'.format(hwid)
    msg['From'] = sender
    
    bodyString = '{}, you received {} points out of 10 on hw {}. Open attached csv for more'.format(name,
                                                                                                    grade,
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

hw.apply(sendEmail,axis=1)

smtpObj.quit()
print("All done sending students feedback for {}".format(grades))