import socket
from wifi_mod import *


class Socket(socket.socket):
    def __init__(self):
        super(Socket, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.IP = IP
        self.PORT = PORT
        self.CODING = 'utf-8'
        self.PACKAGE_SIZE = 2048
        self.CONNECTED = 'connected'
        self.type_object = None
        self._quit = False
        self.clients = []
        self.status = 'offline'
        self.data = ''

    def set_down(self):
        self.status = '[ client stopped ]'
        print(self.status)
        self._quit = True
        self.close()

    def set_up(self):
        raise NotImplemented()
