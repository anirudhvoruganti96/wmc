import cv2
import numpy as np
import time
from playsound import playsound
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage
import sys


def play():
    playsound('aler.mp3')


def send_mail(attachment):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Alert"
    msg['From'] = me
    msg['To'] = you
    fp = open(attachment, 'rb')
    img = MIMEImage(fp.read())
    fp.close()

    msg.attach(img)

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    # uncomment if interested in the actual smtp conversation
    #s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already
    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()


me = "yathisolutionstsiic@gmail.com"
my_password = r"yathi12345"

#change to whomever you wanted to send over heress
you = "khadar.data@gmail.com"


while True:
    choice = int(input("Please select an option \n 1) Capture Image and send Mail \n 2)Exit \n"))

    if (choice==1):
        cap=cv2.VideoCapture(0)
        ret,frame=cap.read()
        #time.sleep(2000)
        print(ret,frame)
        cv2.imwrite('preview.png',frame)
        attachment='preview.png'
        print('playing now!')
        t1=Thread(target=play)
        t1.start()

        t2=Thread(target=send_mail,args=(attachment,))
        t2.start()
        #start_new_thread(send_mail,(attachment,))
        print('Started thread 2')
        t1.join(1)
        t2.join(1)

        cap.release()
        cv2.destroyAllWindows()

    if (choice==2):
        break
