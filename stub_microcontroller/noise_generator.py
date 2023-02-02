import random
import threading
from time import sleep

import numpy as np


class NoiseGenerator:

    def __init__(self, shutdown: threading.Event):
        self.shutdown = shutdown
        self.x_offset = 0
        self.y_offset = 0

    def start_gen_offset(self, shutdown: threading.Event):
        threading.Thread(target=self.gen_thermal_offset_x, args=(shutdown,)).start()
        threading.Thread(target=self.gen_thermal_offset_y, args=(shutdown,)).start()

    def gen_sharp_fluctuations(self) -> None:
        pass

    def gen_thermal_offset_x(self, shutdown: threading.Event) -> None:
        while not shutdown.is_set():
            self.x_offset += self.__get_offset()

    def gen_thermal_offset_y(self, shutdown: threading.Event) -> None:
        while not shutdown.is_set():
            self.y_offset += self.__get_offset()

    def __get_offset(self):
        delay = 0.2
        if bool(random.getrandbits(1)):
            delay += 0.5 * random.random()
        else:
            delay -= 0.5 * random.random()
        sleep(abs(delay))
        return random.randint(0, random.randint(0, 1))

    @staticmethod
    def gen_random_noise(max_field_size: int) -> np.ndarray:
        return np.random.choice([-1, 0, +1], (max_field_size, max_field_size), replace=True, p=[0.2, 0.6, 0.2])
