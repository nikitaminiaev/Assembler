#!/usr/bin/env python
from mySocket import Socket


class Server(Socket):

    def __init__(self):
        super(Server, self).__init__()
        self.quit = False
        self.listen(1)
        self.clients = []
        print('Server listen')

    async def set_up(self):
        self.bind(('127.0.0.1', 1234))
        await self.__accept_sockets()

    async def send_data(self, data):
        for client in self.clients:
            client.send(data)

    async def listen_socket(self, listened_socket: Socket = None):
        while True:
            data = listened_socket.recv(2048)
            await self.send_data(data)

    async def __accept_sockets(self):

        while not self.quit:
            try:
                user_socket, address = self.accept()
                print(f"client <{address[0]}> connected")

                self.clients.append(user_socket)

                user_socket.send('you are connected'.encode('utf-8'))
                data = user_socket.recv(2048)
                print(data)
            except:
                print("\n[ Server Stopped]")
                self.quit = True
        self.close()


if __name__ == '__mane__':
    server = Server()
    server.set_up()
