from socket import *
import time

#
UDP_IP = '13.124.19.161'
UDP_PORT = 5001
MESSAGE = "id:00001234"

print("UDP target IP : ", UDP_IP)
print("UDP target port : ", UDP_PORT)
print("MESSAGE : ", MESSAGE)

# init port:3334
csock = socket(AF_INET, SOCK_DGRAM)
csock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
csock.bind(('', 3334))

# sendto MSG, IP, PORT
csock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))

while True:
    data, addr = csock.recvfrom(1024)
    print("received msg : ", data, " from ", addr)
    # print('rece : ', data.decode('utf-8'))
    datas = data.decode('utf-8').split(',')

    if datas[0] == 'holl':
        addr = (datas[1], int(datas[2]))
        csock.sendto(MESSAGE.encode('utf-8'), addr)
        print('I sent to the web!!')
    elif datas[0] == 'get':
        info = datas[1]
        t = time.gmtime(1234567890)
        # time.time()
        print('info', info, 'time : ', time.asctime(t))