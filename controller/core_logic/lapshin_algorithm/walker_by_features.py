from abc import ABC, abstractmethod
from threading import Event

from controller.core_logic.lapshin_algorithm.binding_probe_to_feature_interface import BindingProbeToFeatureInterface
from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.feature_collection.doubly_linked_list import DoublyLinkedList
from controller.core_logic.service.scanner_interface import ScannerInterface


class WalkerByFeaturesInterface(ABC):

    @abstractmethod
    def go_to_next_feature(self) -> Feature or None:
        pass

    @abstractmethod
    def go_to_prev_feature(self) -> Feature or None:
        pass


class WalkerByFeatures(WalkerByFeaturesInterface):

    def __init__(self,
                 structure_of_feature: DoublyLinkedList,
                 scanner: ScannerInterface,
                 binding_to_feature: BindingProbeToFeatureInterface,
                 binding_in_delay: Event,
                 allow_binding: Event,
                 ):
        self.structure_of_feature = structure_of_feature
        self.scanner = scanner
        self.binding_to_feature = binding_to_feature
        self.binding_in_delay = binding_in_delay
        self.allow_binding = allow_binding

    def go_to_next_feature(self) -> Feature or None:
        if not self.structure_of_feature.is_set_next_feature():
            return None
        self.binding_in_delay.wait()
        self.allow_binding.clear()
        current_feature: Feature = self.structure_of_feature.get_current_feature()
        next_feature = self.structure_of_feature.pointer_to_next_feature()
        self.binding_to_feature.set_current_feature(next_feature)
        self.scanner.go_to_direction(current_feature.vector_to_next)
        self.allow_binding.set()
        return next_feature

    def go_to_prev_feature(self) -> Feature or None:
        if not self.structure_of_feature.is_set_prev_feature():
            return None
        self.binding_in_delay.wait()
        self.allow_binding.clear()
        current_feature: Feature = self.structure_of_feature.get_current_feature()
        prev_feature = self.structure_of_feature.pointer_to_prev_feature()
        self.binding_to_feature.set_current_feature(prev_feature)
        self.scanner.go_to_direction(current_feature.vector_to_prev)
        self.allow_binding.set()
        return prev_feature
