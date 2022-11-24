import unittest
from unittest import TestCase
from unittest.mock import Mock, MagicMock
import json
from controller.constants import *
from controller.core_logic.atom_logic import AtomsLogic, INVALID_DTO
from controller.core_logic.dto import Dto
from controller.core_logic.exceptions.touching_surface import TouchingSurface


class TestSetAndValidateCoordinate(TestCase):
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
        atom_logic.set_is_surface(True)
        assert atom_logic.is_scan_mode()
        assert atom_logic.is_surface()
        z = 70
        with self.assertRaises(TouchingSurface) as e:
            atom_logic.set_val_to_dto(DTO_Z, (1, 3, z))
        self.assertEqual("touching the surface", str(e.exception))
        assert atom_logic.tool_is_coming_down()
        self.assertNotEqual(atom_logic.get_dto_val(DTO_Z), z)

    def test_z_touch_surface_without_scan_mode(self):
        atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        atom_logic.set_is_surface(False)
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
        atom_logic.set_is_surface(False)
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
        atom_logic.set_is_surface(False)
        atom_logic.surface_data[3, 1] = 71
        z = 70
        atom_logic.set_val_to_dto(DTO_Z, (1, 3, z))
        assert atom_logic.tool_is_coming_down()
        self.assertEqual(z - CORRECTION_Z, atom_logic.surface_data[3, 1])
        self.assertEqual(z, atom_logic.get_dto_val(DTO_Z))

    def test_x_touch_side_surface_with_scan_mode(self):
        atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        atom_logic.set_is_surface(False)
        atom_logic.server.send_data_to_all_clients = MagicMock()
        assert atom_logic.is_scan_mode()
        assert not atom_logic.is_surface()
        x = 1
        y = 3
        z = 40
        atom_logic.surface_data[y, x] = 50
        atom_logic.set_val_to_dto(DTO_Z, (0, 0, z))

        atom_logic.update_tool_coordinate()
        tool_x, tool_y, tool_z = atom_logic.get_tool_coordinate()
        self.assertNotEqual(x, tool_x)
        self.assertEqual(z, tool_z)
        self.assertNotEqual(y, tool_y)
        atom_logic.server. \
            send_data_to_all_clients. \
            assert_called_with(f'{{"sensor": "servo_z", "value": "{z}", "auto": 0}}')

        atom_logic.set_val_to_dto(DTO_Y, (0, y, z))
        assert not atom_logic.tool_is_coming_down()

        with self.assertRaises(TouchingSurface) as e:
            atom_logic.set_val_to_dto(DTO_X, (x, y, z))
        self.assertEqual("touching the surface", str(e.exception))
        assert not atom_logic.tool_is_coming_down()
        self.assertNotEqual(atom_logic.get_dto_val(DTO_X), x)

        atom_logic.update_tool_coordinate()
        tool_x, tool_y, tool_z = atom_logic.get_tool_coordinate()
        self.assertNotEqual(x, tool_x)
        self.assertEqual(z, tool_z)
        self.assertEqual(y, tool_y)
        dict = atom_logic.dto_y.to_dict()
        dict['auto'] = 0
        atom_logic.server. \
            send_data_to_all_clients. \
            assert_called_with(json.dumps(dict))


if __name__ == '__main__':
    unittest.main()
