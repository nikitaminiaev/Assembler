import threading
from threading import Event
import numpy as np
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature_interface import BindingProbeToFeatureInterface
from controller.core_logic.lapshin_algorithm.feature_collection.doubly_linked_list import DoublyLinkedList
from controller.core_logic.lapshin_algorithm.service.recognition.feature_recognizer_interface import \
    FeatureRecognizerInterface
from controller.core_logic.lapshin_algorithm.service.scanner_around_feature import ScannerAroundFeature
from controller.core_logic.service.scanner_interface import ScannerInterface

"""
при создании затравки производится поиск такого атома, который расположен под
наименьшим углом к прямой, задающей направление движения. Найденный атом полу-
чает ярлык “следующий”. Причём, при перемещении вдоль кристаллографического на-
правления положение следующего атома цепочки используется для уточнения направле-
ния движения, если изменение локальной кривизны цепочки лежит в заданных пределах.
Таким образом, указанный приём позволяет удерживать выбранное направление, легко
минуя те места на поверхности кристалла, где расположены точечные дефекты решётки.
"""

"""
В случае, когда выполняется обход затравки с присоединением (см. Рис. 5 и Рис. 8),
вначале выполняется сортировка: среди атомов выбираются те, что не принадлежат к
уже пройденной цепочке. После чего среди отобранных ищется тот, что расположен под
наибольшим (наименьшим) углом (отсчёт угла в обоих случаях производится вокруг “те-
кущего” атома в направлении против часовой стрелки) к отрезку, соединяющему “теку-
щий” и “предыдущий” атомы при обходе контура цепочки против часовой стрелки (по ча-
совой стрелке). Найденный таким образом атом принимается за “следующий” атом це-
почки.
"""

"""
Надо искать следующий атом цепочки по предположительному направлению движения. Найдя распознать его определить, 
привязаться, определить относительные координаты к предыдущему и перепрыгивать между ними для усреднения.  
"""


class FeatureSearcher:

    def __init__(self,
                 binding_to_feature: BindingProbeToFeatureInterface,
                 feature_scanner: ScannerInterface,
                 feature_recognizer: FeatureRecognizerInterface,
                 binding_in_delay: Event,
                 allow_binding: Event
                 ):
        self.feature_scanner = feature_scanner
        self.local_surface = None
        self.binding_to_feature = binding_to_feature
        self.feature_recognizer = feature_recognizer
        self.structure_of_feature = DoublyLinkedList()
        self.binding_in_delay = binding_in_delay
        self.allow_binding = allow_binding
        self.scanner_around_feature = ScannerAroundFeature(feature_scanner)

    def search_features(self):
        surface = self.feature_scanner.scan_aria()
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface.copy())
        first_figure = next(figure_gen)
        self.find_first_feature(first_figure, surface)
        while self.structure_of_feature.count < 5:
            self.binding_in_delay.wait()
            self.allow_binding.clear()
            surface = self.scanner_around_feature.scan_aria_around_feature(self.structure_of_feature.get_current_feature(), 5)
            self.allow_binding.set()
            self.find_next_feature(surface)

    def find_first_feature(self, figure: np.ndarray, surface: np.ndarray):
        feature = self.feature_recognizer.recognize_feature(figure, surface)
        self.structure_of_feature.insert_to_end(feature)
        self.binding_to_feature.set_current_feature(feature)
        threading.Thread(target=self.binding_to_feature.bind_to_current_feature).start()

    def find_next_feature(self, surface: np.ndarray):
        vectors_to_neighbors = self.__calc_vectors_to_neighbors(surface)
        next_direction = self.structure_of_feature.get_next_direction()

        self.find_close_vector(vectors_to_neighbors, next_direction)

        # расчитать угол между векторами направления движения и найденной фичой
        # если угол > 90 то надо увеличивать аппертуру, чтобы искать дургие фичи
        pass
        # self.feature_scanner.go_in_direction()

    def bind_to_nearby_feature(self) -> None:  # в случае ошибки при сильном смещении
        pass
        # получить координаты из self.get_val_func
        # делать сканы по кругу и в каждом искать фичу

    def __calc_vectors_to_neighbors(self, surface) -> np.ndarray:
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface.copy())
        neighbor_centers = []
        current_center = None
        for figure in figure_gen:
            if self.feature_recognizer.feature_in_aria(self.feature_scanner.get_scan_aria_center(surface), figure):
                current_center = self.feature_recognizer.get_center(figure)
                continue
            neighbor_centers.append(self.feature_recognizer.get_center(figure))
        if current_center is None:
            raise RuntimeError('center not found')
        if len(neighbor_centers) == 0:
            raise RuntimeError('neighbor not found')
        vectors = np.array([[0, 0]], dtype='int8')
        for neighbor_center in neighbor_centers:
            vectors = np.append(vectors, [
                [
                    neighbor_center[0] - current_center[0],
                    neighbor_center[1] - current_center[1]
                ]
            ], axis=0)
        return np.delete(vectors, 0, 0)

    def __calc_vectors_angle(self, v1: np.ndarray, v2: np.ndarray) -> float:
        dot_pr = v1.dot(v2)
        norms = np.linalg.norm(v1) * np.linalg.norm(v2)

        return np.arccos(dot_pr / norms)

    def find_close_vector(self, vectors_to_neighbors: np.ndarray, next_direction: np.ndarray) -> np.ndarray:
        for vector in vectors_to_neighbors:
            angle = self.__calc_vectors_angle(next_direction, vector)
