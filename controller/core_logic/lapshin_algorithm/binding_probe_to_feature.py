from threading import Event
from typing import Tuple


class BindingProbeToFeature:
    """
    1. Изображение, заданное в некотором окне, просматривается до тех пор, пока не будет
    встречена точка, имеющая высоту большую z, т. е. первая точка, принадлежащая контуру
    очередной области. Найденная точка становится текущей; (особенность - имеет высоту больше чем общий шум)
    2. Просматривается восемь соседних к текущей точек, образующих цепной код, 42,45 до тех
    пор, пока не будет обнаружена точка, имеющая высоту большую z. Найденная таким об-
    разом точка становится текущей;
    3. Повторяется пункт 2, пока не будет встречена первая точка границы области, т. е. не
    произойдёт замыкания контура области;
    4. Зная координаты контура области, вычисляются (с точностью до долей пиксела) коор-
    динаты центра тяжести области;
    5. Точкам изображения, принадлежащим распознанной области, присваиваются нулевые
    значения высоты, и если счётчики строки и столбца просматриваемого окна не достигли
    максимального значения, то выполняется переход к пункту 1.
    """

    def __init__(self, get_val_func, set_x_func, set_y_func, touching_surface_event: Event, **kwargs):
        self.touching_surface_event = touching_surface_event
        self.set_y_func = set_y_func
        self.set_x_func = set_x_func
        self.get_val_func = get_val_func
        self.delay_between_iterations = 1
        self.stop = True
        self.z_start_feature_height = None
        self.current_absolute_coordinates_feature = None

    def bypass_feature(self, start_point: Tuple[int, int, int]) -> None:
        self.bypass_feature(start_point)

    def bypass_point(self, start_point) -> None:
        x = start_point[0]
        y = start_point[1]
        gen = self.__gen_bypass_point((x, y))

        max_iteration = 20
        for _ in range(max_iteration):
            try:
                x, y = next(gen)
            except StopIteration:
                break
            self.set_x_func(x)
            self.set_y_func(y)

        # todo если найдена новая точка то можно рекурсивно вызвать еще раз

    def __gen_bypass_point(self, point: Tuple[int, int]):
        """
            обход 8-ми точек по кругу от стартовой
        """
        x = point[0]
        y = point[1]
        y += 1
        yield x, y
        x -= 1
        yield x, y
        for _ in range(2):
            y -= 1
            yield x, y
        for _ in range(2):
            x += 1
            yield x, y
        for _ in range(2):
            y += 1
            yield x, y

