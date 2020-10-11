# dumb-mirror

For this project, I am specifically using a raspberry pi 4, raspberry camera module.

Hello, this project is designed to display compliments/insults on smart mirror via face detection. This github represents the software side and not the entire build. there are 3 components to this project:

##Table of Contents:

1. Hardware Prerequisites 
2. Setting things up
  a. Face Detection with Python
  b. Creating the local web-server
  c. MagicMirror Configuration
  d. Adding Compliments and Insults
  e. Optional additions
    i. AWS Text-to-speech
    ii. Compliment Generator API
3. How it works
4. Running the code




2. Setting things up
a. Face Detection with Python
  Hardware Prereqs: a computer, some sort of camera (pi camera, ip webcam, webcam, dslr)
  Software Preqes: cv2, numpy, requests, picamera (for raspberry pi camera)
  
  To get all of the software prereqs, you should first create a virtualenv for python. If you do not know what a virtual environment is, it is essentially creating a workspace for python packages as it can get pretty messy. The instructions for setting up a virtual environment can be found here <insert link here>
  
  Now that you have a virtualenv, you should be able to download the required software via ```pip install```. 
  
  Now that we have all of the software requiments we need to connect a camera and make sure that we can access the video stream. If using pi camera, you can access the video stream via:
  ``` camera = PiCamera ```
  If you are using another camera video source, you will likely use:
  ``` camera = cv2.VideoCapture(0)```
  
  We now need to adjust the pi camera stream into something that we can work with in python:
  ```
  camera.resolution = (640, 480)
  camera.framerate = 32
  rawCapture = PiRGBArray(camera, size=(640,480)
  ```
  Controlling cameras via python can vary depending on the type of camera that you are using and can take some research and fiddling around to get it just right!
  
b. Node Web-server configuration
  Hardware Prereqs: a computer
  Prereqs: node
  If you do not have node installed, you can install it via <insert instruction here> or you can follow the offical download options on <insert node download link here>
  
  This part of the project is responsible as way of communication between my Magic Mirror and my Raspberry pi. In hindisght, it was probably better to try an implement a web-socket. For this part, we need to create an endpoint where you can push new messages in (POST) and then also get new messages(GET).
  
  As long as you have node configured, you can run the web-server!
c. Magic Mirror Module configuration
  Hardware prereqs: a computer
  Prereqs: Magic Mirror
  
  I would highly recommend downloading the MagicMirror code first to make sure that it works before modifying anything! The MagicMirror code can be found here <insert MagicMirror link>

  We need to define a custom module to display text when we want it to, in this case, we want to display a new message on the smart mirror when a face is detected. In my own project, I just modified the original compliments module to my own liking. I will be providing the code separately because the proper way is to create a custom module. 
  
  Each module has a node_helper file which is a javascript file that is responsible for making requests or doing any computations for the original module. In this case, we will be using a node_helper file to make requests to our web-server to retrieve any new messages sent by the face detection program.
  <insert code here>
  
  d. Adding compliments and insults
    You can simply modify the list of compliments by using the compliments.json and adding new strings to the array
    
    You can do the same thing with the insults by modifying the insults.json file
    
  e. Optional Additions
    i. AWS Text-to-speech (Amazon Polly) + alternatives
      This requires you to have an Amazon Developer account. The instructions for signing up for an AWS developer account is well documented here <insert link here>. To set up Amazon Polly, you need to install the AWS CLI (command line interface), and the instructions can also be found here. I am currently using the free trial of AWS for 12 months.
  
      If you don't want to use AWS because you don't to use a trial, fair enough. In the beginning, I used Google's FREE text to speech python library (gTTS). It works just fine, all you need to do to install is simply 
      ``` pip install gTTS``` 
    ii. Compliment Generator API
      If you don't feel like creating your own compliments, there is actually a free compliment generator API, I've provided the url in the main python code itself. All you need to do to get a compliment via this method is to make a HTTP GET request to that url like this:
 <insert screenshot of complimentr API>
3. How it works!

4. Running the code

There is probably a way to manage terminal commands, but for now, I am simply using three separate terminals. One for face detection, one for the web-server, and lastly one for running the Magic Mirror.

For the face detection program, make sure that you are in your virtual env (you should have the name of your virtual environment at the beginning of your command line just like this!)

For the web-sever, make sure that you are in the right directory and you can start the web-server via:
``` 
node web-server.js
```

You can test that the web-server is working by making some POST and GET requests via cURL.

POST request test:
<insert screenshot here>
  
GET request test:
For the Magic Mirror, as long as you are in the directory of MagicMirror, you can simply run:
```
npm start
``` 
If you are running this via ssh, you can do <insert rest of instructions here>
