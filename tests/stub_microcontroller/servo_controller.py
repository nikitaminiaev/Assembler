from surface_generator import SurfaceGenerator, MAX_FIELD_SIZE


class ServoController:

    def __init__(self, external_send_func):
        self.external_send_func = external_send_func
        self.real_surface = SurfaceGenerator(MAX_FIELD_SIZE, 20).generate()
        self.x_current = 0
        self.y_current = 0
        self.z_current = 0

    def process_data(self, data: dict):
        sensor = data['sensor']
        value = int(data['value'])
        is_auto = False
        if 'auto' in data:
            is_auto = bool(data['auto'])
        else:
            print('de_' + str(data))
        if -1 != (sensor.find('servo_x')):
            self.x_current = value
            # print('x' + str(value)) # смещение мк по x
            self.scan_algorithm_z(is_auto)
        if -1 != (sensor.find('servo_y')):
            self.y_current = value
            # print('y' + str(value)) # смещение мк по y
            self.scan_algorithm_z(is_auto)
        if -1 != (sensor.find('servo_z')):
            self.z_current = value + 10 # смещение мк по z, только при ручном управлении
            print('de_' + 'руч z')  #todo откуда это приходит??? - риходит из controller/core_logic/scan_algorithms.py:60
            self.scan_algorithm_z(is_auto)
            if is_auto:
                return
            if self.z_current == self.real_surface[self.y_current, self.x_current]:
                self.z_current = self.z_current + 10
                self.external_send_func(f'{{"sensor": "surface", "z_val": {value}}}')
            print('z' + str(value))

    def scan_algorithm_z(self, is_auto: bool):
        # print('de' + str(is_auto))
        # if not is_auto:
        #     return
        for z in range(self.z_current, 0, -1):
            if z < 19: print('de_z' + str(z))
            if z == self.real_surface[self.y_current, self.x_current]:
                self.external_send_func(f'{{"sensor": "surface", "z_val": {z}}}')
                self.z_current = z + 10
                break
