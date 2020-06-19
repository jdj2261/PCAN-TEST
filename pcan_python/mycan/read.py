#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created Date: June 11. 2020
Copyright: UNMANNED SOLUTION
Author: Dae Jong Jin 
Description: Can 통신 Read 예제
'''

"""
['Timestamp:', '2726190.858044', 'ID:', '02b0', 'S', 'DLC:', '5', '69', '00', '00', '07', '6e']
Data Constructure : little endian : data[8] + data[7]
"""

class CanReader():

    def __init__(self, bus):
        self.__bus = bus
        """
        CanReader API calss implementation
        Parameter bus : can.interface.Bus(bustype='pcan',
                                channel='PCAN_USBBUS1',
                                bitrate=500000)
        """
    def run(self):

        self.receive_all()
        result = ''
        msg = str(self.__msg).split()
        '''
        ['Timestamp:', '3407476.104066', 'ID:', '02b0', 'S', 'DLC:', '5', '4a', '11', '00', '07', '6f']
        '''
        # print(msg)
        search = 'DLC:'
        if msg is not None:
            if search in msg:
                i = msg.index(search)
                result = msg[i+3] + msg[i+2]
                result = int(result, 16)
                # print("DEC : {0}\t HEX : {0:04x}\t BIN : {0:016b}".format(result))
                return result
        """ 
        Filter received the raw data
        Parameter: msg 
        Return: result(filtering SAS(Steering Angle Sensor)'s data)
        """

    def receive_all(self):
        self.__msg = self.__bus.recv(1)
        if self.__msg is not None:
            return self.__msg
        """ 
        Recieve CAN raw data
        Parameter: msg 
        Return: msg 
        """


