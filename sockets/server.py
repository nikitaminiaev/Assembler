#!/usr/bin/env python
import socket

from mySocket import Socket


class Server(Socket):

    def __init__(self):
        super(Server, self).__init__()
        self.quit = False
        self.clients = []

    def set_up(self):
        self.bind(('127.0.0.1', 1234))
        self.listen(5)
        print('Server listen')
        self.__accept_sockets()

    def send_data(self, data):
        for client in self.clients:
            client.send(data)

    def listen_socket(self, listened_socket: Socket = None):
        while True:
            data = listened_socket.recv(2048)
            self.send_data(data)

    def __accept_sockets(self):

        while not self.quit:
            try:
                client_socket, address = self.accept()
                print(f"client <{address[0]}> connected")

                self.clients.append(client_socket)

                client_socket.send("you are connected".encode('utf-8'))
                data = client_socket.recv(2048)
                print(data)
            except:
                print("\n[ Server Stopped]")
                self.quit = True
        self.close()


if __name__ == '__main__':
    server = Server()
    server.set_up()
