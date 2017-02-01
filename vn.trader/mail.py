# encoding: UTF-8
import smtplib
import json
import sys
from datetime import *

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def send_email(user='', pwd='', recipient='', subject='mail test', body=''):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    #message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    #""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['FROM'] = FROM
    bodyStr = ''

    #This solved the problem with the encode on the subject.
    msg['Subject'] = Header(
        subject.encode('utf-8'),
        'UTF-8'
    ).encode()
    msg['To'] = recipient
    # And this on the body
    _attach = MIMEText(bodyStr.encode('utf-8'), 'html', 'UTF-8')        
    msg.attach(_attach) 
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        # print('successfully sent the mail')
    except Exception as e:
        print e

if __name__ == '__main__':
    send_email(subject=u'Get EventLog__:2016-11-09 14:50:49:今日总成交合约数量10，超过限制10')
