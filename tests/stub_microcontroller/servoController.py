from surface_generator import SurfaceGenerator, MAX_FIELD_SIZE

CORRECT_FOR_CARRENT_WORKE = 30

class ServoController:

    def __init__(self, external_send_func):
        self.external_send_func = external_send_func
        self.real_surface = SurfaceGenerator(MAX_FIELD_SIZE).generate()
        self.x_current = 0
        self.y_current = 0
        self.z_current = 0

    def process_data(self, data: dict):
        sensor = data['sensor']
        value = int(data['value']) - CORRECT_FOR_CARRENT_WORKE
        if -1 != (sensor.find('servo_x')):
            self.x_current = value
            print('x' + str(value))
        if -1 != (sensor.find('servo_y')):
            self.y_current = value
            print('y' + str(value))
        if -1 != (sensor.find('servo_z')):
            self.z_current = value
            if self.z_current == self.real_surface[self.y_current, self.x_current]:
                self.external_send_func('{"sensor": "surface", "val": 1}')
            print('z' + str(value))
