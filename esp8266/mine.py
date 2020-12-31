import machine

servo = machine.PWM(machine.Pin(13), freq=50)
servo.duty(40)
servo.duty(115)
servo.duty(77)
