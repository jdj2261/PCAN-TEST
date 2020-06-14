#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created Date: June 10. 2020
Copyright: UNMANNED SOLUTION
Author: Dae Jong Jin 
Description: Can 통신 Process
'''

'''
PACKET DEFINITION
CAN ID RTR IDE DLC D1 D2 D3 D4 D5 D6 D7 D8 Desc.
0x181 0 0 5 0x20 0x00 0x00 0x01 0xff X X X 0~7ch ON
0x181 0 0 5 0x20 0x00 0x00 0x01 0x00 X X X 0~7ch OFF
0x181 0 0 5 0x20 0x00 0x00 0x01 0x01 X X X 0ch ON
0x181 0 0 5 0x20 0x00 0x00 0x01 0x02 X X X 1ch ON
'''

'''
1 바퀴 : 3606
360도 : 3606
1도 : 10.017
'''

import can
import time
from mycan.read import CanReader
from mycan.write import CanWriter
from threading import Thread

class UMDCan():
    bus = can.interface.Bus(bustype='pcan', 
                            channel='PCAN_USBBUS1', 
                            bitrate=500000)

    def __init__(self):
        self.__reader    = CanReader(UMDCan.bus)
        self.__writer    = CanWriter(UMDCan.bus)
        self.MAX_VEL     = 7800
        self.INCREMENT   = 10.017
        self.DEGREE      = 0
        self.CUR_STATUS  = 0
        self.PRE_STATUS  = 0
        self.send_data   = 0

    def run(self, degree):
        self.DEGREE      = degree
        THRESHOLD        = self.MAX_VEL/(90) * degree

        while True:
            read_data = self.__reader.run()
            # print(read_data)

            self.compare(read_data, THRESHOLD)

    def compare(self, read_data, THRESHOLD):
        if read_data is not None:
            if read_data == 0:
                self.CUR_STATUS = 0
                self.send_data = 0

            elif THRESHOLD <= read_data <= 65535-THRESHOLD:
                self.CUR_STATUS = THRESHOLD

            right_rotate_data = read_data - 65535
            left_rotate_data  = read_data

            for i in range (8):
                if  int(self.INCREMENT * self.DEGREE) * (i+1) * (-1) < right_rotate_data < int(self.INCREMENT * self.DEGREE) * i* (-1):
                    self.CUR_STATUS = (-1) * (i+1)
                elif int(self.INCREMENT * self.DEGREE) * i < left_rotate_data < int(self.INCREMENT * self.DEGREE) * (i+1):
                    self.CUR_STATUS = i+1                                         
                # print("{0} {1}".format(right_rotate_data, left_rotate_data))

                if self.PRE_STATUS != self.CUR_STATUS:
                    print("prestatus : {0}, curstatus : {1}".format(self.PRE_STATUS, self.CUR_STATUS))

                    if self.CUR_STATUS == i+1:
                        self.send_data = pow(2,i+1) -1
                    elif self.CUR_STATUS == (-1) * (i+1):
                        self.send_data = pow(2,i+1) * (pow(2,8-(i+1))-1)
                    elif self.CUR_STATUS == THRESHOLD:
                        self.send_data = 0x81
                    self.write()
                    self.PRE_STATUS = self.CUR_STATUS


    def write(self):
        msg = can.Message(arbitration_id=0x181, data = [0x20, 0x00, 0x00, 0x01, self.send_data], extended_id=False)
        self.__writer.run(msg)

class CustomException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value

def raise_exception(err_msg):
    raise CustomException(err_msg)


if __name__ == "__main__":
    uc = UMDCan()
    # while True:

    try :
        while True:
            try :
                degree = int(input("원하는 각도를 입력하세요(90도 이하의 각도):  "))
                if  0 >= degree or degree >90:
                    raise_exception("90이하로 입력하세요")
                uc.run(degree)
            except CustomException as e:
                print(e)
            except :
                print("잘못된 입력입니다.")

    except KeyboardInterrupt:
        print("프로그램 종료")