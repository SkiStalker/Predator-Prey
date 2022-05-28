import random
import typing

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget

from src.Essenses.SimulatingCell import SimulatingCell
from src.Essenses.WaterCell import WaterCell


class AnimalCell(SimulatingCell):
    def __init__(self, tp: SimulatingCell.TYPE, position: QPoint, parent=None):
        super().__init__(tp, position, parent)
        self.__define_const()
        self._hunger = self._INIT_HUNGER
        self._thirst = self._INIT_THIRST
        self._ate = False
        self._reproduced = False
        self._crossed = 0
        self._speed = 0
        self.setZValue(1)
        self._cur_eat = SimulatingCell()
        self._cur_water = SimulatingCell()

    def __define_const(self):
        self._INIT_HUNGER = 30
        self._INIT_THIRST = 30
        self._REPRODUCTION_COUNT = 15
        self._REPRODUCTION_EXPENSES = 4
        self._SATIETY_VALUE = 5
        self._DRINKING_VALUE = 5
        self._FOX_SPEED = 1000
        self._HARE_SPEED = 600

    @property
    def hunger(self):
        return self._hunger

    @property
    def thirst(self):
        return self._thirst

    def print_scene_pos(self):
        print(self.scene_pos.x(), self.scene_pos.y())

    def is_dead(self):
        return self._hunger == 0 or self._thirst == 0

    def is_reproduced(self):
        return self._reproduced

    def _step(self):
        self._thirst -= 1
        self._hunger -= 1

    def reproduce(self):
        self._reproduced = False

    def is_ate(self):
        return self._ate

    def paint(self, painter: QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        pass

    def _move_scene_pos(self, dx: int, dy: int):
        if not (0 <= self.scene_pos.x() + dx < 560 // 20):
            raise ValueError("Incorrect dx")

        if not (0 <= self.scene_pos.y() + dy < 560 // 20):
            raise ValueError("Incorrect dy")

        self.scene_pos = QPoint(self.scene_pos.x() + dx,
                                self.scene_pos.y() + dy)

    def _move(self) -> bool:
        self._crossed += self._speed
        if self._crossed >= 1000:
            self._crossed -= 1000
            return True
        return False

    def _move_to(self, cell: SimulatingCell):
        offset: QPoint = self.scene_pos - cell.scene_pos
        if self._move():
            dx, dy = 0, 0
            if offset.x() != 0:
                dx = -(offset.x() // abs(offset.x()))
            if offset.y() != 0:
                dy = -(offset.y() // abs(offset.y()))

            self._move_scene_pos(dx, dy)

    def _random_move(self):
        if self._move():
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            try:
                self._move_scene_pos(dx, 0)
            except ValueError:
                self._move_scene_pos(-dx, 0)
            try:
                self._move_scene_pos(0, dy)
            except ValueError:
                self._move_scene_pos(0, -dy)

    def _find_water(self, water: typing.List[WaterCell]):
        for cur_water in water:
            dist = SimulatingCell.calc_distance(self.scene_pos, cur_water.scene_pos)
            if dist <= 3:
                self._cur_water = cur_water

    def _find_eat(self, eat: typing.List[SimulatingCell]):
        for cur_eat in eat:
            dist = SimulatingCell.calc_distance(self.scene_pos, cur_eat.scene_pos)
            if dist <= 3:
                self._cur_eat = cur_eat

    def _find_eat_or_water(self, water: typing.List[WaterCell], eat: typing.List[SimulatingCell]):
        priority = self._thirst < self._hunger
        if priority and not self._cur_water.is_defined():
            self._find_water(water)
        elif not self._cur_water.is_defined() \
                and not self._cur_eat.is_defined():
            self._find_eat(eat)

    def _move_to_target(self):
        if self._cur_water.is_defined():
            self._move_to(self._cur_water)
            if self.scene_pos == self._cur_water.scene_pos:
                self._thirst += self._DRINKING_VALUE
                self._cur_water = SimulatingCell()

        elif self._cur_eat.is_defined():
            if not self._cur_eat.is_alive():
                self._cur_eat = SimulatingCell()
            else:
                self._move_to(self._cur_eat)
                if self.scene_pos == self._cur_eat.scene_pos:
                    self._hunger += self._SATIETY_VALUE
                    if self._hunger > self._REPRODUCTION_COUNT:
                        self._reproduced = True
                        self._hunger -= self._REPRODUCTION_EXPENSES
                    self._ate = True
        else:
            self._random_move()

    def think(self, eat: typing.List[SimulatingCell], water: typing.List[WaterCell]):
        self._step()

        if self.is_dead():
            self.die()
            return

        self._find_eat_or_water(water, eat)

        self._move_to_target()

    def eat(self):
        self._cur_eat.die()
        self._cur_eat = SimulatingCell()

    def eaten_object(self):
        self._ate = False
        return self._cur_eat

    def get_target_type(self) -> SimulatingCell.TYPE:
        return SimulatingCell.TYPE.Nothing
