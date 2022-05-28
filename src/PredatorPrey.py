import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsView
from PyQt5.QtCore import QPoint, QRect, QRectF, QTimer

from Graph.Graph import Graph
from Scenes.SimulatingScene import SimulatingScene


class PredatorPrey(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("src/Forms/PredatorPrey.ui", self)
        self.foxes_hares = Graph(self)
        self.foxes_hares.move(QPoint(565, 50))
        self.foxes_hares.set_labels('foxes', 'hares')

        self.foxes_time = Graph(self)
        self.foxes_time.move(QPoint(565, 250))
        self.foxes_time.set_labels('foxes', 'time')

        self.hares_time = Graph(self)
        self.hares_time.move(QPoint(565, 450))
        self.hares_time.set_labels('hares', 'time')

        self.simulating_scene = SimulatingScene(self)

        self.simulatingView.setScene(self.simulating_scene)

        self.simulating_scene.generate_scene(5, 5)

        self.simulation_timer = QTimer()
        self.cur_time = 0
        self.__set_connections()
        self.update()

    def start_simulation(self):
        self.simulation_timer.start(self.speedSpinBox.value() * 1000)

    def stop_simulation(self):
        self.simulation_timer.stop()

    def _step_simulation(self):
        self.simulating_scene.step_simulation()
        foxes = self.simulating_scene.get_foxes_count()
        hares = self.simulating_scene.get_hares_count()
        self.hares_time.add_point(self.cur_time, hares)
        self.foxes_time.add_point(self.cur_time, foxes)
        self.foxes_hares.add_point(hares, foxes)
        self.cur_time += 1

    def change_speed(self):
        self.stop_simulation()
        self.start_simulation()

    def __set_connections(self):
        self.startButton.clicked.connect(self.start_simulation)
        self.stopButton.clicked.connect(self.stop_simulation)
        self.speedSpinBox.valueChanged.connect(self.change_speed)
        self.simulation_timer.timeout.connect(self._step_simulation)

