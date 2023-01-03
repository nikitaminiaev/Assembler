from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
from controller.core_logic.lapshin_algorithm.feature_searcher import FeatureSearcher
from controller.core_logic.lapshin_algorithm.service.recognition.lapshin_feature_recognizer import \
    LapshinFeatureRecognizer
from controller.core_logic.service.scanner_interface import ScannerInterface


class Factory:

    @staticmethod
    def create_lapshin_feature_searcher(feature_scanner: ScannerInterface) -> FeatureSearcher:
        feature_scanner.switch_scan(False)
        binding_feature = BindingProbeToFeature(
            LapshinFeatureRecognizer(),
            feature_scanner
        )

        return FeatureSearcher(
            binding_feature,
            feature_scanner,
            LapshinFeatureRecognizer()
        )