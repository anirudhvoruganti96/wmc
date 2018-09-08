import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
from playsound import playsound
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage
#from _thread import start_new_thread



#wait for atleast five frames after raising an alert
#keep track about the moving objects- elimate the moving objects from the list

#if detected cat,dog, pig etc -- don't send the mail
#send the mail only if a person is also detected in the frame

#while sending the mail add the location from where the picture is being sent
#for the above communicate with the DB to get the location


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
my_password = r"******"
you = "anvoruganti@gmail.com"



options ={
        'model':'cfg/tiny-yolo-voc.cfg',
        'load':'tiny-yolo-voc.weights',


        #'model':'cfg/yolo.cfg',
        #'load':'yolov2.weights',

        'threshold':0.2,
}

tfnet=TFNet(options)
colors=[tuple(255*np.random.rand(3)) for _ in range(10)]

cap=cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,540)

tim=0

while True:
    stime=time.time()
    ret,frame=cap.read()
    ctr=0
    #print(frame)
    results=tfnet.return_predict(frame)
    #print(results)
    if ret:
        for color,result in zip(colors,results):
            tl=(result['topleft']['x'],result['topleft']['y'])
            br=(result['bottomright']['x'],result['bottomright']['y'])
            label=result['label']

            if(label!='person' or label!='cat' or label!='dog' or label!='car' or label!='truck'):
                ctr+=1

            confidence=result['confidence']
            text= '{}:{:.0f}%'.format(label,confidence*100)
            frame=cv2.rectangle(frame,tl,br,color,5)
            frame=cv2.putText(frame,text,tl,cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
        cv2.imshow('frame',frame)
        print('FPS {:.1f}'.format(1/(time.time()-stime)))
    if ctr>0:
        #playsound('aler.mp3')---shouldn't mail when there is a dog seen qq

        #'''
        print(tim)
        if(tim%50==0):

            #print('playing now!')
            #t1=Thread(target=play)
            #t1.start()

            cv2.imwrite('preview.png',frame)

            attachment='preview.png'
            mail_ctr=0
            for result in results:
                label=result['label']
                if(label=='person' and mail_ctr==0):
                    #attachment='preview.png'
                    print('playing now!')
                    t1=Thread(target=play)
                    t1.start()

                    t2=Thread(target=send_mail,args=(attachment,))
                    t2.start()
                    #start_new_thread(send_mail,(attachment,))
                    print('Started thread 2')
                    t1.join(1)
                    t2.join(1)
                    print(t2.isAlive())
                    mail_ctr=1
            tim=1

        else:
            tim+=1
        #'''

    if cv2.waitKey(1) &0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
