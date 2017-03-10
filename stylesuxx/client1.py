#!/usr/bin/env python
"""UDP hole punching client."""
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import sys


class ClientProtocol(DatagramProtocol):
    """
    Client protocol implementation.

    The clients registers with the rendezvous server.
    The rendezvous server returns connection details for the other peer.
    The client Initializes a connection with the other peer and sends a
    message.
    """

    def startProtocol(self):
        """Register with the rendezvous server."""
        self.server_connect = False
        self.peer_init = False
        self.peer_connect = False
        self.peer_address = None
        self.transport.write('0'.encode('utf-8'), (sys.argv[1], int(sys.argv[2])))

    def toAddress(self, data):
        """Return an IPv4 address tuple."""
        ip, port = data.split(':')
        return (ip, int(port))

    def datagramReceived(self, datagram, host):
        """Handle incoming datagram messages."""
        if not self.server_connect:
            self.server_connect = True
            self.transport.write('ok'.encode('utf-8'), (sys.argv[1], int(sys.argv[2])))
            print('Connected to server, waiting for peer...')

        elif not self.peer_init: # 서버에서 둘 다 연결 되었을 때 이 조건 실행
            self.peer_init = True
            self.peer_address = self.toAddress(datagram.decode())
            self.transport.write('init'.encode('utf-8'), self.peer_address) # 이 때 peer_address는 컨트롤대쉬보드. 컨대한테 init을 보내면 컨대는 Message from어쩌고 보냄
            print ('Sent init to %s:%d' % self.peer_address)

        elif not self.peer_connect: # 컨대가 Message어쩌고 보내면 여기서 받아서 컨대한테도 메시지 보내줌
            self.peer_connect = True
            print('from foreign : ', datagram)
            host = self.transport.getHost().host
            host = 'Im mac'
            port = self.transport.getHost().port
            msg = 'Message from %s:%d' % (host, port)
            self.transport.write(msg.encode('utf-8'), self.peer_address)

        else:
            print ('Received:', datagram)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("Usage: ./client RENDEZVOUS_IP RENDEZVOUS_PORT")
        sys.exit(1)

    protocol = ClientProtocol()
    t = reactor.listenUDP(0, protocol)
    reactor.run()