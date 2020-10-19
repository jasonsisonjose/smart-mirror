# pi camera libraries
from picamera.array import PiRGBArray
from picamera import PiCamera

# Face detection libraries
import cv2
import numpy as np

# General usage: importing files, outputting sound via speakers
import requests
import time
from gtts import gTTS
import os
import sys
from datetime import datetime, timedelta

import random
import json

# AWS libraries 
#from boto3 import Session
#from botocore.exceptions import BotoCoreError, ClientError
#from contextlib import closing

# if you don't want to generate your own compliments!
# COMPLIMENT_URL= 'https://complimentr.com/api'

MODES = ["COMPLIMENT", "ROAST", "GAMBLE"]

DEFAULT_TIME = datetime(2020,4,20)
DELAYED_TIME = timedelta(seconds=6)

lastTimeCalled = DEFAULT_TIME
facesDetected = False

# If using Amazon Polly (AWS), need to define this!
#session = Session(profile_name="Administrator")
#polly = session.client("polly")

# Web-server location
SERVER_URL = "http://127.0.0.1:3000/message"

# Required to run commands via ssh
os.environ['DISPLAY'] = ':0'

def main():
    # Load in the compliments.json file
    with open('compliments.json',) as file:
        compliments_json = json.load(file)
        #for compliment in compliments_json['compliments']:
            #print(compliment)

    # Load in the insults.json file
    with open('insults.json', 'r') as file:
        insults_json = json.load(file)
        #for insult in insults_json['insults']:
            #print(insult)
    print("Running on face detection service, don't fuck it up")
    faceDetection(lastTimeCalled, facesDetected, compliments_json['compliments'], insults_json['insults'], MODES[0] )

# Selects a random compliment
# @params: array
def getCompliment(complimentsArray):
    #==== Select a random compliment ====#
    randomIndex = random.randint(0, (len(complimentsArray) - 1))
    complimentJson = {"Message": "{}".format(complimentsArray[randomIndex])}

    #==== Send the random compliment to local web-server ===="
    requests.post(SERVER_URL, json=complimentJson)
    print("Successfully sent the message: {} to the web-server".format(complimentsArray[randomIndex]))
    #==== Output the compliment through text-to-speech processing ====#
    sayWords(complimentsArray[randomIndex])

# Selects a random insult
# @params: array
def getInsult(insultsArray):
    randomIndex = random.randint(0, (len(insultsArray) - 1))
    insultJson = {"Message": "{}".format(insultsArray[randomIndex])}
    requests.post(SERVER_URL, json=insultJson)
    sayWords(insultsArray[randomIndex])

# Main face detection service
# @params: datetime, boolean, array, array, str
def faceDetection(lastTimeCalled, facesDetected, complimentsArray, insultsArray, mode):
    #loads in pre-trained face detection model
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #==== For using a pi camera attachment as a video stream ===="
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 32
    rawCapture=PiRGBArray(camera,size=(640,480))

    time.sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        try:
            #=== For using a phone camera as a video stream via bluetooth ===#
            # img_arr = np.array(bytearray(urllib.request.urlopen(PHONE_URL).read()),dtype=np.uint8)
            # img = cv2.imdecode(img_arr,-1)
            # cv2.imshow('IPWebcam',img)

            img = frame.array

            # Turns the image into black and white, so we can work with it
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Determines whether a picture contains a face, may need to tune for better results
            # @params: gray, float, int
            # the float value represents 
            faces = face_cascade.detectMultiScale(gray,1.3,8)

            # Draw rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            if len(faces) > 0:
                # if a face is detected and it wasn't called in the past 6 seconds, get a compliment
                if facesDetected == False and datetime.now() - lastTimeCalled > DELAYED_TIME:
                    lastTimeCalled = datetime.now()
                    facesDetected = True
                    print("Face Detected!")
                    if mode == "COMPLIMENT":
                        print("Generating Compliment!")
                        getCompliment(complimentsArray)
                    elif mode == "ROAST":
                        print("Generating Insult!")
                        getInsult(insultsArray)
                    elif mode == "GAMBLE":
                        chance = random.randint(0,100)
                        print(chance)
                        if chance > 50:
                                getCompliment(complimentsArray)
                        else:
                                getInsult(insultsArray)
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

# uses the AWS text to speech to generate a mp3 and play the mp3 file
# @params: str
def sayWords(complimentText):
    # AWS Polly (text-to-spech)
    #try:
    #    response = polly.synthesize_speech(Text=complimentText, OutputFormat="mp3", VoiceId="Joanna")
    #except (BotoCoreError, ClientError) as error:
    #    print(error)

    #if "AudioStream" in response:
    #    with closing(response["AudioStream"]) as stream:
    #        output = os.path.join(os.getcwd(), "speech.mp3")
    #        try:
    #            with open(output,"wb") as file:
    #                file.write(stream.read())
    #                os.system("mpg321 -q speech.mp3")
    #        except IOError as error:
    #            print(error)
    #else:
    #    print("could not stream audio bruh")

    #===== USING FREE GOOGLE Text-to-speech ====#
    ttsObj = gTTS(text=complimentText, lang='en', slow=False)
    ttsObj.save("compliment.mp3")
    os.system("mpg321 -q compliment.mp3")
    print("I just said your message")
if __name__ == "__main__":
    main()

    #===Speaker Test===#
    #sayWords("you are stupid")
