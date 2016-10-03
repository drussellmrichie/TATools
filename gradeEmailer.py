"""Usage:
  gradeEmailer.py [--name=NAME] [--password=PASSWORD] [--dry-run] <sender-email> <grades-path>

Options:
  --name=NAME           The name of the grader.
                        Used in the signature and From field of the email.
                        If not given, <sender-email> will be used.
  --password=PASSWORD   The password to the sender's email account.
                        If not given, it will be prompted for.
  --dry-run             To test, send emails to yourself instead of to the students.

This reads a table of graded homeworks and emails each student their grade and feedback.

It expects a CSV or XLS/XLSX file at <grades-path> structured like the example below.
Usually, you'll have additional columns for individual questions, students' responses to such questions,
and your grades/comments on such responses.
However, these additional columns aren't strictly necessary for the script to work.

First Name     Last Name        Email                              Total
Total possible points                                              10
Russell        Richie           drussellmrichie@gmail.com          9.5
Student        McStudentFace    student.mcstudentface@uconn.edu    10
Current        Meme             current.meme@uconn.edu             9.75

Note that the name of this file will go in the subject line of the email,
so be sure it is appropriate for students to see this file name.

Total possible points must be in the first row.

"""
# Authors:
#
# Russell Richie
# github.com/drussellmrichie
# drussellmrichie@gmail.com
#
# Henry S. Harrison
# github.com/hsharrison
# henry.schafer.harrison@gmail.com

# This is largely cribbed from Automate the Boring Stuff with Python:
# https://automatetheboringstuff.com/chapter16/


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
from io import StringIO
import os.path
import re
import smtplib
from textwrap import dedent

from docopt import docopt
import pandas as pd
from toolz import curry

subject = '{course}: HW{hwid} feedback'
body = dedent("""
    Dear {First Name} {Last Name},

    This is an automatically generated email providing your grade and feedback on HW{hwid} in {course}.
    You received {Total} points (out of {total_possible}).
    See the attachment for details.

    Let me know if you have any questions.

    Best,
    {grader_name}

""").lstrip()


def send_all_emails(from_address, grades_path, password=None, dry_run=False, from_name=None):
    if password is None:
        password = getpass()
    
    grades_dir = os.path.dirname(grades_path)
    grades_filename = os.path.basename(grades_path)

    without_ext, ext = os.path.splitext(grades_filename)
    if ext.lower() == '.csv':
        hw_df = pd.read_csv(grades_path)
    elif ext.lower() in {'.xlsx', '.xls'}:
        hw_df = pd.read_excel(grades_path)
    else:
        raise NotImplementedError('Extension {} not supported'.format(ext))

    if dry_run:
        hw_df['Email'] = from_address
    
    global_info = dict(
        hwid=re.search(r'HW[0-9]+',grades_filename).group(0)[2:],
        course=grades_filename.split(' - ')[0],
        total_possible=hw_df.loc[0, 'Total'],
        grader_name=from_name or from_address,
        from_address=from_address,
    )
    
    print('Connecting and logging in to SMTP server...', end='')
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    smtp_obj.login(from_address, password)
    print('done.')

    try:
        hw_df.loc[1:, :].apply(send_email(smtp_obj, hw_df, **global_info), axis=1)
    finally:
        smtp_obj.quit()

    print('Sent all emails.')


@curry
def send_email(smtp_obj, df, row, **info):
    msg = MIMEMultipart()
    msg['Subject'] = subject.format(**info)
    msg['From'] = '{grader_name} <{from_address}>'.format(**info)
    msg.attach(MIMEText(body.format(**info, **row), 'plain'))

    attachment_file = StringIO()
    df.loc[[row.name, 0], :].to_csv(attachment_file, index=False)
    attachment_file.seek(0)
    attachment = MIMEText(attachment_file.read(), _subtype='csv')
    attachment.add_header('Content-Disposition', 'attachment', filename='{Last Name} HW{hwid}'.format(**info, **row))
    msg.attach(attachment)

    print('Emailing {First Name} {Last Name} <{Email}>...'.format(**row), end='')
    smtp_obj.sendmail(info['from_address'], row['Email'], msg.as_string())
    print('done.')


def main(argv=None):
    args = docopt(__doc__, argv=argv)

    send_all_emails(args['<sender-email>'], args['<grades-path>'], dry_run=args['--dry-run'], password=args['--password'], from_name=args['--name'])


if __name__ == '__main__':
    main()
