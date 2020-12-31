import machine
from client_socket.client_for_esp import Client


class Mine:

    def __init__(self):
        self.client = Client()
        self.client.set_up()



if __name__ == '__main__':
    client = Client()
    client.set_up()

    servo = machine.PWM(machine.Pin(13), freq=50)  # 7 номер
    servo.duty(40)
    servo.duty(115)
    servo.duty(77)
