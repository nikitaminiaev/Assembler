#!/usr/bin/env python
import threading
from sockets.mySocket import *

COUNT_CONNECTIONS = 1


class Server(Socket):

    def __init__(self, external_handle_func):
        super(Server, self).__init__()
        self.type_object = 'Server'
        self.external_handle_func = external_handle_func

    def set_up(self):
        self.bind((IP, PORT))
        self.listen(COUNT_CONNECTIONS)
        self.status = 'Server listen'
        print(self.status)
        threading.Thread(target=self.accept_sockets).start()

    def send_data_to_all_clients(self, data: str):
        for client in self.clients:
            client.send(data.encode(CODING))

    def listen_client(self, client):
        while not self._quit:
            try:
                data = client.recv(PACKAGE_SIZE).decode(CODING)
                self.handle_data_from_client(data)
            except:
                self.set_down()

    def handle_data_from_client(self, data: str):
        self.external_handle_func(data)
        print(data)

    def accept_sockets(self):
        while not self._quit:
            try:
                client_socket, address = self.accept()
                self.clients.append(client_socket)
                client_socket.send(CONNECTED.encode(CODING))
                data_from_client = client_socket.recv(PACKAGE_SIZE).decode(CODING)
                print(data_from_client)
                threading.Thread(target=self.listen_client, args=(client_socket,)).start()
            except:
                self.set_down()


if __name__ == '__main__':
    server = Server()
    server.set_up()
    if 1 in server.clients:
        server.send_data_to_all_clients('hi')
