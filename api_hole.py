from socket import *

#
UDP_IP = ''
UDP_PORT = 5001

# init
svrsock = socket(AF_INET, SOCK_DGRAM)
svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
svrsock.bind((UDP_IP, UDP_PORT))

# receive and sendto
while True:
    data, addr = svrsock.recvfrom(1024)
    print("received msg : ", data, " from ", addr)

    print('addr[0]', addr[0])
    svrsock.sendto('im server'.encode('utf-8'), addr)