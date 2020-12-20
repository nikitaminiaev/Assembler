import socket


class Socket(socket.socket):
    def __init__(self):
        super(Socket, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

    def send_data(self, data):
        raise NotImplemented()

    def listen_socket(self, listened_socket: socket.socket = None):
        raise NotImplemented()

    def set_up(self):
        raise NotImplemented()
