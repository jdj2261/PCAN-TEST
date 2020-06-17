
# result = 0
# # for i in range (8):
# test = 0
# test2 = test | 0b00000001
# print(bin(test2))

test = 0b00011101111
test1 = 0b00000111
result = test & test1
print("{0:08b}".format(result))
print(bin(result))

data = 0b00000001
for i in range(8):
    test = ((data << i) | data) | test
    # print("Test{0} : {1}".format(i,bin(test)))
    # test = test | data

print(test)
# send_data = ((data << i) | data) | send_data 

# data = (data[0]<<0) | (data[1]<<8) | (data[2]<<16) | (data[3]<<24)
# print(hex(data))