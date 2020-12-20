import socket


class Socket(socket.socket):
    def __init__(self):
        super(Socket, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

    async def send_data(self, data):
        raise NotImplemented()

    async def listen_socket(self, listened_socket: socket.socket = None):
        raise NotImplemented()

    async def set_up(self):
        raise NotImplemented()
