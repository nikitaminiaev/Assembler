import socket

IP = '192.168.0.104'
PORT = 8266
CODING = 'utf-8'
PACKAGE_SIZE = 2048
CONNECTED = 'connected'


class Socket(socket.socket):
    def __init__(self):
        super(Socket, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.type_object = None
        self._quit = False
        self.clients = []
        self.status = 'offline'
        self.data = ''

    def set_down(self):
        self.status = f"\n[ {self.type_object} stopped ]"
        print(self.status)
        self._quit = True
        self.close()

    def set_up(self):
        raise NotImplemented()
