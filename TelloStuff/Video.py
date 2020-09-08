#!/usr/bin/env python3


import cv2
import numpy as np

# Playing video from file:
# cap = cv2.VideoCapture('vtest.avi')
# Capturing video from webcam:
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
width = len(frame[0])
height = len(frame)
print(width, height)
frameCenter = [int(width/2), int(height/2)]
#currentFrame = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Handles the mirroring of the current frame
    frame = cv2.flip(frame,1)
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    a = 30  #Abweichung von CenterFrame
    minFaceF, maxFaceF = 200, 350   # Erlaubte Min und Max der Gesichtsframe-Größe
    #Center of Frame
    frame = cv2.rectangle(frame,(frameCenter[0]-a,frameCenter[1]-a),(frameCenter[0]+a,frameCenter[1]+a),(0,0,255),2)
    # Saves image of the current frame in jpg file
    # name = 'frame' + str(currentFrame) + '.jpg'
    # cv2.imwrite(name, frame)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    face_detect = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    if(face_detect != ()):
        #Center of Face
        faceCenter = [int(face_detect[0][0]+(face_detect[0][2]/2)),int(face_detect[0][1]+(face_detect[0][3]/2))]
        frame = cv2.rectangle(frame,(faceCenter[0],faceCenter[1]),(faceCenter[0],faceCenter[1]),(0,255,0),2)
        if((faceCenter[0] > frameCenter[0]-a) &(faceCenter[0] <= frameCenter[0]+a)):    #TO-DO: TOLERANZBOX ALS INTERVALL ANGEBEN, statt einzelner Punkt.
            pass
        elif(faceCenter[0] < frameCenter[0]-a):
            print("Move right")
        elif(faceCenter[0] > frameCenter[0]+a):
            print("Move Left")
        if((faceCenter[1] > frameCenter[1]-a) &(faceCenter[1] < frameCenter[1]+a)):
            pass
        elif(faceCenter[1] > frameCenter[1]+a):
            print("Move Up")
        elif(faceCenter[1] < frameCenter[1]-a):
            print("Move down")
        if((face_detect[0][2] > minFaceF)&(face_detect[0][2] <= maxFaceF)):
            pass
        elif(face_detect[0][2] <= minFaceF):
            print("Move Forward")
        elif(face_detect[0][2] > maxFaceF):
            print("Move Backwards")
    for (x,y,w,h) in face_detect:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        #print((x,y,w,h))

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # To stop duplicate images
    #currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# Potential Error:
# OpenCV: Cannot Use FaceTime HD Kamera
# OpenCV: camera failed to properly initialize!
# Segmentation fault: 11
#
# Solution:
# I solved this by restarting my computer.
# http://stackoverflow.com/questions/40719136/opencv-cannot-use-facetime/42678644#42678644
