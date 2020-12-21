#!/usr/bin/env python
from mySocket import *
import threading


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        try:
            self.connect((IP, PORT))
        except ConnectionRefusedError:
            self.status = 'Server is offline'
            print(self.status)
            exit(0)

    def send_data(self, data: str):
        try:
            self.send(data.encode(CODING))
        except:
            self.status = "\n[ Client Stopped ]"
            print(self.status)
            self.__quit = True
            self.close()

    def listen_server(self):
        while not self.__quit:
            try:
                data = self.recv(2048)
                print(data.decode(CODING))
            except:
                self.status = "\n[ Client Stopped ]"
                print(self.status)
                self.__quit = True
                self.close()


if __name__ == '__main__':
    client = Client()
    client.set_up()
    threading.Thread(target=client.listen_server).start()
    client.send_data("fghfgh")
    client.send_data("fghfgh")
    client.send_data("fghfgh")
