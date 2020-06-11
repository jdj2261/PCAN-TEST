#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created Date: June 11. 2020
Copyright: UNMANNED SOLUTION
Author: Dae Jong Jin 
Description: Can 통신 Read 예제
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# from can.interface
import can
from can.bus import BusState
from time import sleep


class CanReader():

    def __init__(self, bus):
        self.__bus = bus
        self.__msg = None

    def receive_all(self):
        self.__msg = self.__bus.recv(1)
        if self.__msg is not None:
            return self.__msg
            # print(self.__msg)

    def convert_int(self):
        '''
        ['Timestamp:', '2726190.858044', 'ID:', '02b0', 'S', 'DLC:', '5', '69', '00', '00', '07', '6e']
        * Data Constructure
          little endian : data[8] + data[7]
        '''
        result = ''
        msg = str(self.__msg).split()
        if msg is not None:
            # print(msg)
            result = msg[8] + msg[7]
            result = int(result, 16)

            return result
            # print(result)

if __name__ == "__main__":
    bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
    cr = CanReader(bus)

    while True :
        cr.receive_all()
        test = cr.convert_int()
        print(test)