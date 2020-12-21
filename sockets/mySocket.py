import socket

IP = '127.0.0.3'
PORT = 1234
CODING = 'utf-8'


class Socket(socket.socket):
    def __init__(self):
        super(Socket, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.__quit = False
        self.clients = []
        self.status = ''

    def set_up(self):
        raise NotImplemented()
