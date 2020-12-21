#!/usr/bin/env python
from mySocket import Socket
import threading

class Server(Socket):

    def __init__(self):
        super(Server, self).__init__()
        self.quit = False
        self.clients = []

    def set_up(self):
        self.bind(('127.0.0.3', 1234))
        self.listen(1)
        print('Server listen')
        # self.accept_sockets()

    def send_data_to_all_clients(self, data: str):
        for client in self.clients:
            client.send(data.encode('utf-8'))

    def accept_sockets(self):
        while not self.quit:
            try:
                client_socket, address = self.accept()
                print(f"client <{address[0]}> connected")
                self.clients.append(client_socket)
                client_socket.send("you are connected".encode('utf-8'))
                data = client_socket.recv(2048)
                print(data.decode('utf-8'))
            except:
                print("\n[ Server Stopped ]")
                self.quit = True
                self.close()


if __name__ == '__main__':
    server = Server()
    server.set_up()
    threading.Thread(target=server.accept_sockets).start()
    if 0 in server.clients:
        server.send_data_to_all_clients('hi')