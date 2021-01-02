#!/usr/bin/env python
from sockets.mySocket import *
import threading


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.type_object = 'Client'

    def set_up(self):
        try:
            self.connect((IP, PORT))
        except ConnectionRefusedError:
            self.status = 'Server is offline'
            print(self.status)
            exit(0)
        threading.Thread(target=self.listen_server).start()

    def send_data(self, data: str):
        try:
            self.send(data.encode(CODING))
        except:
            self.set_down()

    def listen_server(self):
        while not self._quit:
            try:
                self.data = self.recv(PACKAGE_SIZE).decode(CODING)
                if self.data == CONNECTED:
                    self.status = CONNECTED
                print(self.data)
                self.send_data('hi')
            except:
                self.set_down()
                break


if __name__ == '__main__':
    client = Client()
    client.set_up()
