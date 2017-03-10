from socket import *

csock = socket(AF_INET, SOCK_DGRAM)
csock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
csock.bind(('', 3334))
csock.sendto('im client'.encode('utf-8'), ('13.124.19.161', 5001))
s, addr = csock.recvfrom(1024)
print('s', s)
print('addr', addr)

