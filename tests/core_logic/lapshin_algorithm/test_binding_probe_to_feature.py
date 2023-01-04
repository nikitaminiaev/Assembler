import sys, os
root = sys.path[1]
path = os.path.join(root, "stub_microcontroller")
if path not in sys.path:
    sys.path.insert(0, path)
    sys.path.insert(0, os.path.abspath("../../../stub_microcontroller"))

from controller.core_logic.service.feature_scanner import FeatureScanner
from unittest import TestCase
from controller.core_logic.lapshin_algorithm.entity.atom import Atom
from controller.core_logic.lapshin_algorithm.service.recognition.lapshin_feature_recognizer import LapshinFeatureRecognizer
from unittest.mock import MagicMock
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
from stub_microcontroller.surface_generator import SurfaceGenerator


class TestBindingProbeToFeature(TestCase):

    def setUp(self) -> None:
        get_val_func = MagicMock()
        set_x_func = MagicMock()
        set_y_func = MagicMock()
        touching_surface_event = MagicMock()
        external_surface = MagicMock()
        push_coord_to_mk = MagicMock()
        scanner = FeatureScanner(get_val_func, set_x_func, set_y_func, touching_surface_event, external_surface, push_coord_to_mk, 0)

        self.binding_probe_to_feature = BindingProbeToFeature(
            LapshinFeatureRecognizer(),
            scanner
        )

    def test_bind_to_feature(self) -> None:
        surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        self.binding_probe_to_feature.feature_scanner.external_surface = surface
        feature = Atom((9, 9, 20))
        self.assertEqual(0, feature.perimeter_len)

        self.binding_probe_to_feature.return_to_feature(feature)

        height = self.binding_probe_to_feature.feature_recognizer.get_max_height(surface)
        self.assertNotEqual(0, feature.perimeter_len)
        self.assertEqual((10, 10, height), feature.coordinates)
        self.binding_probe_to_feature.feature_scanner.set_x_func.assert_called_with((feature.coordinates[0], feature.coordinates[1], feature.coordinates[2] + 3))
        self.binding_probe_to_feature.feature_scanner.set_y_func.assert_called_with((feature.coordinates[0], feature.coordinates[1], feature.coordinates[2] + 3))

    def test_feature_not_found(self) -> None:
        surface = SurfaceGenerator(20, 20, []).generate()
        self.binding_probe_to_feature.feature_scanner.external_surface = surface
        feature = Atom((9, 9, 20))

        self.assertRaises(RuntimeError, self.binding_probe_to_feature.return_to_feature, feature)


    # todo def test_bind_to_feature_with_noise(self) -> None:
    #     self.BindingProbeToFeature.global_surface = SurfaceGenerator(20, 20, [(10, 10)]).generate_noise_surface()
    #     feature = Atom((9, 9, 20), 3)
    #
    #     self.BindingProbeToFeature.bind_to_feature(feature)
    #
    #     print(self.BindingProbeToFeature.x_correction)
    #     print(self.BindingProbeToFeature.y_correction)
