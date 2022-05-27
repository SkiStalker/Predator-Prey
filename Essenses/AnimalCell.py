import random
import typing

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget

from Essenses.GrassCell import GrassCell
from Essenses.SimulatingCell import SimulatingCell
from Essenses.WaterCell import WaterCell


class AnimalCell(SimulatingCell):
    def __init__(self, tp: SimulatingCell.TYPE, position: QPoint, parent=None):
        super().__init__(tp, position, parent)
        self._hunger = 5
        self._thirst = 5
        self._ate = False
        self._reproduced = False
        self._crossed = 0
        self._speed = 0
        self.setZValue(1)

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

    def _move(self, dx: int, dy: int):
        if not (0 <= self.scene_pos.x() + dx < 560 // 20):
            raise ValueError("Incorrect dx")

        if not (0 <= self.scene_pos.y() + dy < 560 // 20):
            raise ValueError("Incorrect dy")

        self.scene_pos = QPoint(self.scene_pos.x() + dx,
                                self.scene_pos.y() + dy)

    def _move_to(self, cell: SimulatingCell):
        offset: QPoint = self.scene_pos - cell.scene_pos
        self._crossed += self._speed
        if self._crossed == 2:
            self._crossed = 0
            dx, dy = 0, 0
            if offset.x() != 0:
                dx = -(offset.x() // abs(offset.x()))
            if offset.y() != 0:
                dy = -(offset.y() // abs(offset.y()))

            self._move(dx, dy)
