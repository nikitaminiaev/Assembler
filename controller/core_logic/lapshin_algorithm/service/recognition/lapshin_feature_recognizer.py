from typing import Tuple, Iterator
import numpy as np
from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.service.feature_factory import FeatureFactory
from controller.core_logic.lapshin_algorithm.service.recognition.feature_recognizer_interface import FeatureRecognizerInterface


class LapshinFeatureRecognizer(FeatureRecognizerInterface):
    FULL_POINT_BYPASS = 9
    NOISE_COEF = 1  #todo подумать, возможн сделать настраиваемым параметром автоматически

    def __init__(self):
        self.__optimal_height = None

    def recognize_feature(self, figure: np.ndarray, surface: np.ndarray) -> Feature:
        center = self.get_center(figure)
        max_rad = self.calc_max_feature_rad(center, figure)
        rad = int(round(max_rad))
        max_height = self.get_max_height(surface[center[1]-rad*2:center[1]+rad*2, center[0]-rad*2:center[0]+rad*2].copy())
        return FeatureFactory.create(len(figure), max_rad, center[0], center[1], max_height)

    def recognize_all_figure_in_aria(self, surface: np.ndarray) -> Iterator[np.ndarray]:
        self.__optimal_height = self.calc_optimal_height(surface.copy())
        for y, row in enumerate(surface):
            for x, val in enumerate(row):
                if self.__is_start_point(val):
                    try:
                        figure = self.recognize_figure((x, y), surface, self.__optimal_height)
                    except IndexError as e:
                        print(e)
                        continue
                    yield figure

    def recognize_figure(self, start_point: Tuple[int, int], surface: np.ndarray, optimal_height: int) -> np.ndarray:
        figure = self.__bypass_feature(start_point, optimal_height, surface)
        self.__reset_to_zero_feature_area(figure, surface)
        return figure

    def feature_in_aria(self, coordinates: tuple, figure: np.ndarray) -> bool:
        figtr = np.transpose(figure)
        for st in range(np.min(figtr[0]), np.max(figtr[0]) + 1):
            fig1 = figtr[1][figtr[0] == st]
            for i in range(np.min(fig1), np.max(fig1) + 1):
                if (coordinates[0], coordinates[1]) == (st, i):
                    return True
        return False

    def get_center(self, figure: np.ndarray) -> Tuple[int, int]:
        _x_list = figure[:, 0]
        _y_list = figure[:, 1]
        _len = len(figure)
        _x = sum(_x_list) / _len
        _y = sum(_y_list) / _len
        return int(_x), int(_y)

    def calc_optimal_height(self, surface_copy: np.ndarray) -> int: # todo сделать приватным
        def recur_clip(arr: np.ndarray, next_to_clip: int):
            arr = np.clip(arr, 0, next_to_clip)
            if np.amax(arr) != int(arr.mean()):
                next_to_clip = recur_clip(arr, next_to_clip - 1)
            return next_to_clip

        return recur_clip(surface_copy, np.amax(surface_copy)) + self.NOISE_COEF

    def get_max_height(self, surface_copy: np.ndarray) -> int:
        return np.amax(surface_copy)

    def calc_max_feature_rad(self, center: tuple, figure: np.ndarray) -> float:
         for point in figure:
             point[0] = point[0] - center[0]
             point[1] = point[1] - center[1]

         return max(np.linalg.norm(vector) for vector in figure)


    def __reset_to_zero_feature_area(self, figure: np.ndarray, surface: np.ndarray):
        figtr = np.transpose(figure)
        for st in range(np.min(figtr[0]), np.max(figtr[0]) + 1):
            fig1 = figtr[1][figtr[0] == st]
            surface[np.min(fig1):np.max(fig1) + 1, st] = 0

    def __bypass_feature(self, start_point: Tuple[int, int], optimal_height: int, surface: np.ndarray) -> np.ndarray:
        x_start = start_point[0]
        y_start = start_point[1]
        points = np.array([[0, 0]], dtype='int8')
        x, y = x_start, y_start
        x_prev, y_prev = x_start, y_start
        max_iterations = 500
        i = 0
        while not self.__is_vector_entry(points, np.array([x_start, y_start], dtype='int8')):
            i += 1
            if i > max_iterations:
                raise RuntimeError('exceeding iterations of perimeter search')
            gen = self.__gen_bypass_point((x, y))
            for _ in range(self.FULL_POINT_BYPASS):
                try:
                    x, y = next(gen)
                except StopIteration:
                    break
                if surface[y, x] > optimal_height >= surface[y_prev, x_prev] \
                        and surface[y, x] > surface[y_prev, x_prev]:
                    points = np.append(points, [[x, y]], axis=0)
                    x_prev, y_prev = x, y
                    break
                x_prev, y_prev = x, y
        return np.delete(points, 0, 0)

    def __is_vector_entry(self, arr: np.ndarray, entry: np.ndarray) -> bool:
        return np.isclose(arr - entry, np.zeros(entry.shape)).all(axis=1).any()

    def __is_start_point(self, val: int) -> bool:
        return val > self.__optimal_height

    def __gen_bypass_point(self, point: Tuple[int, int]):
        """
            обход 8-ми точек против часовой от стартовой
        """
        x = point[0]
        y = point[1]
        y += 1
        yield x, y
        x -= 1
        yield x, y
        for _ in range(2):
            y -= 1
            yield x, y
        for _ in range(2):
            x += 1
            yield x, y
        for _ in range(2):
            y += 1
            yield x, y
        yield x - 1, y
