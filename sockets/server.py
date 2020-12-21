#!/usr/bin/env python
from mySocket import *
import threading


class Server(Socket):

    def __init__(self):
        super(Server, self).__init__()

    def set_up(self):
        self.bind((IP, PORT))
        self.listen(1)
        self.status = 'Server listen'
        print(self.status)

    def send_data_to_all_clients(self, data: str):
        for client in self.clients:
            client.send(data.encode(CODING))

    def accept_sockets(self):
        while not self.__quit:
            try:
                client_socket, address = self.accept()
                print(f"client <{address[0]}> connected")
                self.clients.append(client_socket)
                client_socket.send("you are connected".encode(CODING))
                data = client_socket.recv(2048)
                print(data.decode(CODING))
            except:
                self.status = "\n[ Server Stopped ]"
                print(self.status)
                self.__quit = True
                self.close()


if __name__ == '__main__':
    server = Server()
    server.set_up()
    threading.Thread(target=server.accept_sockets).start()
    if 0 in server.clients:
        server.send_data_to_all_clients('hi')