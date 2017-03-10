from socket import *

#
UDP_IP = '13.124.19.161'
UDP_PORT = 5001
MESSAGE = "Hi Im web!!"

print("UDP target IP : ", UDP_IP)
print("UDP target port : ", UDP_PORT)
print("MESSAGE : ", MESSAGE)

# init port:3334
csock = socket(AF_INET, SOCK_DGRAM)
csock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
csock.bind(('', 5001))

# sendto MSG, IP, PORT
csock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
print("send")