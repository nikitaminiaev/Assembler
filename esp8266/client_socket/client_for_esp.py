from scanAlgorithms import ScanAlgorithms
from .mySocket import *
import ujson
import sys


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.data_prev = ''
        self.type_object = 'Client'
        self.scan_algorithms = ScanAlgorithms()

    def set_up(self):
        try:
            self.connect((IP, PORT))
        except Exception:
            self.status = 'Server is offline'
            print(self.status)
            sys.exit(0)
        self.listen_server()

    def listen_server(self):
        while not self._quit:
            try:
                self.data = self.recv(PACKAGE_SIZE).decode(CODING)
                if self.data == CONNECTED:
                    self.status = CONNECTED
                print(self.data)
                self.send_data('hi_esp8266')
                if (self.data_prev != self.data) and (CONNECTED != self.data):
                    parsed = ujson.loads(self.data)
                    self.scan_algorithms.process_data(parsed)
                    self.data_prev = self.data
            except:
                self.set_down()
                break

    def send_data(self, data: str):
        try:
            self.send(data.encode(CODING))
        except:
            self.set_down()




if __name__ == '__main__':
    client = Client()
    client.set_up()
