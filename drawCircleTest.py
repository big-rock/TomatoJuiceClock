# !/usr/bin/python3
# -*- coding:utf-8 -*-

# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtGui import QPainter, QPen, QBrush
# from PyQt5.QtCore import Qt
#
# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.title = "PyQt5 Drawing Tutorial"
#         self.setGeometry(150,150,500,500)
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.show()
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setPen(QPen(Qt.green, 8, Qt.SolidLine))
#         painter.drawEllipse(40,40,400,400)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = Window()
#     sys.exit(app.exec_())


import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)

TIME_LIMIT = 100

class External(QThread):
    countChanged = pyqtSignal(int)

    def run(self):
        count = 0
        while count < TIME_LIMIT:
            count += 1
            time.sleep(0.5)
            self.countChanged.emit(count)


class Actions(QDialog):
    """
    Simple dialog that consists of a Progress Bar and a Button.
    Clicking on the button results in the start of a timer and
    updates the progress bar.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Progress Bar')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.button = QPushButton('Start', self)
        self.button.move(0, 30)
        self.show()

        self.button.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        self.calc = External()
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()

    def onCountChanged(self, value):
        self.progress.setValue(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Actions()
    sys.exit(app.exec_())