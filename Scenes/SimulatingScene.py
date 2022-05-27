import random
from typing import List

from PyQt5.QtCore import QRect, QRectF, QLine, QLineF, QPoint, QTimer
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem

from Essenses.FoxCell import FoxCell
from Essenses.GrassCell import GrassCell
from Essenses.HareCell import HareCell
from Essenses.WaterCell import WaterCell


class SimulatingScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(QRectF(0.0, 0.0, 560, 560))

        self.__foxes: List[FoxCell] = []
        self.__hares: List[HareCell] = []
        self.__grass: List[GrassCell] = []
        self.__water: List[WaterCell] = []
        self.draw_grid()
        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.step_simulation)
        self.update()

    def start_simulating(self, delay: int):
        self.simulation_timer.start(delay)

    def step_simulation(self):
        for fox in self.__foxes:
            fox.think(self.__hares, self.__water)
            if fox.is_dead():
                self.__foxes.remove(fox)
                self.removeItem(fox)
                del fox
                print("Fox dead")
            else:
                if fox.is_reproduced():
                    fox.reproduce()
                    new_fox = HareCell(QPoint(0, 0))
                    self.__hares.append(new_fox)
                    self.addItem(new_fox)
                    print("Fox reproduced")
                if fox.is_ate():
                    hare = fox.eaten_hare()
                    self.__hares.remove(hare)
                    self.removeItem(hare)
                    del hare
                    fox.eat()
                    print("Hare eat")

        for hare in self.__hares:
            hare.think(self.__grass, self.__water)
            if hare.is_dead():
                self.__hares.remove(hare)
                self.removeItem(hare)
                del hare
                print("Hare dead")
            else:
                if hare.is_reproduced():
                    hare.reproduce()
                    new_hare = HareCell(QPoint(0, 0))
                    self.__hares.append(new_hare)
                    self.addItem(new_hare)
                    print("Hare reproduced")
                if hare.is_ate():
                    grass = hare.eaten_grass()
                    self.__grass.remove(grass)
                    self.removeItem(grass)
                    del grass
                    hare.eat()
                    print("Grass eat")

        self.update()

    def stop_simulating(self):
        self.simulation_timer.stop()

    def generate_scene(self, foxes_count: int, hares_count: int):
        if foxes_count < 1:
            raise ValueError("Foxes count less 1")
        if hares_count < 1:
            raise ValueError("Hares count less 1")

        for i in range(0, 560 // 20):
            for j in range(0, 560 // 20):
                res = 0
                if len(self.__foxes) == 0:
                    res = 1
                elif len(self.__hares) == 0:
                    res = 2
                elif len(self.__water) == 0:
                    res = 3
                elif len(self.__grass) == 0:
                    res = 4
                else:
                    res = random.randint(0, 4)

                _i = i * 20
                _j = j * 20

                if res == 0:
                    pass
                elif res == 1:
                    if len(self.__foxes) < foxes_count:
                        new_fox = FoxCell(QPoint(_i, _j))
                        self.__foxes.append(new_fox)
                        self.addItem(new_fox)
                elif res == 2:
                    if len(self.__hares) < hares_count and j > 2:
                        new_hare = HareCell(QPoint(_i, _j))
                        self.__hares.append(new_hare)
                        self.addItem(new_hare)
                elif res == 3:
                    new_water = WaterCell(QPoint(_i, _j))
                    self.__water.append(new_water)
                    self.addItem(new_water)
                elif res == 4:
                    new_grass = GrassCell(QPoint(_i, _j))
                    self.__grass.append(new_grass)
                    self.addItem(new_grass)

    def draw_grid(self):
        for i in range(0, 560, 20):
            if i < 560:
                line_h = QGraphicsLineItem()
                line_h.setLine(QLineF(i, 0, i, 560))
                line_h.setPen(QPen(QColor("b")))
                self.addItem(line_h)
            line_w = QGraphicsLineItem()
            line_w.setLine(QLineF(0, i, 560, i))
            line_w.setPen(QPen(QColor("b")))
            self.addItem(line_w)
