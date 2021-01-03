class ScanAlgorithms:

    def __init__(self):
        self.stop = True

    def data_generator(self):
        for y in range(75):
            for x in range(75):
                yield x, y  # random.randint(5, 8)
        self.stop = True
