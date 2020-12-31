import random

from dto import Dto


class ScanAlgorithm:

    def __init__(self):
        self.dto_x = Dto(Dto.SERVO_X)
        self.dto_y = Dto(Dto.SERVO_Y)
        self.dto_z = Dto(Dto.SERVO_Z)
        self.stop = True

    def data_generator(self):
        for y in range(50):
            for x in range(50):
                yield x, y, random.randint(5, 8)
        self.stop = True
