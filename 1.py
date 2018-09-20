import RPi.GPIO as GPIO
import time
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
import matplotlib.pyplot as plt
import matplotlib.image as mpm
import requests
from uuid import getnode as get_mac

'''
#API endpoint
API_ENDPOINT=""

API_KEY=


#ask for the format of data, i.e the parameters in the database table
def post_request(data):
    r=requests.post(url=API_ENDPOINT,data=data)
'''


#to play the sound
def play():
    playsound('alert.mp3')
    

#to get the mac address of the raspberry pi3 
def GetID():
    id=get_mac()
    return id

#to send the mail 
def send_mail(attachment):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Alert"
    msg['From'] = me
    msg['To'] = you
    fp = open(attachment, 'rb')
    #if received error here, based on MIME image
    #make sure camera is connected properly 
    img = MIMEImage(fp.read())
    fp.close()

    msg.attach(img)

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    print("Email sent!")
    s.quit()


#capturing the image from the camera 
def image_capture():
        cap=cv2.VideoCapture(0)
        ret,frame=cap.read()
        #time.sleep(2000)
        print(ret,frame)
        cv2.imwrite('preview.jpg',frame)
        time.sleep(10)
        attachment='preview.jpg'
        a=mpm.imread('preview.jpg')
        plt.imshow(a)
        plt.ion()
        plt.show()
        time.sleep(5)
        plt.close()
        print('playing now!')

        t1=Thread(target=play)
        t1.start()
        
        
        t2=Thread(target=send_mail,args=(attachment,))
        t2.start()
        #start_new_thread(send_mail,(attachment,))
        print('Started thread 2')
        t1.join(1)
        
        t2.join(1)
    
        send_mail(attachment)
        
        image1=bytearray(a)
        
        '''
        #check the parameters to be put here 
        data={
            'api_dev_key':API_KEY,
            'image1':image1
            'deviceId':DeviceId
            'image2':
            
            }
        
        '''
        
        cap.release()
        cv2.destroyAllWindows()
        time.sleep(100)

DeviceId=GetID()
me = "yathisolutionstsiic@gmail.com"
my_password = r"yathi12345"

#change to whomever you wanted to send over heress
you = "anvoruganti@gmail.com"

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN) #PIR
GPIO.setup(24, GPIO.OUT) #BUzzer

while True:
        a=int(GPIO.input(2))
        print(a)
        if a==0:
            GPIO.output(24, True)
            time.sleep(0.5) #Buzzer turns on for 0.5 sec
            GPIO.output(24, False)
            print("Motion Detected...")
            time.sleep(5) #to avoid multiple detection
            time.sleep(1)
            '''
            cap=cv2.VideoCapture(0)
            ret,frame=cap.read()
            #time.sleep(2000)
            print(ret,frame)
            cv2.imwrite('preview.jpg',frame)
            attachment='preview.jpg'
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
            '''
            image_capture()
            
        else:
            print("Normal")
            time.sleep(0.5) #Buzzer turns on for 0.5 sec
           

