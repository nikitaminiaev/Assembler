import threading

from controller.core_logic.lapshin_algorithm.binding_probe_to_feature_interface import BindingProbeToFeatureInterface
from controller.core_logic.lapshin_algorithm.feature_collection.doubly_linked_list import DoublyLinkedList
from controller.core_logic.lapshin_algorithm.service.recognition.feature_recognizer_interface import \
    FeatureRecognizerInterface
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

    def __init__(self, binding_to_feature: BindingProbeToFeatureInterface, feature_scanner: ScannerInterface, feature_recognizer: FeatureRecognizerInterface):
        self.feature_scanner = feature_scanner
        self.local_surface = None
        self.binding_to_feature = binding_to_feature
        self.feature_recognizer = feature_recognizer
        self.structure_of_feature = DoublyLinkedList()

    def find_first_feature(self):
        surface = self.feature_scanner.scan_aria()
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface)
        figure = next(figure_gen)
        feature = self.feature_recognizer.recognize_feature(figure, surface) #todo передавать сьюда surface ограниченную областью фичи
        self.structure_of_feature.insert_to_end(feature)
        threading.Thread(target=self.binding_to_feature.bind_to_feature, args=(feature,)).start()
        self.structure_of_feature.display()

    def find_next_feature(self):
        pass
        # self.feature_scanner.go_in_direction()

    def bind_to_nearby_feature(self) -> None:
        pass
        # получить координаты из self.get_val_func
        # делать сканы по кругу и в каждом искать фичу


