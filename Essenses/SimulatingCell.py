import math
import typing

from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem, QWidget, QStyleOptionGraphicsItem
from enum import Enum


class SimulatingCell(QGraphicsRectItem):
    class TYPE(Enum):
        Nothing = 0
        Grass = 1
        Fox = 2
        Hare = 3
        Water = 4

    def __init__(self, cell_type: TYPE, position: QPoint, parent=None):
        super().__init__(parent)
        self.__cell_type = cell_type
        if position != QPoint(-1, -1):
            self.__scene_pos = QPoint(position.x() % 20, position.y() % 20)
        else:
            self.__scene_pos = position
        self.setPos(position)

    @property
    def scene_pos(self):
        return self.__scene_pos

    @scene_pos.setter
    def scene_pos(self, position: QPoint):
        if (position.x() < 0) or (position.y() < 0):
            raise ValueError("Incorrect position")
        self.__scene_pos = position
        self.setPos(position.x() * 20, position.y() * 20)

    @property
    def cell_type(self):
        return self.__cell_type

    @cell_type.setter
    def cell_type(self, val: TYPE):
        self.__cell_type = val

    @staticmethod
    def calc_distance(first: QPoint, second: QPoint):
        return math.sqrt((first.x() + second.x())**2 + (first.y() + second.y())**2)
