# !/usr/bin/python3
# -*- coding:utf-8 -*-
# Author = big_rock
'''
this script init main window's features.
'''
import sys,os
import TomatoClock, TimerControl
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QApplication, QPushButton, \
    QGridLayout, QSystemTrayIcon, QVBoxLayout, QLabel,QLineEdit,\
    QComboBox, QMainWindow
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt


class TomatoWindow(QWidget):
    mode = False
    existTaskList = []
    clocksTime = []
    selectedTaskName = " "
    selectedTaskTime = 0

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 500)
        self.checkConfig()
        self.initUI()

    def checkConfig(self):
        file = open("config/FocusClockListFile.txt", "r").readlines()
        print(file)
        if file:
            self.mode = True
            for i in file:
                print(i)
                elements = i.split("$")
                print(elements)
                taskName = elements[0]
                self.existTaskList.append(taskName)
                taskTime = elements[1].strip("\n")
                self.clocksTime.append(taskTime)
        else:
            self.mode = False

    def initUI(self):
        #left "enable window maxsize and close botton status bar
        self.move(600,100)
        self.setWindowTitle('JUICE - a tomato clock APP')

        #准备图片素材
        infoIcon = QIcon()
        infoIcon.addFile("ui/infoIcon.png", size=QSize(48, 48), mode=infoIcon.Normal)
        settingsIcon = QIcon()
        settingsIcon.addFile("ui/settingsIcon.png", size=QSize(48, 48), mode=settingsIcon.Normal)
        dataIcon = QIcon()
        dataIcon.addFile("ui/dataIcon.png", size=QSize(48, 48), mode=dataIcon.Normal)
        addIcon = QIcon()
        addIcon.addFile("ui/addIcon.png", size=QSize(48, 48), mode=dataIcon.Normal)

        #设置button, 装填按钮
        self.infoBtn = QPushButton(self)
        self.infoBtn.setIcon(infoIcon)
        self.infoBtn.setFlat(True)
        self.infoBtn.setGeometry(0,0,30,30)

        self.settingsBtn = QPushButton(self)
        self.settingsBtn.setIcon(settingsIcon)
        self.settingsBtn.setFlat(True)
        self.settingsBtn.setGeometry(0,470,30,30)

        self.dataBtn = QPushButton(self)
        self.dataBtn.setIcon(dataIcon)
        self.dataBtn.setFlat(True)
        self.dataBtn.setGeometry(270,0,30,30)

        self.addBtn = QPushButton(self)
        self.addBtn.setIcon(addIcon)
        self.addBtn.setFlat(True)
        self.addBtn.setGeometry(270,470,30,30)

        #放置番茄钟相关组件, ！！！不同状态，放置不同内容！！！
        if self.mode == False:
            self.blank = blankView(self)
        else:
            self.clock = clockView(self)
            self.show()
            self.taskSelect = QComboBox(self)
            self.taskSelect.addItems(self.existTaskList)

            self.playButton = TimerControl.playButton(self)

            self.closeBtn = QPushButton(self)
            self.closeBtn.setIcon(QIcon("ui/deletIcon.png"))
            self.closeBtn.setFlat(True)

            grid = QGridLayout(self)
            grid.addWidget(self.clock,0,0)
            grid.addWidget(self.taskSelect,1,0)
            grid.addWidget(self.playButton,2,0)
            grid.addWidget(self.closeBtn,3,0)
            self.setLayout(grid)

        #设置类按钮行为
        self.addClockDialog = addClockDialog(self)
        self.addBtn.clicked.connect(self.addClockDialog.exec_)

        self.settingsDialog = settingsDialog(self)
        self.settingsBtn.clicked.connect(self.settingsDialog.exec_)

        self.show()

class blankView(QWidget):
    def __init__(self, parent=None):
        super(blankView, self).__init__(parent)
        self.setGeometry(30, 30, 240, 440)
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        text = '当前尚未创建任何Tomato Clock.\n\n' \
               '点击右下方的添加icon\n' \
               '来创建一个Tomato Clock吧！'
        self.label.setText(text)
        self.label.setFont(QFont("", 12))
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.label)
        self.setLayout(vbox)

class clockView(QWidget):
    def __init__(self, parent=None):
        super(clockView, self).__init__(parent)
        self.setGeometry(30,30,200,200)
        self.initUI()

    def initUI(self):
        self.clock = TomatoClock.clock(self)


class addClockDialog(QDialog):
    def __init__(self, parent=None):
        super(addClockDialog,self).__init__(parent)
        self.move(600,200)
        self.setFixedSize(300,200)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("设置番茄钟")

        self.inputBox = QLineEdit()
        self.label = QLabel('<font color="#ff0000">*每个番茄钟的时长，请在"设置"中进行修改')
        self.label.setFont(QFont("",12))
        self.acceptBtn = QPushButton("添加")
        self.rejectBtn = QPushButton("取消")

        grid = QGridLayout()
        grid.addWidget(self.inputBox,1,0,2,4)
        grid.addWidget(self.label,3,0,1,4)
        grid.addWidget(self.acceptBtn,4,3)
        grid.addWidget(self.rejectBtn,4,0)
        self.setLayout(grid)

        #按钮事件对应处理
        self.acceptBtn.clicked.connect(self.acceptAction)
        self.rejectBtn.clicked.connect(self.rejectAction)

    def acceptAction(self):
        self.close()

    def rejectAction(self):
        self.close()

class settingsDialog(QDialog):
    def __init__(self, parent=None):
        super(settingsDialog,self).__init__(parent)
        self.move(600, 200)
        self.setFixedSize(300, 300)
        self.initUI()

    def initUI(self):
        self.focusDruationLabel = QLabel("番茄钟时长：")
        self.breakDruationLabel = QLabel("休息钟时长：")
        self.focusBgmLabel = QLabel("番茄钟音效：")
        self.rejectBtn = QPushButton("取消")
        self.accpetBtn = QPushButton("确定")

        #create a drop box
        #create a timer list for focusDruationLabel and break label
        self.focusDruationList = ["25:00","15:00","20:00","30:00","35:00","40:00","45:00","50:00","55:00"]
        self.focusComboBox = QComboBox(self)
        self.focusComboBox.addItems(self.focusDruationList)

        self.breakDruationList = ["5:00","10:00","15:00"]
        self.breakComboBox = QComboBox(self)
        self.breakComboBox.addItems(self.breakDruationList)
        #create a file name list for bgm label
        self.getFileName()
        self.focusBgmComboBox = QComboBox(self)
        self.focusBgmComboBox.addItems(self.fileNameList)

        grid = QGridLayout()
        grid.addWidget(self.focusDruationLabel,0,0)
        grid.addWidget(self.breakDruationLabel,1,0)
        grid.addWidget(self.focusBgmLabel,2,0)
        grid.addWidget(self.focusComboBox,0,1,1,3)
        grid.addWidget(self.breakComboBox,1,1,1,3)
        grid.addWidget(self.focusBgmComboBox,2,1,1,3)
        grid.addWidget(self.rejectBtn,3,0)
        grid.addWidget(self.accpetBtn,3,3)
        self.setLayout(grid)

        #create event and action
        self.accpetBtn.clicked.connect(self.accpetAction)
        self.rejectBtn.clicked.connect(self.rejectAction)

    def getFileName(self):
        self.fileNameList = []
        for self.file in os.listdir("./audio"):
            self.fileNameList.append(self.file)

    def accpetAction(self):
        self.close()

    def rejectAction(self):
        self.close()

class dataDialog(QDialog):
    def __init__(self,parent=None):
        super(dataDialog,self).__init__(parent)
        self.init(self)

    def initUI(self):
        pass

class infoDialog(QDialog):
    def __init__(self, parent=None):
        super(infoDialog,self).__init__(parent)
        self.initUI(self)

    def initUI(self):
        pass

class Tray:
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tomato = TomatoWindow()
    sys.exit(app.exec_())
