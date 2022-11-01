class Origin:

    def __init__(self):
        self.__coordinate = {'x': 0, 'y': 0, 'z': 0}

    def get_coordinate(self) -> tuple:
        return self.__coordinate['x'], self.__coordinate['y'], self.__coordinate['z']

    def set_coordinate(self, x: int, y: int, z: int) -> None:
        self.__coordinate['x'] = x
        self.__coordinate['y'] = y
        self.__coordinate['z'] = z

    def get_x(self) -> int:
        return self.__coordinate['x']

    def get_y(self) -> int:
        return self.__coordinate['y']

    def get_z(self) -> int:
        return self.__coordinate['z']

    def set_x(self, x: int) -> None:
        self.__coordinate['x'] = x

    def set_y(self, y: int) -> None:
        self.__coordinate['y'] = y

    def set_z(self, z: int) -> None:
        self.__coordinate['z'] = z
