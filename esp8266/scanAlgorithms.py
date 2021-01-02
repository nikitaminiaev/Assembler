import machine


class ScanAlgorithms:

    def __init__(self):
        self.servo_x = machine.PWM(machine.Pin(13), freq=50)
        self.servo_y = machine.PWM(machine.Pin(12), freq=50)
        # self.servo_z = machine.PWM(machine.Pin(5), freq=50)
        self.stop = True

    @staticmethod
    def process_data(data: dict):
        sensor = data['sensor']
        value = data['value']
        if -1 != (sensor.find('servo')):
            exec('self.%s.duty(%d)' % (sensor, value))
