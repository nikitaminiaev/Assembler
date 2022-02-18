import unittest
from unittest import TestCase
from unittest.mock import Mock

from controller.constants import *
from controller.core_logic.atom_logic import AtomsLogic


class TestHandleServerData(TestCase):
    server_mock = None

    @classmethod
    def setUpClass(cls):
        cls.server_mock = Mock()
        attrs = {
            'type_object': 'Server',
            'external_handle_func': '',
        }
        cls.server_mock.configure_mock(**attrs)

    @classmethod
    def tearDownClass(cls):
        cls.server_mock = None

    surface_data = [
        ('{"sensor": "surface", "val": 1}', 'valid'),
        (', "val": 1}{"sensor": "surface", "val": 1}', 'valid'),
        ('al": 1}{"sensor": "surface", "val": 1}{"sensor": "su', 'valid'),
        ('al": 1}{"sensor": "su', 'invalid'),
        ('{"sensor": "surface", "any": 1}', 'invalid'),
    ]

    def test_handle_surface_data(self):
        for data, validated in self.surface_data:
            atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
            z = 70
            self.__set_tool_is_coming_down(atom_logic, z)
            atom_logic.set_is_surface(False)
            if validated == 'valid':
                atom_logic.handle_server_data(data)
                self.assertTrue(atom_logic.is_surface())
                self.assertEqual(z - CORRECTION_Z, atom_logic.surface_data[0, 0])
            else:
                atom_logic.handle_server_data(data)
                self.assertFalse(atom_logic.is_surface())
                self.assertNotEqual(z - CORRECTION_Z, atom_logic.surface_data[0, 0])
            self.assertFalse(atom_logic.is_atom())

    atom_data = [
        ('{"sensor": "atom", "val": 1}', 'valid'),
        (', "val": 1}{"sensor": "atom", "val": 1}', 'valid'),
        ('al": 1}{"sensor": "atom", "val": 1}{"sensor": "su', 'valid'),
        ('al": 1}{"sensor": "at', 'invalid'),
        ('{"sensor": "atom", "any": 1}', 'invalid'),
    ]

    def test_handle_atom_data(self):
        for data, validated in self.atom_data:
            atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
            if validated == 'valid':
                atom_logic.handle_server_data(data)
                self.assertTrue(atom_logic.is_atom())
            else:
                atom_logic.handle_server_data(data)
                self.assertFalse(atom_logic.is_atom())

    def __set_tool_is_coming_down(self, atom_logic, z):
        atom_logic.surface_data[3, 1] = z + 1
        atom_logic.set_val_to_dto(DTO_Z, (1, 3, z))


if __name__ == '__main__':
    unittest.main()
