#!/usr/bin/env python3
from TelloSDKPy.djitellopy.tello import Tello
import cv2
import pygame
import numpy as np
import time
# Speed of the drone
S = 25
# Frames per second of the pygame window display
FPS = 30


class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations
            - W and S: Up and down.
    """

    def __init__(self):
        # Init pygame
        pygame.init()
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])
        self.screen.fill([0, 0, 0])
        pygame.display.update()
        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10
        self.prnt = False
        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)

    def run(self):

        if not self.tello.connect():
            print("Tello not connected")
            return

        if not self.tello.set_speed(self.speed):
            print("Not set speed to lowest possible")
            return

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        if not self.tello.streamon():
            print("Could not start video stream")
            return

        frame_read = self.tello.get_frame_read()
        frame = frame_read.frame
        should_stop = False
        currentFrame = 0
        width = len(frame[0])
        height = len(frame)
        print(width, height)
        a = 80
        minFaceF, maxFaceF = 130, 220
        frameCenter = [int(width/2), int(height/2)]
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                frame_read.stop()
                break
            #FaceDetection
            frame = frame_read.frame
            frame = cv2.flip(frame,1)
            frame = cv2.rectangle(frame,(frameCenter[0]-a,frameCenter[1]-a),(frameCenter[0]+a,frameCenter[1]+a),(0,0,255),2)
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
            face_detect = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
            if(face_detect != ()):
                #Center of Face
                faceCenter = [int(face_detect[0][0]+(face_detect[0][2]/2)),int(face_detect[0][1]+(face_detect[0][3]/2))]
                frame = cv2.rectangle(frame,(faceCenter[0],faceCenter[1]),(faceCenter[0],faceCenter[1]),(0,255,0),2)
                if((faceCenter[0] > frameCenter[0]-a) &(faceCenter[0] <= frameCenter[0]+a)):    #TO-DO: TOLERANZBOX ALS INTERVALL ANcGEBEN, statt einzelner Punkt.
                    self.yaw_velocity = 0
                elif(faceCenter[0] < frameCenter[0]-a):
                    #print("Move right")
                    if(self.prnt == True):
                        print("Move right")
                    self.yaw_velocity = S
                elif(faceCenter[0] > frameCenter[0]+a):
                    if(self.prnt == True):
                        print("Move Left")
                    self.yaw_velocity = -S
                if((faceCenter[1] > frameCenter[1]-a) &(faceCenter[1] < frameCenter[1]+a)):
                    self.up_down_velocity = 0
                elif(faceCenter[1] > frameCenter[1]+a):
                    if(self.prnt == True):
                        print("Move Down")
                    self.up_down_velocity = -S
                elif(faceCenter[1] < frameCenter[1]-a):
                    if(self.prnt == True):
                        print("Move Up")
                    self.up_down_velocity = S
                if((face_detect[0][2] > minFaceF)&(face_detect[0][2] <= maxFaceF)):
                    self.for_back_velocity = 0
                elif(face_detect[0][2] <= minFaceF):
                    print("zu fern")
                    self.for_back_velocity = S
                elif(face_detect[0][2] > maxFaceF):
                    print("zu nah")
                    self.for_back_velocity = -S
            elif():
                self.yaw_velocity = 0
                self.up_down_velocity = 0
                self.for_back_velocity = 0
            for (x,y,w,h) in face_detect:
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # To stop duplicate images
            currentFrame += 1
            time.sleep(1 / FPS)
        cv2.destroyAllWindows()
        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S
        elif key == pygame.K_f:
            self.prnt = True

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            self.tello.land()
            self.send_rc_control = False
        elif key == pygame.K_f:
            self.prnt = False

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
