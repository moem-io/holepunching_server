from socket import *

svrsock = socket(AF_INET, SOCK_DGRAM)
svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
svrsock.bind(('', 5001))
s, addr = svrsock.recvfrom(1024)
print('s', s)
print('addr',addr)
svrsock.sendto('im server'.encode('utf-8'), addr)

