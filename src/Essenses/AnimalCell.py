import random
import typing
from enum import IntEnum

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget

from src.Essenses.SimulatingCell import SimulatingCell
from src.Essenses.WaterCell import WaterCell


class AnimalCell(SimulatingCell):
    class _CONSTS(IntEnum):
        FOX_INIT_HUNGER = 30
        FOX_INIT_THIRST = 30

        HARE_INIT_HUNGER = 30
        HARE_INIT_THIRST = 30

        FOX_REPRODUCTION_EXPENSES = 4
        HARE_REPRODUCTION_EXPENSES = 4

        FOX_SATIETY_VALUE = 10
        HARE_SATIETY_VALUE = 10

        DRINKING_VALUE = 5

        FOX_VIEW_RANGE = 4
        HARE_VIEW_RANGE = 3

        FOX_SPEED = 1000
        HARE_SPEED = 600

        HARE_CRITICAL_HUNGER_OR_THIRST = 4

        FOX_WELL_FED = 15
        HARE_WELL_FED = 10

        FOX_REPRODUCE_COUNT = 1
        HARE_REPRODUCE_COUNT = 3

    def __init__(self, tp: SimulatingCell.TYPE, position: QPoint, parent=None):
        super().__init__(tp, position, parent)
        self._hunger = 0
        self._thirst = 0
        self._ate = False
        self._reproduced = False
        self._crossed = 0
        self._speed = 0
        self.setZValue(1)
        self._cur_eat = SimulatingCell()
        self._cur_water = SimulatingCell()
        self._cur_predator = SimulatingCell()

    @property
    def hunger(self):
        return self._hunger

    @property
    def thirst(self):
        return self._thirst

    def _satiety(self):
        pass

    def print_scene_pos(self):
        print(self.scene_pos.x(), self.scene_pos.y())

    def is_dead(self):
        return self._hunger == 0 or self._thirst == 0

    def _is_critical_hunger_or_thirst(self) -> bool:
        return False

    def is_reproduced(self):
        return self._reproduced

    def reproduce_count(self):
        pass

    def _reproduce_expenses(self):
        pass

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

    def _move_to(self, point: QPoint, away: bool = False):
        offset: QPoint = self.scene_pos - point
        sign = -1
        if away:
            sign = 1

        if self._move():
            dx, dy = 0, 0
            if offset.x() != 0:
                dx = sign * (offset.x() // abs(offset.x()))
            if offset.y() != 0:
                dy = sign * (offset.y() // abs(offset.y()))
            try:
                self._move_scene_pos(dx, 0)
            except ValueError as ex:
                print(ex.args)
            try:
                self._move_scene_pos(0, dy)
            except ValueError as ex:
                print(ex.args)

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

    def _find_range(self):
        pass

    def _find_best_object(self, objects: typing.List[SimulatingCell | WaterCell]):
        best_obj = SimulatingCell()
        best_dist = -1
        for cur_obj in objects:
            dist = SimulatingCell.calc_distance(self.scene_pos, cur_obj.scene_pos)
            if dist <= self._find_range():
                if best_obj.is_defined() and best_dist > dist:
                    best_obj = cur_obj
                    best_dist = dist
                else:
                    best_obj = cur_obj
                    best_dist = dist
        return best_obj

    def _find_water(self, water: typing.List[WaterCell]):
        self._cur_water = self._find_best_object(water)

    def _find_eat(self, eat: typing.List[SimulatingCell]):
        self._cur_eat = self._find_best_object(eat)

    def _find_predator(self, predators: typing.List['AnimalCell']):
        pass

    def _find_eat_or_water(self, water: typing.List[WaterCell], eat: typing.List[SimulatingCell]):
        priority = self._thirst < self._hunger
        if priority and not self._cur_water.is_defined():
            self._find_water(water)
        elif not self._cur_water.is_defined() \
                and not self._cur_eat.is_defined():
            self._find_eat(eat)

    def _move_to_water(self):
        self._move_to(self._cur_water.scene_pos)
        if self.scene_pos == self._cur_water.scene_pos:
            self._thirst += self._CONSTS.DRINKING_VALUE
            self._cur_water = SimulatingCell()

    def _is_well_fed(self):
        pass

    def _move_to_eat(self):
        self._move_to(self._cur_eat.scene_pos)
        if self.scene_pos == self._cur_eat.scene_pos:
            self._hunger += self._satiety()
            if self._is_well_fed():
                self._reproduced = True
                self._hunger -= self._reproduce_expenses()
            self._ate = True

    def _move_away_from_predator(self):
        self._move_to(self._cur_predator.scene_pos, True)

    def _move_to_target(self):
        if self._cur_predator.is_defined():
            self._move_away_from_predator()
        elif self._cur_water.is_defined():
            self._move_to_water()
        elif self._cur_eat.is_defined():
            if not self._cur_eat.is_alive():
                self._cur_eat = SimulatingCell()
            else:
                self._move_to_eat()
        else:
            self._random_move()

    def think(self, eat: typing.List[SimulatingCell], water: typing.List[WaterCell],
              predators: typing.List['AnimalCell'] = None):
        self._step()

        if self.is_dead():
            self.die()
            return

        if predators is not None:
            if not self._is_critical_hunger_or_thirst():
                self._find_predator(predators)
            else:
                self._cur_predator = SimulatingCell()

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
