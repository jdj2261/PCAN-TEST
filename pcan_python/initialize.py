import can
import time

'''
SAS에 ID 0x7C0로 아래의 값을 순차적으로 보내면 현재 값에서 초기화
1. 05 2B
2. 03 2B
'''

bus = can.interface.Bus(bustype='pcan',
                        channel='PCAN_USBBUS1',
                        bitrate=500000)

msg1 = can.Message(arbitration_id=0x7C0, data=[0x2B, 0x05], extended_id=False)
bus.send(msg1)
print("0x05, 0x2B Send~")
time.sleep(1)
msg2 = can.Message(arbitration_id=0x7C0, data=[0x2B, 0x03], extended_id=False)
bus.send(msg2)
print("0x03, 0x2B Send~")

print("Initialize~~")