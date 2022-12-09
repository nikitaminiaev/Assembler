from unittest import TestCase
from unittest.mock import MagicMock, call
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
from stub_microcontroller.surface_generator import SurfaceGenerator


class TestBindingProbeToFeature(TestCase):

    def setUp(self) -> None:
        get_val_func = MagicMock()
        set_x_func = MagicMock()
        set_y_func = MagicMock()
        touching_surface_event = MagicMock()

        self.BindingProbeToFeature = BindingProbeToFeature(
            get_val_func,
            set_x_func,
            set_y_func,
            touching_surface_event,
        )

    def test_bypass_single_point(self) -> None:
        self.BindingProbeToFeature.bypass_feature((3, 3))

        calls = [call(3), call(2), call(2), call(2), call(3), call(4), call(4), call(4)]
        self.BindingProbeToFeature.set_x_func.assert_has_calls(calls)

        calls = [call(4), call(4), call(3), call(2), call(2), call(2), call(3), call(4)]
        self.BindingProbeToFeature.set_y_func.assert_has_calls(calls)

    def test_calc_optimal_height(self) -> None:
        arr = SurfaceGenerator(20, 20, [(5, 5), (10, 5), (15, 5), (5, 10), (10, 10), (15, 10)]).generate_noise_surface()

        self.BindingProbeToFeature.calc_optimal_height(arr)

        self.assertEqual(21, self.BindingProbeToFeature.z_optimal_height)
