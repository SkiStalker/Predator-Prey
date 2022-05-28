import sys
from PyQt5.QtWidgets import QApplication
from PredatorPrey import PredatorPrey


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = PredatorPrey()
    w.show()

    sys.exit(app.exec_())
