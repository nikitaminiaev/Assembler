from threading import Event
from typing import Tuple

from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
from controller.core_logic.lapshin_algorithm.feature_collection.doubly_linked_list import DoublyLinkedList, \
    StructureOfFeatureInterface
from controller.core_logic.lapshin_algorithm.feature_searcher import FeatureSearcher
from controller.core_logic.lapshin_algorithm.feature_searcher_interface import FeatureSearcherInterface
from controller.core_logic.lapshin_algorithm.service.recognition.lapshin_feature_recognizer import \
    LapshinFeatureRecognizer
from controller.core_logic.lapshin_algorithm.walker_by_features import WalkerByFeaturesInterface, WalkerByFeatures
from controller.core_logic.service.scanner_interface import ScannerInterface


class Factory:

    @staticmethod
    def create_lapshin_algorithm(scanner: ScannerInterface) -> Tuple[FeatureSearcherInterface, WalkerByFeaturesInterface, StructureOfFeatureInterface]:
        binding_in_delay = Event()
        allow_binding = Event()
        binding_feature = BindingProbeToFeature(
            LapshinFeatureRecognizer(),
            scanner,
            binding_in_delay,
            allow_binding,
        )

        structure_of_feature = DoublyLinkedList()

        return FeatureSearcher(
            binding_feature,
            scanner,
            LapshinFeatureRecognizer(),
            structure_of_feature,
            binding_in_delay,
            allow_binding,
        ), WalkerByFeatures(
            structure_of_feature,
            scanner,
            binding_feature,
            binding_in_delay,
            allow_binding,
        ), structure_of_feature
