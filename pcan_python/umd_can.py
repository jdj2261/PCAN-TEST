#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Summary         : 8CH RELAY BOARD lights up by receiving SAS CAN 
Copyright       : UNMANNED SOLUTION
Author          : DaeJong Jin (djjin@unmansol.com) 
Version         : v0.0.1 (June 15. 2020)
Created Date    : June 10. 2020
Completed Data  : June 15. 2020
'''

'''
RELAY2CAN 8CH
from http://rovitek.com/download/rp/RELAY2CAN-8CH/RELAY2CAN-8CH_E-RLY-CA_131_Manual.pdf
DATA DEFINITION
--------------------------------------------------------------
CANID RTR IDE DLC  D1   D2   D3   D4   D5  D6 D7 D8  Desc.
0x181  0   0  5   0x20 0x00 0x00 0x01 0xff X  X  X  0~7ch ON
0x181  0   0  5   0x20 0x00 0x00 0x01 0x00 X  X  X  0~7ch OFF
0x181  0   0  5   0x20 0x00 0x00 0x01 0x01 X  X  X  0ch   ON
0x181  0   0  5   0x20 0x00 0x00 0x01 0x02 X  X  X  1ch   ON
--------------------------------------------------------------

SAS CAN
Timestamp:  3218253.436089        ID: 02b0    S          DLC: 5    07 00 00 07 66
'''

'''
360도 : 3606
1도 : 10.017
'''

import can
import time
from mycan import CanReader, CanWriter, Logger
from threading import Thread

import os

current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = '{}/log'.format(current_dir)
# FILE_NAME = '{}/log'.format(current_dir)

MAX_VEL = 7800
INCREMENT = 10.017

class UmdCan():

    bus = can.interface.Bus(bustype='pcan',
                            channel='PCAN_USBBUS1',
                            bitrate=500000)

    """
    Relay LED lights after receiving SAS data
    """
    def __init__(self, degree):
        self.__reader = CanReader(UmdCan.bus)
        self.__writer = CanWriter(UmdCan.bus)
        self.log = Logger(log_dir, logname='SAS2RELAY')

        self.DEGREE = degree
        self.CUR_STATUS = 0
        self.PRE_STATUS = 0
        self.THRESHOLD = 0
        self._send_data = 0
        self.__MAX_VEL = MAX_VEL
        self.__INCREMENT = INCREMENT

        self.log.info('Start..')
        self.log.info(str(degree) + " degree input received")
    
    def run(self):
        self.THRESHOLD = self.__MAX_VEL if (
            self.__MAX_VEL/(90) * self.DEGREE > self.__MAX_VEL) else self.__MAX_VEL/(90) * self.DEGREE

        read_data = self.__reader.run()
        # print(read_data)
        self.compare(read_data)
        """
        read and process data
        Parameter: degree(Input degree)
        Return: None
        """

    def compare(self, read_data):

        POSITIVE_DIRECTION = 1
        NEGATIVE_DIRECTION = -1

        if read_data is not None:
            """
            Classification of received data
            """
            right_rotate_data = read_data - 65535
            left_rotate_data = read_data

            if read_data == 0:
                self.CUR_STATUS = 0
                self._send_data = 0

            elif self.THRESHOLD <= read_data <= 65535-self.THRESHOLD:
                self.CUR_STATUS = self.THRESHOLD

            for i in range(8):
                """     
                Determine whether it is positive or negative direction
                Counterclockwise : positive direction
                Clockwise : negative direction
                """
                right_cond1 = int(self.__INCREMENT * self.DEGREE) * (i+1) * (-1)
                right_cond2 = int(self.__INCREMENT * self.DEGREE) * i * (-1)
                left_cond1 = int(self.__INCREMENT * self.DEGREE) * i
                left_cond2 = int(self.__INCREMENT * self.DEGREE) * (i+1)
                if right_cond1 < right_rotate_data < right_cond2:
                    NEGATIVE_DIRECTION = (-1) * (i+1)
                    self.CUR_STATUS = NEGATIVE_DIRECTION
                elif left_cond1 < left_rotate_data < left_cond2:
                    POSITIVE_DIRECTION = i+1
                    self.CUR_STATUS = POSITIVE_DIRECTION
                # print("Left rotate: {0} Right rotate: {1}".format(left_rotate_data, right_rotate_data))

                """
                Send can data 
                when the current state is different 
                from the previous state
                """
                if self.PRE_STATUS != self.CUR_STATUS:
                    print("prestatus : {0}, curstatus : {1}".format(
                        self.PRE_STATUS, self.CUR_STATUS))

                    if self.CUR_STATUS == POSITIVE_DIRECTION:
                        self._send_data = pow(2, i+1) - 1
                        
                    elif self.CUR_STATUS == NEGATIVE_DIRECTION:
                        self._send_data = pow(2, i+1) * (pow(2, 8-(i+1))-1)

                    elif self.CUR_STATUS == self.THRESHOLD:
                        self._send_data = 0x81
                        print("OVERRIDE: {0}".format(bin(self._send_data)))
                        self.log.warning("OVERRIDE")

                    self.log_rotate(self._send_data)
                    self.write(self._send_data)
                    self.PRE_STATUS = self.CUR_STATUS
        """
        After determining whether the current SAS direction is positive or negative, 
        and rotating by the entered degree, 
        the LEDs turn on one by one.
        Parameter: data(Filtered data)
        Return: None
        """

    def log_rotate(self, data):
        if self.CUR_STATUS > self.PRE_STATUS:
            print("LEFT ROTATE: {0}".format(bin(data)))
            log_data = "LEFT ROTATE: " + "{0:b}".format(data).zfill(8)
            self.log.info(log_data)
        else:
            print("RIGHT ROTATE: {0}".format(bin(data)))
            log_data = "RIGHT ROTATE: " + "{0:b}".format(data).zfill(8)
            self.log.info(log_data)
        """
        Shows which direction to rotate and what data to send
        Parameter: data(Send data)
        Return: None
        """
    def write(self, read_data):
        msg = can.Message(arbitration_id=0x181, data=[
                          0x20, 0x00, 0x00, 0x01, read_data], extended_id=False)
        self.__writer.run(msg)

        """
        send can data
        Parameter: data(Filtered data)
        Return: None
        """

# class CustomException(Exception):
    # def __init__(self, value):
        # self.value = value
# 
    # def __str__(self):
        # return self.value
# 
# def raise_exception(err_msg):
    # raise CustomException(err_msg)

if __name__ == "__main__":
    
    # while True:

    while True:
        try:
            degree = int(input("원하는 각도를 입력하세요(90도 이하의 각도): "))
            uc = UmdCan(degree)
            while True:
                uc.run()
        # except CustomException as e:
        #     print(e)
        except KeyboardInterrupt:
            uc.log.error("프로그램 강제 종료..")
            print("\n프로그램 종료...")
            exit(0)
        # except NameError:
        #     print("잘못된 입력입니다.")
