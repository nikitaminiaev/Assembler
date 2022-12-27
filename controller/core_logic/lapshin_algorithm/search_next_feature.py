"""
при создании затравки производится поиск такого атома, который расположен под
наименьшим углом к прямой, задающей направление движения. Найденный атом полу-
чает ярлык “следующий”. Причём, при перемещении вдоль кристаллографического на-
правления положение следующего атома цепочки используется для уточнения направле-
ния движения, если изменение локальной кривизны цепочки лежит в заданных пределах.
Таким образом, указанный приём позволяет удерживать выбранное направление, легко
минуя те места на поверхности кристалла, где расположены точечные дефекты решётки.
"""

"""
В случае, когда выполняется обход затравки с присоединением (см. Рис. 5 и Рис. 8),
вначале выполняется сортировка: среди атомов выбираются те, что не принадлежат к
уже пройденной цепочке. После чего среди отобранных ищется тот, что расположен под
наибольшим (наименьшим) углом (отсчёт угла в обоих случаях производится вокруг “те-
кущего” атома в направлении против часовой стрелки) к отрезку, соединяющему “теку-
щий” и “предыдущий” атомы при обходе контура цепочки против часовой стрелки (по ча-
совой стрелке). Найденный таким образом атом принимается за “следующий” атом це-
почки.
"""

"""
Надо искать следующий атом цепочки по предположительному направлению движения. Найдя распознать его определить, 
привязаться, определить относительные координаты к предыдущему и перепрыгивать между ними для усреднения.  
"""