from pyqtgraph import PlotWidget, plot
from PyQt5.QtCore import QPoint, QRect
import pyqtgraph as pg


class Graph(PlotWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.setBackground("w")
        self.setXRange(0, 100)
        self.setYRange(0, 100)
        self.setGeometry(QRect(0, 0, 200, 200))
