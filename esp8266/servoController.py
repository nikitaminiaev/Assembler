import machine

MAX = 75
CORRECT_FOR_CARRENT_WORKE = 40


class ServoController:

    def __callback(self, arg):
        if str(arg) == 'Pin(0)':
            self.external_send_func('{"sensor": "atom", "val": 1}')
        if str(arg) == 'Pin(2)':
            self.external_send_func('{"sensor": "surface", "val": 1}')

    def __init__(self, external_send_func):
        self.external_send_func = external_send_func
        self.servo_x = machine.PWM(machine.Pin(13), freq=50)
        self.servo_y = machine.PWM(machine.Pin(12), freq=50)
        self.servo_z = machine.PWM(machine.Pin(5), freq=50)
        self.hall_sensor = machine.Pin(0, machine.Pin.IN)
        self.hall_sensor.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.__callback)
        self.surface_sensor = machine.Pin(2, machine.Pin.IN)
        self.surface_sensor.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.__callback)

    def process_data(self, data: dict):
        sensor = data['sensor']
        value = int(data['value']) + CORRECT_FOR_CARRENT_WORKE
        if -1 != (sensor.find('servo')):
            exec('self.%s.duty(%d)' % (sensor, value), {}, {'self': self})

    @staticmethod
    def __invert_data(data: dict):
        data['value'] = str(MAX - int(data['value']))
        return data