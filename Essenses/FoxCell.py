import random
import typing

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget

from Essenses.AnimalCell import AnimalCell
from Essenses.HareCell import HareCell
from Essenses.SimulatingCell import SimulatingCell
from Essenses.WaterCell import WaterCell


class FoxCell(AnimalCell):
    def __init__(self, position: QPoint, parent=None):
        super().__init__(SimulatingCell.TYPE.Fox, position, parent)
        self.__cur_hare = HareCell(QPoint(-1, -1))
        self.__cur_water = WaterCell(QPoint(-1, -1))
        self._speed = 2
        self.update()

    def paint(self, painter: QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.setBrush(QBrush(QColor("orange")))
        painter.drawRect(QRect(0, 0, 20, 20))

    def eaten_hare(self):
        self._ate = False
        return self.__cur_hare

    def eat(self):
        self.__cur_hare = HareCell(QPoint(-1, -1))

    def think(self, hares: typing.List[HareCell], water: typing.List[WaterCell]):
        self._step()

        if self.is_dead():
            return

        priority = self._thirst < self._hunger

        if self.__cur_water.scene_pos.x() == -1 and priority:
            for cur_water in water:
                dist = SimulatingCell.calc_distance(self.scene_pos, cur_water.scene_pos)
                if dist <= 3:
                    self.__cur_water = cur_water

        elif self.__cur_hare.scene_pos.x() == -1 and self.__cur_water.scene_pos.x() == -1:
            for cur_hare in hares:
                dist = SimulatingCell.calc_distance(self.scene_pos, cur_hare.scene_pos)
                if dist <= 3:
                    self.__cur_hare = cur_hare

        if self.__cur_water.scene_pos.x() != -1:
            self._move_to(self.__cur_water)
            if self.scene_pos == self.__cur_water.scene_pos:
                self._thirst += 5
                self.__cur_water = WaterCell(QPoint(-1, -1))
        elif self.__cur_hare.scene_pos.x() != -1:
            self._move_to(self.__cur_hare)
            if self.scene_pos == self.__cur_hare.scene_pos:
                self._hunger += 5
                if self._hunger > 10:
                    self._reproduced = True
                    self._hunger -= 3
                self._ate = True
        else:
            self._crossed += self._speed
            if self._crossed == 2:
                self._crossed = 0
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                try:
                    self._move(dx, 0)
                except ValueError:
                    self._move(-dx, 0)
                try:
                    self._move(0, dy)
                except ValueError:
                    self._move(0, -dy)
