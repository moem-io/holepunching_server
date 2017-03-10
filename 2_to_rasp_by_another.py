from socket import *

#
UDP_IP = '61.43.139.4'
UDP_PORT = 50343
MESSAGE = "get,info"

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