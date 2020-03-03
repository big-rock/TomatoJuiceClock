# !/usr/bin/python3
# -*- coding:utf-8 -*-

"""
tomatoClock组件相关
"""
import sys, time, clockElement
from PyQt5.QtWidgets import QWidget, QProgressBar, QApplication, QPushButton, QComboBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QConicalGradient, QFont,QPolygon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRectF, QPoint
"""
fucus mode下的时钟组件、圆形进度条和计数线程
"""
class clock(QWidget):
    def __init__(self, parent=None):
        super(clock,self).__init__(parent)
        self.clockMode = True #True为focus clock，False为break clock
        self.setGeometry(50,10,160,160)
        self.setWindowFlags(Qt.FramelessWindowHint) #去边框
        self.setAttribute(Qt.WA_TranslucentBackground) #背景透明
        self.getClockValue()
        self.initUI()
        self.show()

    def getClockValue(self):
        file = open("config/clockValue.txt", 'r')
        valueStr = file.readline()
        valueList = valueStr.split("$")
        self.totalTime = int(valueList[1])

    def initUI(self):
        self.time = timeProgress(self.totalTime, self)
        self.breakClock = breakProgress(self)
        self.breakClock.setVisible(False)
        self.time.playCounter.finished.connect(self.runBreakClock)

    def runBreakClock(self):
        self.soundplayer = clockElement.playSound()
        self.time.setVisible(False)
        self.breakClock.setVisible(True)
        self.breakClock.breakCounter.start()
        self.soundplayer.playBreakSound()
        self.breakClock.breakCounter.finished.connect(self.soundplayer.stopBreakSound)

    def clockStart(self):
        self.time.playCounter.start()

    def clockPause(self):
        self.time.playCounter.pauseTime()

class timeProgress(QWidget):
    def __init__(self, int, parent=None):
        super(timeProgress, self).__init__(parent)
        self.setFixedSize(160,160)
        self.time = 0
        self.persent = 0
        self.targetTime = int
        self.text = str((self.targetTime - self.time) // 60) + ":" + str((self.targetTime - self.time) % 60) + "0"
        self.playCounter = counter(self.targetTime)
        self.playCounter.clockCounter.connect(self.valueUpdate)

    def setTotalTime(self,int):
        self.targetTime = int

    def valueUpdate(self, value):
        self.time = value
        self.persent = self.time // self.targetTime
        if ((self.targetTime - self.time) // 60) < 10:
            self.minutes = "0" + str((self.targetTime - self.time) // 60)
        else:
            self.minutes = str((self.targetTime - self.time) // 60)
        if ((self.targetTime - self.time) % 60) < 10:
            self.second = "0" + str((self.targetTime - self.time) % 60)
        else:
            self.second = str((self.targetTime - self.time) % 60)
        self.text = self.minutes + ":" + self.second

    def paintEvent(self, QPaintEvent):
        rotateAngle = 360 * self.persent
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
        painter.drawText(QRectF(4,4,148,148),Qt.AlignCenter, "%s" % self.text)
        self.update()

class breakProgress(QWidget):
    def __init__(self, parent=None):
        super(breakProgress, self).__init__(parent)
        self.setFixedSize(160,160)
        self.time = 0
        self.persent = 0
        self.setTargetTime()
        self.text = str((self.targetTime - self.time) // 60) + ":" + str((self.targetTime - self.time) % 60) + "0"
        self.breakCounter = breakCount(self.targetTime)
        self.breakCounter.breakCounter.connect(self.valueUpdate)

    def setTargetTime(self):
        file = open("config/currentBreakTime.txt", "r").readline()
        self.targetTime = eval(file)

    def valueUpdate(self, value):
        self.time = value
        self.persent = self.time // self.targetTime
        if ((self.targetTime - self.time) // 60) < 10:
            self.minutes = "0" + str((self.targetTime - self.time) // 60)
        else:
            self.minutes = str((self.targetTime - self.time) // 60)

        if ((self.targetTime - self.time) % 60) < 10:
            self.second = "0" + str((self.targetTime - self.time) % 60)
        else:
            self.second = str((self.targetTime - self.time) % 60)
        self.text = self.minutes + ":" + self.second


    def paintEvent(self, QPaintEvent):
        rotateAngle = 360 * self.persent
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing) #去锯齿

        #绘制过程
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#99CC99")))
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
        painter.setPen(QColor("#99CC99"))
        painter.drawText(QRectF(4,4,148,148),Qt.AlignCenter, "%s" % self.text)
        self.update()

class counter(QThread):
    clockCounter = pyqtSignal(int)
    finished = pyqtSignal()
    count = 0
    isPause = True
    def __init__(self,totalTime):
        super(counter, self).__init__()
        self.targetTime = totalTime

    def run(self):
        self.isPause = not self.isPause
        while self.count < self.targetTime:
            time.sleep(1)
            if self.isPause:
                break
            self.count += 1
            self.clockCounter.emit(self.count)

        if self.count == self.targetTime:
            self.finished.emit()

    def pauseTime(self):
        self.isPause = not self.isPause

class breakCount(QThread):
    breakCounter = pyqtSignal(int)
    breakFinished = pyqtSignal()
    count = 0
    def __init__(self,TargetTime=100):
        super(breakCount, self).__init__()
        self.targetTime = TargetTime

    def run(self):
        while self.count < self.targetTime:
            time.sleep(1)
            self.count += 1
            self.breakCounter.emit(self.count)
        if self.count == self.targetTime:
            self.breakFinished.emit()