#!/usr/bin/env python3
from TelloSDKPy.djitellopy.tello import Tello
import cv2
import pygame
import numpy as np
import time


def main():
    #Controller Init
    pygame.init()
    joysticks = []
    for i in range(0,pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print(joysticks[-1].get_name())
    #Tello Init
    
    while True:
        for event in pygame.event.get():
            if(event.type == pygame.JOYBUTTONDOWN):
                b = event.button
                if (b == 0):
                    print("takeoff")
                    drone.takeoff()
                elif (b == 1):
                    print("land")
                    drone.land()
                elif (b == 2):
                    print("quit")
                    return 0
if __name__== "__main__":
    main()


