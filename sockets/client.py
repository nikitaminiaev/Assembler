#!/usr/bin/env python
from mySocket import Socket
import threading

class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.quit = False

    def set_up(self):
        try:
            self.connect(('127.0.0.3', 1234))
        except ConnectionRefusedError:
            print('Server is offline')
            exit(0)

    def send_data(self, data: str):
        try:
            self.send(data.encode('utf-8'))
        except:
            print("\n[ Server Stopped ]")
            self.quit = True
            self.close()

    def listen_server(self):
        while not self.quit:
            try:
                data = self.recv(2048)
                print(data.decode('utf-8'))
            except:
                print("\n[ Client Stopped ]")
                self.quit = True
                self.close()


if __name__ == '__main__':
    client = Client()
    client.set_up()
    threading.Thread(target=client.listen_server).start()
    client.send_data("fghfgh")
    client.send_data("fghfgh")
    client.send_data("fghfgh")
