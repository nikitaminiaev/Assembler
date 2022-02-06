from unittest import TestCase
from unittest.mock import Mock

from controller.constants import *
from controller.core_logic.atom_logic import AtomsLogic
from controller.core_logic.exceptions.touching_surface import TouchingSurface


class TestValidateCoordinate(TestCase):

    def test_z_touch_surface_with_scan_mode(self):
        server_mock = Mock()
        attrs = {'type_object': 'Server', 'external_handle_func': ''}
        server_mock.configure_mock(**attrs)
        atom_ligic = AtomsLogic(10, 10, server_mock)
        atom_ligic.set_is_it_surface(True)
        with self.assertRaises(TouchingSurface) as e:
            atom_ligic.set_val_to_dto(DTO_Z, (1, 3, - 1))
        assert "touching the surface" in str(e.exception)
        assert atom_ligic.tool_is_coming_down()
