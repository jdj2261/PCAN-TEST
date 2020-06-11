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

import can
import time
from mycan.read import CanReader
from mycan.write import CanWriter



class UMDCan():
    bus = can.interface.Bus(bustype='pcan', 
                            channel='PCAN_USBBUS1', 
                            bitrate=500000)

    def __init__(self):

        self.__reader = CanReader(UMDCan.bus)
        self.__writer = CanWriter(UMDCan.bus)

    def compare(self):
        
        curstatus = 0
        prestatus = 0
        while True:

            read_data = self.__reader.receive_all()


            if read_data is not None:

                print("pre : {0} cur : {1}".format(prestatus, curstatus))
                read_data = self.__reader.convert_int()
                print(read_data)

                '''
                1 바퀴 : 3606
                360도 : 3606
                1도 : 10.017

                default resolution = 10.017


                -90 <read_Data - 65535 < 0
                
                read_data = 0
                0 < read_data < 90

                current status
                previous status

                '''

                if 0 > read_data-65535 > -900:
                    curstatus = -1
                    # print(read_data-65535 )
                    print(-90)
                
                elif -900 > read_data-65535 > -1800:
                    curstatus = -2
                    # print(read_data-65535 )
                    print(-180)           
                
                elif 0< read_data<900:
                    curstatus = 1
                    print(90)
                elif read_data > 1800:
                    curstatus = 2
                    print(180)

                elif read_data == 0:
                    curstatus = 0
                    print(0)
                
                print("status : %d"%curstatus)


                if prestatus != curstatus:
                    # if curstatus == 1:
                    if curstatus == 1:
                        print("curstatus : {0}".format(curstatus))
                    print("CHANGE")
                    print("pre : {0} cur : {1}".format(prestatus, curstatus))
                    prestatus = curstatus


                # prestatus = curstatus
                # print("2 pre status : %d"%prestatus)

                # print("2 pre status : %d"%prestatus)
                
                # else :
                #     prestatus = curstatus




if __name__ == "__main__":
    uc = UMDCan()
    # while True:
    uc.compare()