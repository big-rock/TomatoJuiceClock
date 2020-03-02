# !/usr/bin/python3
# -*- coding:utf-8 -*-

"""
tomatoClock组件相关
"""
import sys, time
from PyQt5.QtWidgets import QWidget, QProgressBar, QApplication, QPushButton, QComboBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QConicalGradient, QFont,QPolygon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRectF, QPoint
"""
fucus mode下的时钟组件、圆形进度条和计数线程
"""
class clock(QWidget):
    def __init__(self, parent=None):
        super(clock,self).__init__(parent)
        self.setGeometry(50,10,160,160)
        self.setWindowFlags(Qt.FramelessWindowHint) #去边框
        self.setAttribute(Qt.WA_TranslucentBackground) #背景透明
        self.initUI()

    def initUI(self):
        self.time = timeProgress(self)
        self.show()

class timeProgress(QWidget):
    def __init__(self, parent=None):
        super(timeProgress, self).__init__(parent)
        self.setFixedSize(160,160)
        self.persent = 0
        self.playCounter = counter()
        self.playCounter.clockCounter.connect(self.valueUpdate)
        self.playCounter.start()

    def valueUpdate(self, value):
        self.persent = value

    def paintEvent(self, QPaintEvent):
        rotateAngle = 360 * self.persent / 100
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing) #去锯齿

        #绘制过程
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#FF9966")))
        painter.drawEllipse(3,3,150,150) #画外圆

        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawEllipse(5,5,146,146) #画内圆

        gradient = QConicalGradient(50, 50, 91)
        gradient.setColorAt(0, QColor("#e1e1e1"))
        gradient.setColorAt(1, QColor("#e1e1e1"))
        self.pen = QPen()
        self.pen.setBrush(gradient)
        self.pen.setWidth(2)
        self.pen.setCapStyle(Qt.RoundCap)
        painter.setPen(self.pen)
        painter.drawArc(QRectF(4,4,148,148), (90-0)*16, rotateAngle * 16)
        font = QFont()
        font.setPointSize(25)
        painter.setFont(font)
        painter.setPen(QColor("#FF9966"))
        painter.drawText(QRectF(4,4,148,148),Qt.AlignCenter, "%d" % self.persent)
        self.update()

class counter(QThread):
    clockCounter = pyqtSignal(int)
    count = 0
    def __init__(self):
        super(counter, self).__init__()

    def run(self):
        while self.count < 100:
            self.count += 1
            time.sleep(0.1)
            self.clockCounter.emit(self.count)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = pauseButton()
    sys.exit(app.exec_())