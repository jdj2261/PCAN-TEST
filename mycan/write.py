#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created Date: June 10. 2020
Copyright: UNMANNED SOLUTION
Author: Dae Jong Jin 
Description: Can 통신 Write 예제
'''

'''
PACKET DEFINITION
CAN ID RTR IDE DLC D1 D2 D3 D4 D5 D6 D7 D8 Desc.
0x181 0 0 5 0x20 0x00 0x00 0x01 0xff X X X 0~7ch ON
0x181 0 0 5 0x20 0x00 0x00 0x01 0x00 X X X 0~7ch OFF
0x181 0 0 5 0x20 0x00 0x00 0x01 0x01 X X X 0ch ON
0x181 0 0 5 0x20 0x00 0x00 0x01 0x02 X X X 1ch ON
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# from can.interface
import can

class CanWriter():

    def __init__(self, bus):
        self.__bus = bus

    def write(self, msg):
        try:
            self.__bus.send(msg)
            print(msg)
            # print("Message sent on {}".format(self.__bus.channel_info))
        except can.CanError:
            print("Message NOT sent")
        
if __name__ == "__main__":
    bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
    send_data = 0x00
    msg = can.Message(arbitration_id=0x181, data= [0x20, 0x00, 0x00, 0x01, send_data], extended_id=False)
    cw = CanWriter(bus)
    cw.write(msg)