#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created Date: June 11. 2020
Copyright: UNMANNED SOLUTION
Author: Dae Jong Jin 
Description: Can 통신 Read 예제
'''

class CanReader():

    def __init__(self, bus):
        self.__bus = bus
        self.__msg = None

    def receive_all(self):
        self.__msg = self.__bus.recv(1)
        if self.__msg is not None:
            # print(self.__msg)
            return self.__msg

    def run(self):
        '''
        ['Timestamp:', '2726190.858044', 'ID:', '02b0', 'S', 'DLC:', '5', '69', '00', '00', '07', '6e']
        * Data Constructure
          little endian : data[8] + data[7]
        '''
        self.receive_all()
        result = ''
        msg = str(self.__msg).split()
        if msg is not None:
            # print(msg)
            result = msg[8] + msg[7]
            result = int(result, 16)
            # print(result)
            return result
