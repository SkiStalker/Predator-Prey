import typing

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget

from src.Essenses.AnimalCell import AnimalCell
from src.Essenses.SimulatingCell import SimulatingCell


class HareCell(AnimalCell):
    def __init__(self, position: QPoint, parent=None):
        super().__init__(SimulatingCell.TYPE.Hare, position, parent)
        self._speed = AnimalCell._CONSTS.HARE_SPEED
        self._hunger = AnimalCell._CONSTS.HARE_INIT_HUNGER
        self._thirst = AnimalCell._CONSTS.HARE_INIT_THIRST
        self.update()

    def paint(self, painter: QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.setBrush(QBrush(QColor("brown")))
        painter.drawRect(QRect(0, 0, 20, 20))

    def get_target_type(self) -> SimulatingCell.TYPE:
        if self._cur_water.is_defined():
            return SimulatingCell.TYPE.Water
        elif self._cur_eat.is_defined():
            return SimulatingCell.TYPE.Grass
        elif self._cur_predator.is_defined():
            return SimulatingCell.TYPE.Fox
        else:
            return SimulatingCell.TYPE.Nothing

    def _is_well_fed(self):
        return self._hunger > AnimalCell._CONSTS.HARE_WELL_FED

    def reproduce_count(self):
        return AnimalCell._CONSTS.HARE_REPRODUCE_COUNT

    def _reproduce_expenses(self):
        return AnimalCell._CONSTS.HARE_REPRODUCTION_EXPENSES

    def _find_range(self):
        return AnimalCell._CONSTS.HARE_VIEW_RANGE

    def _satiety(self):
        return AnimalCell._CONSTS.HARE_SATIETY_VALUE

    def _is_critical_hunger_or_thirst(self):
        return self.hunger < AnimalCell._CONSTS.HARE_CRITICAL_HUNGER_OR_THIRST or \
               self.thirst < AnimalCell._CONSTS.HARE_CRITICAL_HUNGER_OR_THIRST

    def _find_predator(self, predators: typing.List[AnimalCell]):
        self._cur_predator = self._find_best_object(predators)
