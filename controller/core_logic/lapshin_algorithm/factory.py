from threading import Event
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
from controller.core_logic.lapshin_algorithm.feature_searcher import FeatureSearcher
from controller.core_logic.lapshin_algorithm.service.recognition.lapshin_feature_recognizer import \
    LapshinFeatureRecognizer
from controller.core_logic.service.scanner_interface import ScannerInterface


class Factory:

    @staticmethod
    def create_lapshin_feature_searcher(scanner: ScannerInterface) -> FeatureSearcher:
        binding_in_delay = Event()
        allow_binding = Event()
        binding_feature = BindingProbeToFeature(
            LapshinFeatureRecognizer(),
            scanner,
            binding_in_delay,
            allow_binding
        )

        return FeatureSearcher(
            binding_feature,
            scanner,
            LapshinFeatureRecognizer(),
            binding_in_delay,
            allow_binding
        )