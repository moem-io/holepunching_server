from socket import *

#
UDP_IP = ''
UDP_PORT = 5001

# init
svrsock = socket(AF_INET, SOCK_DGRAM)
svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
svrsock.bind((UDP_IP, UDP_PORT))

# rasp IP PORT
RASP = None
RASP_IP = None
RASP_PORT = None

# receive and sendto
while True:
    data, addr = svrsock.recvfrom(1024)
    print("received msg : ", data, " from ", addr)

    print('addr[0]', addr[0])
    if addr[0] == '52.79.188.83' and not RASP:
        # svrsock.sendto('holl'.encode('utf-8'), (RASP_IP, RASP_PORT))
        svrsock.sendto('holl'.encode('utf-8'), RASP)
    else:
        RASP = addr
        svrsock.sendto('im server, nice to meet you rasp!!'.encode('utf-8'), addr)