from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import requests
import time
import urllib.request
from gtts import gTTS
import os
import numpy as np
from datetime import datetime, timedelta
import time

COMPLIMENT_URL= 'https://complimentr.com/api'
COMPLIMENT_MODE = True;

DEFAULT_TIME = datetime(2020,4,20)
DELAYED_TIME = timedelta(seconds=4)

lastTimeCalled = DEFAULT_TIME
facesDetected = False;


PHONE_URL = "http://192.168.1.207:8080/shot.jpg"
def main():
    faceDetection(lastTimeCalled, facesDetected)

        

def getCompliment():
    complimentRequest = requests.get(url=COMPLIMENT_URL)
    complimentText = complimentRequest.json()
    sayWords(complimentText['compliment'])

def faceDetection(lastTimeCalled, facesDetected):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 32    
    rawCapture=PiRGBArray(camera,size=(640,480))
    time.sleep(0.1)
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        try:
            #===For using a phone camera via bluetooth===#
            # img_arr = np.array(bytearray(urllib.request.urlopen(PHONE_URL).read()),dtype=np.uint8)
            # img = cv2.imdecode(img_arr,-1)
            # cv2.imshow('IPWebcam',img)

            img = frame.array

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,7)
            print(datetime.now() - lastTimeCalled > DELAYED_TIME)
            # and datetime.now() - lastTimeCalled > DELAYED_TIME
            if len(faces) > 0:
                # if a face is detected and it wasn't called in the past 6 seconds, get a compliment
                print("Faces Detected: ",facesDetected)
                if facesDetected == False and datetime.now() - lastTimeCalled > DELAYED_TIME:
                    lastTimeCalled = datetime.now()
                    facesDetected = True
                    getCompliment()
            else:
                facesDetected = False
            # Draw rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Display the output
            cv2.imshow('img', img)
            rawCapture.truncate(0)
            k = cv2.waitKey(30) & 0xff
            if k==27:
                break
        except:
            print("You don't have a video stream available. Try again dumbass")
            return

def sayWords(complimentText):
    ttsObj = gTTS(text=complimentText, lang='en', slow=False)
    ttsObj.save("compliment.mp3")
    os.system("start compliment.mp3")
    
if __name__ == "__main__":
    main()

