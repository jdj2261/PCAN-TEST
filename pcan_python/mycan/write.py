# -*- coding: utf-8 -*-

'''
Created Date: June 10. 2020
Copyright: UNMANNED SOLUTION
Author: Dae Jong Jin 
Description: Can 통신 Write 예제
'''


class CanWriter():

    def __init__(self, bus):
        self.__bus = bus
        """
        CanWriter API calss implementation
        Parameter bus : can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
        """

    def run(self, msg):
        try:
            self.__bus.send(msg)
            # print(msg)
            # print("Message sent on {}".format(self.__bus.channel_info))
        except can.CanError:
            print("Message NOT sent")
        """ 
        Write CAN DATA
        Parameter msg : Can Data
        Return :None
        """
