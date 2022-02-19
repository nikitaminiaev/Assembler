import unittest
from unittest.mock import Mock, MagicMock

from controller.core_logic.atom_logic import AtomsLogic
from controller.core_logic.scan_algorithms import ScanAlgorithms
from controller.manipulator import ConstructorFrames


class FakeConstructorFrames(ConstructorFrames):

    def __init__(self, atoms_logic, scan_vars):
        self.scanAlgorithm = ScanAlgorithms(0)
        self.tk = Mock()
        self.tk.graph.frame.atoms_logic = atoms_logic
        self._ConstructorFrames__scan_vars = scan_vars


class testScanAlgorithm(unittest.TestCase):

    def setUp(self) -> None:
        server_mock = Mock()
        attrs = {
            'type_object': 'Server',
            'external_handle_func': '',
        }
        server_mock.configure_mock(**attrs)
        atoms_logic = AtomsLogic(10, 10, server_mock)

        data = ['1', '1', '5', '5']
        scan_vars = Mock()
        get = Mock()
        get.split = MagicMock(return_value=data)
        scan_vars.get = MagicMock(return_value=get)

        self.fake_constructor_frames = FakeConstructorFrames(atoms_logic, scan_vars)

    def tearDown(self) -> None:
        self.fake_constructor_frames = None

    def test_auto_scan(self):
        self.fake_constructor_frames.auto()


if __name__ == '__main__':
    unittest.main()
