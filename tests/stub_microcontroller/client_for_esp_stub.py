import ujson
import sys
from mySocket_stub import Socket
from servoController import ServoController


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.data_prev = ''
        self.type_object = 'Client'
        self.servoController = ServoController(self.send_data)

    def set_up(self):
        try:
            self.connect((self.IP, self.PORT))
        except Exception as e:
            self.status = 'Server is offline'
            print(str(e))
            sys.exit(0)
        self.listen_server()

    def listen_server(self):
        while not self._quit:
            try:
                data = self.recv(self.PACKAGE_SIZE).decode(self.CODING)
                if data == self.CONNECTED:
                    self.status = self.CONNECTED
                    self.send_data('hi_esp8266')
                if self.data_prev != data and self.CONNECTED != data:
                    try:
                        parsed = ujson.loads(data)
                        self.servoController.process_data(parsed)
                    except ValueError as e:
                        self.send_data(str(e))
                    finally:
                        self.data_prev = data
            except Exception as e:
                self.send_data(str(e))
                self.set_down()
                break

    def send_data(self, data: str):
        try:
            self.send(data.encode(self.CODING))
        except:
            self.set_down()


if __name__ == '__main__':
    client = Client()
    client.set_up()
