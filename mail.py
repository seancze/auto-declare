import json
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import sha256

import pytz


# Ensure that time is in Canada timezone
def utc_to_time(naive, timezone="Canada/Eastern"):
  return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))

def send_email(isSuccessful = True):
  #The mail addresses and password
  sender_email = "autodeclare@gmail.com"
  sender_pass = "tcngjjliydwtfjrd"
  recipient_email = os.environ.get("EMAIL")
  #Setup the MIME
  message = MIMEMultipart()
  message['From'] = sender_email
  message['To'] = recipient_email


  now = utc_to_time(datetime.utcnow())
  if isSuccessful:
    message['Subject'] = "Health Declaration Posted"
    mail_content = f'''Your temperature was successfully updated on {now.strftime("%B %d, %Y")} at {now.strftime("%H:%M:%S")}. Stay safe from COVID-19! :)
Note: Do record your temperature manually and stop the script IF YOU'RE NOT FEELING WELL
    '''
  else:
    message['Subject'] = "Health Declaration FAILED"
    mail_content = f'''Your temperature failed to update on {now.strftime("%B %d, %Y")} at {now.strftime("%H:%M:%S")}.
Please record your temperature manually and report the bug to the github contributors if you know them. Thanks!'''
  
  message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
  message.attach(MIMEText(mail_content, 'plain'))

  #Create SMTP session for sending the mail
  session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
  session.starttls() #enable security
  session.login(sender_email, sender_pass) #login with mail_id and password
  text = message.as_string()
  session.sendmail(sender_email, recipient_email, text)
  session.quit()
  print('Mail Sent')
  

if __name__ == "__main__":
  send_email()
