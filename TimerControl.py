# !/usr/bin/python3
# -*- coding:utf-8 -*-

"""
绘制play按钮和暂停按钮
"""

import sys, os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QPolygon, QColor
from PyQt5.QtCore import Qt
class playButton(QWidget):
    def __init__(self, parent=None):
        super(playButton, self).__init__(parent)
        self.setFixedSize(42,42)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#FF9966")))
        painter.setRenderHints(QPainter.Antialiasing) #抗锯齿

        #绘制过程
        polygon = QPolygon()
        polygon.setPoints([0,0,0,40,40,20])
        painter.drawPolygon(polygon)
        self.update()

class pauseButton(QWidget):
    def __init__(self, parent=None):
        super(pauseButton, self).__init__(parent)
        self.setFixedSize(42,42)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#FF9966")))
        painter.setRenderHints(QPainter.Antialiasing)

        #绘制过程
        painter.drawRect(4,0,15,42)
        painter.drawRect(23,0,15,42)
        self.update()