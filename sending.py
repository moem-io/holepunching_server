import socket

UDP_IP = "13.124.19.161"
UDP_PORT = 42354
MESSAGE = "id:00001234"

print("UDP target IP : ", UDP_IP)
print("UDP target port : ", UDP_PORT)
print("MESSAGE : ", MESSAGE)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 3334))
sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
