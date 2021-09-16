#!/usr/bin/env python
import threading
from sockets.mySocket import *

COUNT_CONNECTIONS = 1


class Server(Socket):

    def __init__(self):
        super(Server, self).__init__()
        self.type_object = 'Server'

    def set_up(self):
        self.bind((IP, PORT))
        self.listen(COUNT_CONNECTIONS)
        self.status = 'Server listen'
        print(self.status)
        threading.Thread(target=self.accept_sockets).start()

    def send_data_to_all_clients(self, data: str):
        for client in self.clients:
            client.send(data.encode(CODING))

    def accept_sockets(self):
        while not self._quit:
            try:
                client_socket, address = self.accept()
                self.clients.append(client_socket)
                client_socket.send(CONNECTED.encode(CODING))
                self.data = client_socket.recv(PACKAGE_SIZE).decode(CODING)
                print(self.data)
            except:
                self.set_down()


if __name__ == '__main__':
    server = Server()
    server.set_up()
    if 1 in server.clients:
        server.send_data_to_all_clients('hi')
