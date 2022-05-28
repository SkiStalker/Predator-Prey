import random
import typing

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget

from src.Essenses.AnimalCell import AnimalCell
from src.Essenses.HareCell import HareCell
from src.Essenses.SimulatingCell import SimulatingCell
from src.Essenses.WaterCell import WaterCell


class FoxCell(AnimalCell):
    def __init__(self, position: QPoint, parent=None):
        super().__init__(SimulatingCell.TYPE.Fox, position, parent)
        self._speed = self._FOX_SPEED
        self.update()

    def paint(self, painter: QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.setBrush(QBrush(QColor("orange")))
        painter.drawRect(QRect(0, 0, 20, 20))

    def get_target_type(self) -> SimulatingCell.TYPE:
        if self._cur_water.is_defined():
            return SimulatingCell.TYPE.Water
        elif self._cur_eat.is_defined():
            return SimulatingCell.TYPE.Hare
        else:
            return SimulatingCell.TYPE.Nothing
