# !/usr/bin/python3
# -*- coding:utf-8 -*-

"""
绘制play按钮和暂停按钮
"""

import sys, os
from PyQt5.QtWidgets import QWidget,QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPolygon, QColor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSound, QSoundEffect
class playButton(QPushButton):
    def __init__(self, parent=None):
        super(playButton, self).__init__(parent)
        self.setFixedSize(42,42)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#FF9966")))
        painter.setRenderHints(QPainter.Antialiasing) #抗锯齿

        #绘制过程
        polygon = QPolygon()
        polygon.setPoints([10,0,10,40,40,20])
        painter.drawPolygon(polygon)
        self.update()

class pauseButton(QPushButton):
    def __init__(self, parent=None):
        super(pauseButton, self).__init__(parent)
        self.setFixedSize(42,42)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#FF9966")))
        painter.setRenderHints(QPainter.Antialiasing)

        #绘制过程
        painter.drawRect(4,2,15,40)
        painter.drawRect(23,2,15,40)
        self.update()

class playSound(QWidget):
    def __init__(self, parent=None):
        super(playSound, self).__init__(parent)
        self.fileName = ""
        self.getFileName()
        self.focusSound = QSound(self.fileName)
        self.focusSound.setLoops(10)

        self.finishedSound = QSound("config/ringring.wav")

        self.breakSound = QSound("config/happy.wav")
        self.breakSound.setLoops(10)

        self.accpetSound = QSound("config/accpet.wav")

        self.errorSound = QSound("config/error.wav")
        return

    def getFileName(self):
        file = open("config/currentBgm.txt", "r").readline()
        text = file.strip("\n")
        self.fileName = "audio/" + text
        return

    def playFocusSound(self):
        self.focusSound.play()
        return

    def playFinishedSound(self):
        self.finishedSound.play()
        return

    def playBreakSound(self):
        self.breakSound.play()
        return

    def playAcceptSound(self):
        self.accpetSound.play()
        return

    def playErrorSound(self):
        self.errorSound.play()
        return

    def stopFocusSound(self):
        self.focusSound.stop()

    def stopBreakSound(self):
        self.breakSound.stop()

