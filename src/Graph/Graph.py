import typing

from pyqtgraph import PlotWidget,  mkPen
from PyQt5.QtCore import QRect


class Graph(PlotWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.setBackground("w")
        self.setXRange(0, 10)
        self.setYRange(0, 10)
        self.setGeometry(QRect(0, 0, 200, 200))
        self.setLimits(xMin=0, yMin=0)
        self._points_x: typing.List[int] = []
        self._points_y: typing.List[int] = []

    def set_labels(self, left_label: str, bottom_label: str):
        self.setLabel('left', left_label)
        self.setLabel('bottom', bottom_label)

    def add_point(self, x: int, y: int):
        self._points_x.append(x)
        self._points_y.append(y)
        self.plot(self._points_x, self._points_y, pen=mkPen(width=3, color=(0, 0, 0)))
        self.update()
