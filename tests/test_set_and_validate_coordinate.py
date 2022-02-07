import unittest
from unittest import TestCase
from unittest.mock import Mock

from controller.constants import *
from controller.core_logic.atom_logic import AtomsLogic, INVALID_DTO
from controller.core_logic.dto import Dto
from controller.core_logic.exceptions.touching_surface import TouchingSurface


class TestSetAndValidateCoordinate(TestCase):
    server_mock = None

    @classmethod
    def setUpClass(cls):
        cls.server_mock = Mock()
        attrs = {'type_object': 'Server', 'external_handle_func': ''}
        cls.server_mock.configure_mock(**attrs)

    @classmethod
    def tearDownClass(cls):
        cls.server_mock = None

    def test_invalid_dto(self):
        atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        with self.assertRaises(ValueError) as e:
            atom_logic.set_val_to_dto("iny_dto", (1, 3, 1))
        self.assertEqual(INVALID_DTO, str(e.exception))
        with self.assertRaises(ValueError) as e:
            atom_logic.get_dto_val("iny_dto")
        self.assertEqual(INVALID_DTO, str(e.exception))

    def test_z_touch_surface_with_scan_mode(self):
        atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        atom_logic.set_is_it_surface(True)
        assert atom_logic.is_scan_mode()
        z = 70
        with self.assertRaises(TouchingSurface) as e:
            atom_logic.set_val_to_dto(DTO_Z, (1, 3, z))
        self.assertEqual("touching the surface", str(e.exception))
        assert atom_logic.tool_is_coming_down()
        self.assertNotEqual(atom_logic.get_dto_val(DTO_Z), z)

    def test_z_touch_surface_without_scan_mode(self):
        atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        atom_logic.set_is_it_surface(False)
        atom_logic.set_scan_mode(False)
        atom_logic.surface_data[3, 1] = 71
        z = 70
        with self.assertRaises(TouchingSurface) as e:
            atom_logic.set_val_to_dto(DTO_Z, (1, 3, z))
        self.assertEqual("touching the surface", str(e.exception))
        assert atom_logic.tool_is_coming_down()
        self.assertNotEqual(atom_logic.get_dto_val(DTO_Z), z)

    def test_z_not_touch_surface_with_scan_mode(self, ):
        atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        atom_logic.set_is_it_surface(False)
        z = 70
        set_z_func = atom_logic.set_val_dto_curried(DTO_Z)
        set_z_func((1, 3, z))
        assert atom_logic.tool_is_coming_down()
        self.assertNotEqual(z - CORRECTION_Z, atom_logic.surface_data[3, 1])
        self.assertEqual(z, atom_logic.get_dto_val(DTO_Z))
        self.assertEqual(
            {Dto.SENSOR: Dto.SERVO_Z, 'value': str(z)},
            atom_logic.dto_z.to_dict()
        )

    def test_update_surface_with_scan_mode(self):
        atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        atom_logic.set_is_it_surface(False)
        atom_logic.surface_data[3, 1] = 71
        z = 70
        atom_logic.set_val_to_dto(DTO_Z, (1, 3, z))
        assert atom_logic.tool_is_coming_down()
        self.assertEqual(z - CORRECTION_Z, atom_logic.surface_data[3, 1])
        self.assertEqual(z, atom_logic.get_dto_val(DTO_Z))


if __name__ == '__main__':
    unittest.main()
