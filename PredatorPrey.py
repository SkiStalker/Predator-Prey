import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsView
from PyQt5.QtCore import QPoint, QRect, QRectF

from Graph.Graph import Graph
from Scenes.SimulatingScene import SimulatingScene


class PredatorPrey(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Forms/PredatorPrey.ui", self)
        self.foxes_hares = Graph(self)
        self.foxes_hares.move(QPoint(565, 50))
        self.foxes_hares.setLimits(xMin=0, xMax=100, yMin=0, yMax=100)

        self.foxes_time = Graph(self)
        self.foxes_time.move(QPoint(565, 250))
        self.foxes_time.setLimits(xMin=0, yMin=0,)

        self.hares_time = Graph(self)
        self.hares_time.move(QPoint(565, 450))
        self.hares_time.setLimits(xMin=0, yMin=0,)

        self.simulatingScene = SimulatingScene(self)

        self.simulatingView.setScene(self.simulatingScene)

        self.simulatingScene.generate_scene(5, 5)

        self.__set_connections()
        self.update()

    def start_simulation(self):
        self.simulatingScene.start_simulating(self.speedSpinBox.value() * 1000)

    def stop_simulation(self):
        self.simulatingScene.stop_simulating()

    def change_speed(self):
        self.stop_simulation()
        self.start_simulation()

    def __set_connections(self):
        self.startButton.clicked.connect(self.start_simulation)
        self.stopButton.clicked.connect(self.stop_simulation)
        self.speedSpinBox.valueChanged.connect(self.change_speed)

