#!/usr/bin/env python3
import socket
import time
import pygame
myIP = "192.168.10.2"
port = 9000
me = (myIP,port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ("192.168.10.1", 8889)
s.bind(me)
command_timeout = .3

pygame.init()
joysticks = []
for i in range(0,pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    print(joysticks[-1].get_name())
s.sendto("command".encode(encoding="utf-8"), tello_address)
while True:
	for event in pygame.event.get():
		if(event.type == pygame.JOYBUTTONDOWN):
			b = event.button
			if (event.joy == 0):
				if (b == 0):
					print("takeoff")
					s.sendto("takeoff".encode(encoding="utf-8"), tello_address)
				elif (b == 1):
					print("land")
					s.sendto("land".encode(encoding="utf-8"), tello_address)
				elif (b == 2):
					print("quit")
					break
#drone.send_command("emergency")
#time.sleep(5)
"""
def send_command( command):
        """"""Sends a command to the Tello and waits for a response.
        If self.command_timeout is exceeded before a response is received,
        a RuntimeError exception is raised.
        Args:
            command (str): Command to send.
        Returns:
            str: Response from Tello.
        Raises:
            RuntimeError: If no response is received within self.timeout seconds.
        """"""

        self.abort_flag = False
        timer = threading.Timer(command_timeout, set_abort_flag)

        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        timer.start()
        while self.response is None:
            if self.abort_flag is True:
                raise RuntimeError('No response to command')
        timer.cancel()
        response = self.response.decode('utf-8')
        self.response = None
        return response
"""
