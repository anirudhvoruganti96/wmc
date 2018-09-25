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
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt 
import matplotlib.image as mpm
import requests
from uuid import getnode as get_mac
import pygame
import pygame.camera
from pygame.locals import *
import os,random
from PIL import Image
import io
import requests
import json
import base64


#to play the sound
def play():
    andomfile = random.choice(os.listdir("/home/pi/Desktop/wmc"))
    file = ' /home/pi/Desktop/wmc/voice.ogg'
    os.system ("omxplayer -o local voice.ogg")
    '''
    ImageItself = Image.open('preview.jpg')
    ImageNumpyFormat = np.asarray(ImageItself)
    plt.imshow(ImageNumpyFormat)
    plt.draw()
    plt.pause(5) # pause how many seconds
    plt.close()
    '''

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
        #time.sleep(10)
        attachment='preview.jpg'
        print('playing now!')

        t1=Thread(target=play)
        t1.start()
        
        '''
        t2=Thread(target=send_mail,args=(attachment,))
        t2.start()
        #start_new_thread(send_mail,(attachment,))
        print('Started thread 2')
        '''
        t1.join(1)
        
        #t2.join(1)
        img = Image.open('preview.jpg', mode='r')
        #roiImg = img.crop(box)

        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()

        encoded=base64.b64encode(imgByteArr)

        #print(encoded)


        #to decode
        #arr=base64.b64decode(encoded)
        #print(arr)

        headers = {
            'Content-Type': 'application/json'
        }



        payload={
            "deviceId":"1",
            "image1":list(encoded),
            "image2":list(encoded),
            "status":"0"

        }

        response=requests.post(url=API_ENDPOINT,data=json.dumps(payload),headers=headers)
        print(response.text)

        
        
        cap.release()
        cv2.destroyAllWindows()
        #time.sleep(100)

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
            time.sleep(3) #to avoid multiple detection
            #time.sleep(1)
            image_capture()
            time.sleep(5)
            
        else:
            print("Normal")
            time.sleep(0.5) #Buzzer turns on for 0.5 sec
           

