#!/usr/bin/env python
from mySocket import Socket


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.quit = False

    def set_up(self):
        try:
            self.connect(('127.0.0.1', 1234))
        except ConnectionRefusedError:
            print('Server is offline')
            exit(0)

    def send_data(self, data: str):
            self.send(data.encode('utf-8'))

    def listen_socket(self):
        while not self.quit:
            try:
                data = self.recv(2048)
                print(data.decode('utf-8'))
                self.send_data(input("::"))
            except:
                print("\n[ Server Stopped ]")
                self.quit = True
        self.close()


if __name__ == '__main__':
    client = Client()
    client.set_up()
    client.listen_socket()