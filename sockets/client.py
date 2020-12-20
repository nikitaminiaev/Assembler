#!/usr/bin/env python
from mySocket import Socket


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

    async def set_up(self):
        try:
            self.connect(('127.0.0.1', 1234))
        except ConnectionRefusedError:
            print('Server is offline')
            exit(0)
        self.setblocking(False)

    async def listen_socket(self, listened_socket: Socket = None):
        while True:
            data = self.recv(2048)
            print(data.decode('utf-8'))
            self.send(input("::").encode('utf-8'))

    async def send_server(self):
        self.send(input("::").encode('utf-8'))


if __name__ == '__mane__':
    client = Client()
    client.send_server()
