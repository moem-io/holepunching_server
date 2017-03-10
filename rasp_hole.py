from socket import *

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
    if str(data) == 'holl':
        csock.sendto(MESSAGE.encode('utf-8'), addr)
        print('I sent to the web!!')