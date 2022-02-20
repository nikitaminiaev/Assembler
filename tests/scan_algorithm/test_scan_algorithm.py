import unittest
from unittest.mock import Mock, MagicMock

from controller.constants import MAX
from controller.core_logic.atom_logic import AtomsLogic
from controller.core_logic.scan_algorithms import ScanAlgorithms
from controller.manipulator import ConstructorFrames
from tests.scan_algorithm.data_fore_test import X_DATA, Y_DATA, Z_DATA


class FakeConstructorFrames(ConstructorFrames):

    def __init__(self, atoms_logic):
        self.scanAlgorithm = ScanAlgorithms(0)
        self.tk = Mock()
        self.tk.graph.frame.atoms_logic = atoms_logic


class testScanAlgorithm(unittest.TestCase):

    def setUp(self) -> None:
        self.server_mock = Mock()
        attrs = {
            'type_object': 'Server',
            'external_handle_func': '',
        }
        self.server_mock.configure_mock(**attrs)

    def tearDown(self) -> None:
        self.server_mock = None

    def test_auto_scan(self):
        atoms_logic = self.__get_atoms_logic(10, 10, MAX)

        fake_constructor_frames = FakeConstructorFrames(atoms_logic)
        fake_constructor_frames.scanAlgorithm.stop = False
        fake_constructor_frames._go_auto(1, 1, 5, 5)

        atoms_logic.dto_x.set_val.assert_has_calls(X_DATA, any_order=False)
        atoms_logic.dto_y.set_val.assert_has_calls(Y_DATA, any_order=False)
        atoms_logic.dto_z.set_val.assert_has_calls(Z_DATA, any_order=False)

    def __get_atoms_logic(self, x_max, y_max, z_max):
        atoms_logic = AtomsLogic(x_max, y_max, self.server_mock)

        def set_val(dto_obj, val): dto_obj.value = val

        atoms_logic.dto_x = Mock()
        setattr(atoms_logic.dto_x, 'value', 0)
        atoms_logic.dto_x.set_val = MagicMock(return_value=set_val)
        atoms_logic.dto_x.get_val = MagicMock(return_value=atoms_logic.dto_x.value)
        atoms_logic.dto_y = Mock()
        setattr(atoms_logic.dto_y, 'value', 0)
        atoms_logic.dto_y.set_val = MagicMock(return_value=set_val)
        atoms_logic.dto_y.get_val = MagicMock(return_value=atoms_logic.dto_y.value)
        atoms_logic.dto_z = Mock()
        setattr(atoms_logic.dto_z, 'value', z_max)
        atoms_logic.dto_z.set_val = MagicMock(return_value=set_val)
        atoms_logic.dto_z.get_val = MagicMock(return_value=atoms_logic.dto_z.value)
        return atoms_logic


if __name__ == '__main__':
    unittest.main()
