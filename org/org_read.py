#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created Date: June 11. 2020
Copyright: UNMANNED SOLUTION
Author: Dae Jong Jin 
Description: original read 
'''

import can
from time import sleep
import os


try:
	bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
except OSError:
	print('Cannot find PiCAN board.')
	exit()
	
print('Ready')

try:
    while True:
        # Wait until a message is received.
        message = bus.recv()
        # print(message.dlc)

        c = '{0:f} {1:x} {2:x} '.format(message.timestamp, message.arbitration_id, message.dlc)
        s = ''
        for i in range(message.dlc ):
            s +=  '{0:x} '.format(message.data[i])

        print(' {}'.format(c+s))

        # data = '{0:x}'.format(message.data[0])
        # print(data)
        sleep(0.0095)
	
except KeyboardInterrupt:
	#Catch keyboard interrupt
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')

except AttributeError:
    pass