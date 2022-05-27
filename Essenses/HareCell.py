import random
import typing

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget

from Essenses.AnimalCell import AnimalCell
from Essenses.GrassCell import GrassCell
from Essenses.SimulatingCell import SimulatingCell
from Essenses.WaterCell import WaterCell


class HareCell(AnimalCell):
    def __init__(self, position: QPoint, parent=None):
        super().__init__(SimulatingCell.TYPE.Hare, position, parent)
        self.__cur_water: WaterCell = WaterCell(QPoint(-1, -1))
        self.__cur_grass: GrassCell = GrassCell(QPoint(-1, -1))
        self._speed = 1
        self.update()

    def eaten_grass(self):
        self._ate = False
        return self.__cur_grass

    def eat(self):
        self.__cur_grass = GrassCell(QPoint(-1, -1))

    def paint(self, painter: QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.setBrush(QBrush(QColor("brown")))
        painter.drawRect(QRect(0, 0, 20, 20))

    def think(self, grass: typing.List[GrassCell], water: typing.List[WaterCell]):
        self._step()

        if self.is_dead():
            return

        priority = self._thirst < self._hunger

        if self.__cur_water.scene_pos.x() == -1 and priority:
            for cur_water in water:
                dist = SimulatingCell.calc_distance(self.scene_pos, cur_water.scene_pos)
                if dist <= 3:
                    self.__cur_water = cur_water

        elif self.__cur_grass.scene_pos.x() == -1 and self.__cur_water.scene_pos.x() == -1:
            for cur_grass in grass:
                dist = SimulatingCell.calc_distance(self.scene_pos, cur_grass.scene_pos)
                if dist <= 3:
                    self.__cur_grass = cur_grass

        if self.__cur_water.scene_pos.x() != -1:
            self._move_to(self.__cur_water)
            if self.scene_pos == self.__cur_water.scene_pos:
                self._thirst += 5
                self.__cur_water = WaterCell(QPoint(-1, -1))
        elif self.__cur_grass.scene_pos.x() != -1:
            self._move_to(self.__cur_grass)
            if self.scene_pos == self.__cur_grass.scene_pos:
                self._hunger += 5
                if self._hunger > 10:
                    self._reproduced = True
                    self._hunger -= 3
                self._ate = True
        else:
            self._crossed += self.__speed
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


