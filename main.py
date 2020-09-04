from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import requests
import time
import urllib.request
from gtts import gTTS
import os
import sys
import numpy as np
from datetime import datetime, timedelta
import random
import json
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

COMPLIMENT_URL= 'https://complimentr.com/api'

MODES = ["COMPLIMENT", "ROAST", "GAMBLE"]

DEFAULT_TIME = datetime(2020,4,20)
DELAYED_TIME = timedelta(seconds=6)

lastTimeCalled = DEFAULT_TIME
facesDetected = False

session = Session(profile_name="Administrator")
polly = session.client("polly")

SERVER_URL = "http://127.0.0.1:3000/message"

os.environ['DISPLAY'] = ':0'

def main():
    with open('compliments.json',) as file:
        compliments_json = json.load(file)
        for compliment in compliments_json['compliments']:
            print(compliment)
    with open('insults.json', 'r') as file:
        insults_json = json.load(file)
        for insult in insults_json['insults']:
            print(insult)
    faceDetection(lastTimeCalled, facesDetected, compliments_json['compliments'], insults_json['insults'], MODES[0] )

def getCompliment(complimentsArray):
    #complimentRequest = requests.get(url=COMPLIMENT_URL)
    #complimentText = complimentRequest.json()
    randomIndex = random.randint(0, (len(complimentsArray) - 1))
    print(randomIndex)
    complimentJson = {"Message": "{}".format(complimentsArray[randomIndex])}

    requests.post(SERVER_URL, json=complimentJson)
    print("requests went successfully")
    sayWords(complimentsArray[randomIndex])
    print("say words went successfully")

def getInsult(insultsArray):
    randomIndex = random.randint(0, (len(insultsArray) - 1))
    insultJson = {"Message": "{}".format(insultsArray[randomIndex])}
    requests.post(SERVER_URL, json=insultJson)
    sayWords(insultsArray[randomIndex])

def faceDetection(lastTimeCalled, facesDetected, complimentsArray, insultsArray, mode):
    #print(complimentsArray, insultsArray)
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
            faces = face_cascade.detectMultiScale(gray,1.3,4)


            # Draw rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            if len(faces) > 0:
                # if a face is detected and it wasn't called in the past 6 seconds, get a compliment
                if facesDetected == False and datetime.now() - lastTimeCalled > DELAYED_TIME:
                    lastTimeCalled = datetime.now()
                    facesDetected = True
                    print("Face Detected! Generating Compliment")
                    if mode == "COMPLIMENT":
                        requests.post(SERVER_URL, json={"Message":"Hey I just wanted to say that you are an amazing and talented person"})
                        time.sleep(1)
                        sayWords("Hey I just wanted to say that you are an amazing and talented person")
                        #time.sleep(2)
                        requests.post(SERVER_URL, json={"Message": "Sike I am just kidding. Please get your fat, man boob, big forehead dumb ass out of my sight."})
                        time.sleep(1)
                        sayWords("Sike I am just kidding. Please you deserve the best in the world")
                        #sayWords("Sike, I am just kidding. Please get your fat, man boob, big forehead dumb ass out of my sight")
                    """
                    if mode == "COMPLIMENT":
                        print("trying to run compliment")
                        getCompliment(complimentsArray)
                        print("compliments ran successfully")
                    elif mode == "ROAST":
                        getInsult(insultsArray)
                    elif mode == "GAMBLE":
                        chance = random.randint(0,100)
                        print(chance)
                        if chance > 50:
                                getCompliment(complimentsArray)
                        else:
                                getInsult(insultsArray)
                    """
            else:
                facesDetected = False
            # Display the output
            cv2.imshow('img', img)
            rawCapture.truncate(0)
            k = cv2.waitKey(30) & 0xff
            if k==27:
                break
        except Exception as e:
            print("Error:", e)
            print("You don't have a video stream available. Try again dumbass")
            return

def sayWords(complimentText):
    try:
        response = polly.synthesize_speech(Text=complimentText, OutputFormat="mp3", VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        print(error)

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(os.getcwd(), "speech.mp3")
            try:
                with open(output,"wb") as file:
                    file.write(stream.read())
                    os.system("mpg321 -q speech.mp3")
            except IOError as error:
                print(error)
    else:
        print("could not stream audio bruh")
    #ttsObj = gTTS(text=complimentText, lang='en', slow=False)
    #ttsObj.save("compliment.mp3")
    #os.system("mpg321 -q compliment.mp3")
    #print("sent your message bro")
if __name__ == "__main__":
    main()
