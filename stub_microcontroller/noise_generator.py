import random
import threading
from time import sleep

import numpy as np


class NoiseGenerator:

    def __init__(self):
        self.x_offset = 0
        self.y_offset = 0
        self.stop = False

    def start(self):
        threading.Thread(target=self.gen_thermal_offset_x).start()
        threading.Thread(target=self.gen_thermal_offset_y).start()
        pass

    def gen_sharp_fluctuations(self) -> None:
        pass

    def gen_thermal_offset_x(self) -> None:
        delay = 0.2
        while not self.stop:
            sleep(abs(delay))
            self.x_offset += random.randint(0, random.randint(0, 1))
            if bool(random.getrandbits(1)):
                delay += 0.5 * random.random()
            else:
                delay -= 0.5 * random.random()

    def gen_thermal_offset_y(self) -> None:
        delay = 0.2
        while not self.stop:
            sleep(abs(delay))
            self.y_offset += random.randint(0, random.randint(0, 1))
            if bool(random.getrandbits(1)):
                delay += 0.5 * random.random()
            else:
                delay -= 0.5 * random.random()

    @staticmethod
    def gen_random_noise(max_field_size: int) -> np.ndarray:
        return np.random.choice([-1, 0, +1], (max_field_size, max_field_size), replace=True, p=[0.2, 0.6, 0.2])
