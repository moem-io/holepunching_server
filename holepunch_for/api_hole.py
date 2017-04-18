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

print('server is listening at', UDP_PORT)
# receive and sendto
while True:
    data, addr = svrsock.recvfrom(1024)
    print("received msg : ", data, " from ", addr)

    print('addr[0]', addr[0])
    if addr[0] == '52.79.188.83' and RASP:
        svrsock.sendto(('holl,'+addr[0]+','+str(addr[1])).encode('utf-8'), RASP)
        print('debug : hole info')
    elif not addr[0] == '52.79.188.83':
        RASP = addr
        svrsock.sendto('im server, nice to meet you rasp!!'.encode('utf-8'), addr)
        print('debug : hi rasp')
    else:
        svrsock.sendto('not yet web..!! rasp first'.encode('utf-8'), addr)
        print('debug : not yet..')