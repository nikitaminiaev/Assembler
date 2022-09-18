import unittest
from typing import Tuple
from unittest.mock import Mock, MagicMock

from controller.constants import MAX, DTO_Z, DTO_X, DTO_Y
from controller.core_logic.atom_logic import AtomsLogic
from controller.core_logic.dto import Dto
from controller.core_logic.exceptions.touching_surface import TouchingSurface
from controller.core_logic.scan_algorithms import ScanAlgorithms
from controller.frontend.manipulator import ConstructorFrames
from tests.scan_algorithm.fixture_scan_algo import INITIAL_DATA, X_DATA_WITHOUT_SURFACE, \
    Y_DATA_WITHOUT_SURFACE, Z_DATA_WITHOUT_SURFACE, X_DATA_WITH_SURFACE, Y_DATA_WITH_SURFACE, Z_DATA_WITH_SURFACE


class FakeConstructorFrames(ConstructorFrames):

    def __init__(self, atoms_logic):
        self.scanAlgorithm = ScanAlgorithms(0)
        self.tk = Mock()
        self.tk.graph.frame.atoms_logic = atoms_logic


class FakeDto(Dto):
    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name
        self._Dto__value: int = 0
        self.mock_value = MagicMock()

    def set_val(self, coordinates: Tuple[int, ...]) -> None:
        self._Dto__value = int(coordinates[Dto.COORDINATE_ORDER[self.sensor_name]])
        self.mock_value(coordinates)

    def validate_val(self, coordinates: tuple) -> None:
        pass


class FakeAtomsLogic(AtomsLogic):
    def set_val_to_dto(self, dto_str: str, coordinates: Tuple[int, int, int]) -> None:
        if dto_str == DTO_Z and coordinates[2] == 20:
            raise TouchingSurface()
        if dto_str == DTO_X and coordinates[0] == 4 and coordinates[2] == 30:
            raise TouchingSurface()
        if dto_str == DTO_Y and coordinates[0] == 4 and coordinates[2] == 30:
            raise TouchingSurface()
        super().set_val_to_dto(dto_str, coordinates)


class TestScanAlgorithm(unittest.TestCase):

    def setUp(self) -> None:
        self.server_mock = Mock()
        attrs = {
            'type_object': 'Server',
            'external_handle_func': '',
        }
        self.server_mock.configure_mock(**attrs)

    def tearDown(self) -> None:
        self.server_mock = None

    def test_auto_scan_without_surface(self):
        atoms_logic = self.__get_atoms_logic(AtomsLogic, 10, 10, MAX)

        fake_constructor_frames = FakeConstructorFrames(atoms_logic)
        fake_constructor_frames.scanAlgorithm.stop = False
        fake_constructor_frames._go_auto(*INITIAL_DATA)

        atoms_logic.dto_x.mock_value.assert_has_calls(X_DATA_WITHOUT_SURFACE, any_order=False)
        atoms_logic.dto_y.mock_value.assert_has_calls(Y_DATA_WITHOUT_SURFACE, any_order=False)
        atoms_logic.dto_z.mock_value.assert_has_calls(Z_DATA_WITHOUT_SURFACE, any_order=False)

    def test_auto_scan_with_surface(self):
        atoms_logic = self.__get_atoms_logic(FakeAtomsLogic, 10, 10, MAX)

        fake_constructor_frames = FakeConstructorFrames(atoms_logic)
        fake_constructor_frames.scanAlgorithm.stop = False
        fake_constructor_frames._go_auto(*INITIAL_DATA)

        atoms_logic.dto_x.mock_value.assert_has_calls(X_DATA_WITH_SURFACE, any_order=False)
        atoms_logic.dto_y.mock_value.assert_has_calls(Y_DATA_WITH_SURFACE, any_order=False)
        atoms_logic.dto_z.mock_value.assert_has_calls(Z_DATA_WITH_SURFACE, any_order=False)

    def __get_atoms_logic(self, atoms_logic_class, x_max, y_max, z_max):
        atoms_logic = atoms_logic_class(x_max, y_max, self.server_mock)

        atoms_logic.dto_x = FakeDto(Dto.SERVO_X)
        atoms_logic.dto_y = FakeDto(Dto.SERVO_Y)
        atoms_logic.dto_z = FakeDto(Dto.SERVO_Z)
        atoms_logic.dto_z.set_val((0, 0, z_max))
        return atoms_logic


if __name__ == '__main__':
    unittest.main()
