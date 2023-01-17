from controller.core_logic.service.scanner_interface import ScannerInterface
import numpy as np


class ScannerAroundFeature:

    def __init__(self, feature_scanner: ScannerInterface):
        self.feature_scanner = feature_scanner

    def scan_aria_around_current_position(self, rad: int) -> np.ndarray:
        x_min, x_max, y_min, y_max = self.__calc_aria_borders(rad)
        return self.feature_scanner.scan_aria(x_min, y_min, x_max, y_max)

    def __calc_aria_borders(self, rad: int):
        x, y, _ = self.feature_scanner.get_current_position()
        x_min = int(x - rad)
        y_min = int(y - rad)
        x_max = int(x + rad + 1)
        y_max = int(y + rad + 1)
        return x_min, x_max, y_min, y_max
