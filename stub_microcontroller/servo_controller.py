from surface_generator import *
from noise_generator import NoiseGenerator

DEPARTURE_BY_Z = 10
OFFSET = 425

class ServoController:

    def __init__(self, external_send_func):
        self.external_send_func = external_send_func
        self.surface_generator = SurfaceGenerator(MAX_FIELD_SIZE, GENERAL_HEIGHT, ATOMS)
        self.noise_generator = NoiseGenerator()
        self.noise_generator.start()
        self.noise_surface = self.surface_generator.generate_noise_surface()
        self.x_current = 0 + OFFSET
        self.y_current = 0 + OFFSET
        self.z_current = 0

    def process_data(self, data: dict):
        sensor = data['sensor']
        value = int(data['value'])
        is_auto = False
        if 'auto' in data:
            is_auto = bool(data['auto'])
        if -1 != (sensor.find('servo_x')):
            self.x_current = value + OFFSET + self.noise_generator.x_offset
            print(self.noise_generator.x_offset)
            self.scan_algorithm_z()
        if -1 != (sensor.find('servo_y')):
            self.y_current = value + OFFSET + self.noise_generator.y_offset
            print(self.noise_generator.y_offset)
            self.scan_algorithm_z()
        if -1 != (sensor.find('servo_z')):
            self.z_current = value + DEPARTURE_BY_Z  # смещение мк по z, только при ручном управлении
            self.scan_algorithm_z()
            if is_auto:
                return
            if self.z_current == self.noise_surface[self.y_current, self.x_current]:
                self.z_current = self.z_current + DEPARTURE_BY_Z
                print(value)
                self.external_send_func(f'{{"sensor": "surface", "z_val": {value}}}')
        if sensor == 'gen_new_noise': # имитация реальности
            self.generate_new_noise()

    def scan_algorithm_z(self):
        for z in range(self.z_current, 0, -1):
            if z == self.noise_surface[self.y_current, self.x_current]:
                self.z_current = z + DEPARTURE_BY_Z
                self.external_send_func(f'{{"sensor": "surface", "z_val": {z}}}')
                break

    def generate_new_noise(self):
        self.noise_surface = self.surface_generator.generate_noise_surface()
        self.external_send_func('{}')  # обязательно должен быть ответ серверу иначе зависнит при следующем сообщении
