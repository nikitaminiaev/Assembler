import random

FIELD_SIZE = 75


class ScanAlgorithms:

    def __init__(self):
        self.stop = True

    def data_generator(self):
        for y in range(FIELD_SIZE):
            if y % 2 == 0:
                for x in range(FIELD_SIZE):
                    yield x, y, random.randint(5, 8)
            else:
                for x in range(FIELD_SIZE, -1, -1):
                    yield x, y, random.randint(5, 8)

        self.stop = True
