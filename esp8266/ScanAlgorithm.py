from dto import Dto, SENSOR_NAME


class ScanAlgorithm:

    def __init__(self):
        self.dto_x = Dto(SENSOR_NAME['SERVO_X'])
        self.dto_y = Dto(SENSOR_NAME['SERVO_Y'])
        self.dto_z = Dto(SENSOR_NAME['SERVO_Z'])
        self.stop = True

    def data_generator(self):
        for y in range(49):
            for x in range(49):
                yield x, y, 5
        self.stop = True
