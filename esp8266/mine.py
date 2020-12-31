import machine
from client_socket.client_for_esp import Client

client = Client()
client.set_up()

servo = machine.PWM(machine.Pin(13), freq=50)
servo.duty(40)
servo.duty(115)
servo.duty(77)
