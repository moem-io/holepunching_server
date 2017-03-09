from socket import *

svrsock = socket(AF_INET, SOCK_DGRAM)
svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
svrsock.bind(('', 5001))
s, addr = svrsock.recvfrom(1024)
print('s', s)
print('addr',addr)
svrsock.sendto('im server'.encode('utf-8'), addr)

# import socket
#
# UDP_IP = "127.0.0.1"
# UDP_PORT = 5005
# MESSAGE = "Hello, im server"
#
# print("UDP target IP : ", UDP_IP)
# print("UDP target port : ", UDP_PORT)
# print("MESSAGE : ", MESSAGE)
#
# sock = socket.socket(socket.AF_INET,
#                      socket.SOCK_DGRAM)
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
#
