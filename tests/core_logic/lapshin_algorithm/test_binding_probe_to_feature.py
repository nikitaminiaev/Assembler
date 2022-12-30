import sys, os

path = os.path.abspath("../../../stub_microcontroller")
if path not in sys.path:
    sys.path.insert(0, path)

from unittest import TestCase
from controller.core_logic.entity.atom import Atom
from controller.core_logic.lapshin_algorithm.recognition.lapshin_feature_recognizer import LapshinFeatureRecognizer
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

        self.binding_probe_to_feature = BindingProbeToFeature(
            LapshinFeatureRecognizer(),
            get_val_func,
            set_x_func,
            set_y_func,
            touching_surface_event,
            external_surface
        )

    def test_calc_optimal_height(self) -> None:
        arr = SurfaceGenerator(20, 20, [(5, 5), (10, 5), (15, 5), (5, 10), (10, 10), (15, 10)]).generate_noise_surface()

        self.binding_probe_to_feature.calc_optimal_height(arr)

        self.assertEqual(21, self.binding_probe_to_feature.optimal_height)

    def test_bind_to_feature(self) -> None:
        surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        self.binding_probe_to_feature.external_surface = surface
        feature = Atom((9, 9, 20))
        self.assertEqual(0, feature.perimeter_len)

        self.binding_probe_to_feature.bind_to_feature(feature)

        self.assertNotEqual(0, feature.perimeter_len)
        self.assertEqual((10, 10, self.binding_probe_to_feature.optimal_height), feature.coordinates)

    def test_feature_not_found(self) -> None:
        surface = SurfaceGenerator(20, 20, []).generate()
        self.binding_probe_to_feature.external_surface = surface
        feature = Atom((9, 9, 20))

        self.assertRaises(RuntimeError, self.binding_probe_to_feature.bind_to_feature, feature)


    # todo def test_bind_to_feature_with_noise(self) -> None:
    #     self.BindingProbeToFeature.global_surface = SurfaceGenerator(20, 20, [(10, 10)]).generate_noise_surface()
    #     feature = Atom((9, 9, 20), 3)
    #
    #     self.BindingProbeToFeature.bind_to_feature(feature)
    #
    #     print(self.BindingProbeToFeature.x_correction)
    #     print(self.BindingProbeToFeature.y_correction)
