import unittest
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from controller.constants import *
from controller.core_logic.atom_logic import AtomsLogic


class TestAtomCollection(TestCase):
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

    def setUp(self) -> None:
        self.atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        self.atom_logic.set_is_surface(False)
        self.atom_logic.server.send_data_to_all_clients = MagicMock()
        assert self.atom_logic.is_scan_mode()
        assert not self.atom_logic.is_surface()
        self.atom_logic.set_is_atom(True)
        atom_coord = (1, 3, 40)
        self.atom_logic.set_val_to_dto(DTO_X, atom_coord)
        self.atom_logic.set_val_to_dto(DTO_Y, atom_coord)
        self.atom_logic.set_val_to_dto(DTO_Z, atom_coord)
        self.atom_logic.update_tool_coordinate()

    def tearDown(self) -> None:
        self.atom_logic = None

    def test_append_unique_atom(self):
        self.assertEqual(0, len(self.atom_logic.atom_collection.atoms_list))

        is_append = self.atom_logic.atom_collection.append_unique_atom()
        self.assertTrue(is_append)
        self.assertEqual(1, len(self.atom_logic.atom_collection.atoms_list))

        is_append = self.atom_logic.atom_collection.append_unique_atom()
        self.assertFalse(is_append)
        self.assertEqual(1, len(self.atom_logic.atom_collection.atoms_list))

    def test_set_atom_captured(self):
        self.assertEqual(0, len(self.atom_logic.atom_collection.atoms_list))

        is_append = self.atom_logic.atom_collection.append_unique_atom()
        self.assertTrue(is_append)
        self.assertEqual(1, len(self.atom_logic.atom_collection.atoms_list))
        x, y, z = self.atom_logic.get_tool_coordinate()

        self.atom_logic.set_is_atom_captured(True)
        self.assertTrue(self.atom_logic.atom_captured_event)
        atom = self.atom_logic.atom_collection.atoms_list[0]
        self.assertTrue(atom.is_captured)
        self.assertTrue(self.atom_logic.is_atom_captured())
        self.assertEqual(atom.coordinates, (x, y, z))

        self.atom_logic.set_is_atom_captured(False)
        self.assertTrue(self.atom_logic.atom_release_event)
        atom = self.atom_logic.atom_collection.atoms_list[0]
        self.assertFalse(atom.is_captured)
        self.assertFalse(self.atom_logic.is_atom_captured())
        self.assertEqual(atom.coordinates, (x, y, z))

        self.atom_logic.set_val_to_dto(DTO_Z, (x, y, z + 1))
        self.atom_logic.update_tool_coordinate()
        self.atom_logic.set_is_atom_captured(True)
        self.assertTrue(self.atom_logic.atom_captured_event)
        atom = self.atom_logic.atom_collection.atoms_list[0]
        self.assertTrue(atom.is_captured)
        self.assertTrue(self.atom_logic.is_atom_captured())
        self.assertEqual(atom.coordinates, (x, y, z))

        self.atom_logic.set_is_atom_captured(False)
        self.assertTrue(self.atom_logic.atom_release_event)
        atom = self.atom_logic.atom_collection.atoms_list[0]
        self.assertFalse(atom.is_captured)
        self.assertFalse(self.atom_logic.is_atom_captured())
        self.assertEqual(atom.coordinates, (x, y, z + 1))

        self.assertEqual(len(self.atom_logic.atom_collection.atoms_list), 1)


if __name__ == '__main__':
    unittest.main()
