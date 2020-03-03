# !/usr/bin/python3
# -*- coding:utf-8 -*-
# Author = big_rock
'''
this script init main window's features.
'''
import sys,os
import TomatoClock, clockElement
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QPushButton, \
    QGridLayout, QVBoxLayout, QLabel,QLineEdit,\
    QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt, pyqtSignal


class TomatoWindow(QWidget):
    taskDict = {}
    selectedTaskName = " "
    selectedTaskTime = 0

    def __init__(self):
        super().__init__()
        self.clockMode = False
        self.switchMode = False #True是播放状态，False是停止状态
        self.setFixedSize(300, 500)

        self.playButton = clockElement.playButton(self)
        self.playButton.setVisible(False)
        self.pauseButton = clockElement.pauseButton(self)
        self.pauseButton.setVisible(False)

        self.checkConfig()
        self.initUI()
        self.show()

    def checkConfig(self):
        self.existTaskList = []
        self.clocksTime = []

        file = open("config/FocusClockListFile.txt", "r").readlines()
        if file:
            self.clockMode = True
            try:
                for i in file:
                    elements = i.split("$")
                    taskName = elements[0]
                    self.existTaskList.append(taskName)
                    taskTime = elements[1].strip("\n")
                    self.clocksTime.append(taskTime)
                    self.taskDict[taskName] = taskTime
            except:
                pass
        else:
            self.clockMode = False

    def initUI(self):
        #left "enable window maxsize and close botton status bar
        self.move(600,100)
        self.setWindowTitle('JUICE - a tomato clock APP')

        #准备图片素材
        infoIcon = QIcon()
        infoIcon.addFile("ui/infoIcon.png", size=QSize(48, 48), mode=infoIcon.Normal)
        settingsIcon = QIcon()
        settingsIcon.addFile("ui/settingsIcon.png", size=QSize(48, 48), mode=settingsIcon.Normal)
        # dataIcon = QIcon()
        # dataIcon.addFile("ui/dataIcon.png", size=QSize(48, 48), mode=dataIcon.Normal)
        addIcon = QIcon()
        addIcon.addFile("ui/addIcon.png", size=QSize(48, 48), mode=addIcon.Normal)

        # 设置button, 装填按钮
        self.infoBtn = QPushButton(self)
        self.infoBtn.setIcon(infoIcon)
        self.infoBtn.setFlat(True)
        self.infoBtn.setGeometry(0,0,30,30)

        self.settingsBtn = QPushButton(self)
        self.settingsBtn.setIcon(settingsIcon)
        self.settingsBtn.setFlat(True)
        self.settingsBtn.setGeometry(0,470,30,30)

        # self.dataBtn = QPushButton(self)
        # self.dataBtn.setIcon(dataIcon)
        # self.dataBtn.setFlat(True)
        # self.dataBtn.setGeometry(270,0,30,30)

        self.addBtn = QPushButton(self)
        self.addBtn.setIcon(addIcon)
        self.addBtn.setFlat(True)
        self.addBtn.setGeometry(270,470,30,30)

        #设置空白和有时钟两种视图

        if self.clockMode == False:
            self.blank = blankView(self)
        else:
            # 生成番茄钟视图
            self.clockView = clockView()
            self.clockView.clock.time.playCounter.finished.connect(self.intoBreak)
            self.playButton.setVisible(True)

            #生成声音
            self.mainSound = clockElement.playSound()

            # 生成task列表
            self.taskSelect = QComboBox(self)
            self.taskSelect.addItems(self.existTaskList)
            f = open("config/clockValue.txt", 'r').readline()
            name = f.split("$")
            defaultName = name[0]
            self.taskSelect.setCurrentText(defaultName)

            # 生成关闭按钮
            closeBtn = QPushButton(self)
            closeBtn.setIcon(QIcon("ui/deletIcon.png"))
            closeBtn.setFlat(True)

            self.grid = QGridLayout(self)
            self.grid.addWidget(self.clockView, 0, 0)
            self.grid.addWidget(self.taskSelect, 1, 0, Qt.AlignCenter)
            self.grid.addWidget(self.playButton, 2, 0, Qt.AlignHCenter)
            self.grid.addWidget(self.pauseButton, 2, 0, Qt.AlignHCenter)
            self.grid.addWidget(closeBtn, 3, 0, Qt.AlignHCenter)
            self.switchUI()

            # 设置按钮点击事件
            #关闭按钮，点击后重新构建一个窗口并且关闭旧的窗口，使得所有实例重建
            closeBtn.clicked.connect(self.__init__)
            closeBtn.clicked.connect(self.close)

            # 播放按钮。clock开始计时，界面切换到暂停按钮
            self.playButton.clicked.connect(self.switchUI)
            self.playButton.clicked.connect(self.valueSaver)
            self.playButton.clicked.connect(self.clockView.clock.clockStart)
            self.playButton.clicked.connect(self.mainSound.playFocusSound)

            #选择了下拉框中的不同项目，也要切换状态
            self.taskSelect.activated.connect(self.valueSaver)
            self.taskSelect.activated.connect(self.__init__)
            self.taskSelect.activated.connect(self.close)

            # 暂停按钮。clock停止计时，界面切换到播放按钮
            self.pauseButton.clicked.connect(self.switchUI)
            self.pauseButton.clicked.connect(self.clockView.clock.clockPause)
            self.pauseButton.clicked.connect(self.mainSound.stopFocusSound)

            self.clockView.clock.time.playCounter.finished.connect(self.mainSound.stopFocusSound)
            self.clockView.clock.time.playCounter.finished.connect(self.mainSound.playFinishedSound)

            self.clockView.clock.breakClock.breakCounter.finished.connect(self.mainSound.playFinishedSound)

        # 设置固定按钮事件
        # 触发新增番茄钟界面
        self.addClockDialog = addClockDialog(self)
        self.addBtn.clicked.connect(self.addClockDialog.exec_)
        # self.addClockDialog.taskAdded.connect(self.valueSaver)
        self.addClockDialog.taskAdded.connect(self.__init__)
        self.addClockDialog.taskAdded.connect(self.close)

        # 触发软件设置界面
        self.settingsDialog = settingsDialog(self)
        self.settingsBtn.clicked.connect(self.settingsDialog.exec_)

        # 触发软件说明界面
        self.info = infoDialog()
        self.infoBtn.clicked.connect(self.info.exec_)

        #关闭窗口前提示
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "提示", "确定要关闭JUICE么？", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def switchUI(self):
        if self.switchMode == True: #正在播放
            self.playButton.setVisible(False)
            self.pauseButton.setVisible(True)
        else: #正在停止
            self.pauseButton.setVisible(False)
            self.playButton.setVisible(True)

        self.switchMode = not self.switchMode

    def intoBreak(self):
        self.playButton.setVisible(False)
        self.pauseButton.setVisible(False)
        self.taskSelect.setVisible(False)

    def valueSaver(self):
        self.clockName = self.taskSelect.currentText()
        self.clockTime = self.taskDict[self.clockName]
        self.currentClockValue = self.clockName + "$" + self.clockTime
        file = open("config/clockValue.txt",'w')
        file.write(self.currentClockValue)
        file.close()

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
    taskAdded = pyqtSignal()

    def __init__(self, parent=None):
        super(addClockDialog,self).__init__(parent)
        self.move(600,200)
        self.setFixedSize(300,200)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("设置番茄钟")

        self.inputBox = QLineEdit()
        self.label1 = QLabel('<font color="#ff0000">*注意：如果番茄钟正在计时，\n'
                            '新增番茄钟会自动停止当前计时的番茄钟哟~\n')
        self.label2 = QLabel('*每个番茄钟的时长，请在"设置"中进行修改')
        self.label1.setWordWrap(True)
        self.label1.setFont(QFont("",12))
        self.label2.setFont(QFont("",12))
        self.acceptBtn = QPushButton("添加")
        self.rejectBtn = QPushButton("取消")

        grid = QGridLayout()
        grid.addWidget(self.inputBox,1,0,1,4)
        grid.addWidget(self.label1,2,0,1,4)
        grid.addWidget(self.label2,3,0,1,4)
        grid.addWidget(self.acceptBtn,4,3)
        grid.addWidget(self.rejectBtn,4,0)
        self.setLayout(grid)

        #按钮事件对应处理
        self.acceptBtn.clicked.connect(self.acceptAction)
        self.rejectBtn.clicked.connect(self.rejectAction)

    def acceptAction(self):
        newTaskName = self.inputBox.text()
        file = open("config/currentFocusTime.txt", "r")
        druationStr = file.readline()
        NewTask = newTaskName + "$" + druationStr
        file = open("config/FocusClockListFile.txt","r+")
        old = file.read()
        file.seek(0)
        file.write(NewTask)
        file.write(old)
        file.close()
        self.sendSignal()
        self.close()

    def rejectAction(self):
        self.close()

    def sendSignal(self):
        self.taskAdded.emit()

class settingsDialog(QDialog):
    changed = pyqtSignal()
    def __init__(self, parent=None):
        super(settingsDialog,self).__init__(parent)
        self.move(600, 200)
        self.setFixedSize(300, 300)
        self.initUI()

    def initUI(self):
        self.label = QLabel("<font color='#FF0000'>*设置会生效于下一个新建或启动的番茄钟。")
        self.label.setWordWrap(True)
        self.focusDruationLabel = QLabel("番茄钟时长：")
        self.breakDruationLabel = QLabel("休息钟时长：")
        self.focusBgmLabel = QLabel("番茄钟音效：")
        self.rejectBtn = QPushButton("取消")
        self.accpetBtn = QPushButton("确定")

        #create a drop box
        #create a timer list for focusDruationLabel and break label
        self.focusDruationList = ["15:00","20:00","25:00","30:00","35:00","40:00","45:00","50:00","55:00"]
        self.focusComboBox = QComboBox(self)
        self.focusComboBox.addItems(self.focusDruationList)
            #通过配置文件来设置默认值
        file = open("config/currentFocusTime.txt",'r')
        currentFocusTime = file.readline()
        file.close()
        timeStr1 = str(eval(currentFocusTime) // 60)
        currentFocusStr = timeStr1+":00"
        indexNum1 = self.focusDruationList.index(currentFocusStr)
        self.focusComboBox.setCurrentIndex(indexNum1)

        #通过配置文件来设置默认值
        self.breakDruationList = ["5:00","10:00","15:00"]
        self.breakComboBox = QComboBox(self)
        self.breakComboBox.addItems(self.breakDruationList)
        file = open("config/currentBreakTime.txt","r")
        currentBreakTime = file.readline()
        file.close()
        timeStr2 = str(eval(currentBreakTime) // 60)
        currentBreakStr = timeStr2+":00"
        indexNum2 = self.breakDruationList.index(currentBreakStr)
        self.breakComboBox.setCurrentIndex(indexNum2)

        #create a file name list for bgm label
        self.getFileName()
        self.focusBgmComboBox = QComboBox(self)
        self.focusBgmComboBox.addItems(self.fileNameList)
        file = open("config/currentBgm.txt","r")
        bgmName = file.readline()
        bgmName = bgmName.strip("\n")
        self.focusBgmComboBox.setCurrentText(bgmName)

        #页面布局
        grid = QGridLayout()
        grid.addWidget(self.focusDruationLabel,0,0)
        grid.addWidget(self.breakDruationLabel,1,0)
        grid.addWidget(self.focusBgmLabel,2,0)
        grid.addWidget(self.focusComboBox,0,1,1,3)
        grid.addWidget(self.breakComboBox,1,1,1,3)
        grid.addWidget(self.focusBgmComboBox,2,1,1,3)
        grid.addWidget(self.rejectBtn,3,0)
        grid.addWidget(self.accpetBtn,3,3)
        grid.addWidget(self.label,4,0,1,4)
        self.setLayout(grid)

        #create event and action
        self.accpetBtn.clicked.connect(self.accpetAction)
        self.rejectBtn.clicked.connect(self.rejectAction)


    def getFileName(self):
        self.fileNameList = []
        for self.file in os.listdir("./audio"):
            if self.file == ".DS_Store":
                continue
            else:
                self.fileNameList.append(self.file)

    def accpetAction(self):
        self.focusTimeStr = self.focusComboBox.currentText()
        self.breakTimeStr = self.breakComboBox.currentText()
        self.focusBgmStr = self.focusBgmComboBox.currentText()

        timeStr = self.focusTimeStr.split(":")
        self.focusTime = int(timeStr[0])*60 + int(timeStr[1])
        file = open("config/currentFocusTime.txt","w")
        file.seek(0,0)
        file.write(str(self.focusTime)+"\n")
        file.close()

        breakStr = self.breakTimeStr.split(":")
        self.breakTime = int(breakStr[0])*60 + int(breakStr[1])
        file = open("config/currentBreakTime.txt","w")
        file.seek(0,0)
        file.write(str(self.breakTime)+"\n")
        file.close()

        file = open("config/currentBgm.txt","w")
        file.seek(0,0)
        file.write(self.focusBgmStr+"\n")
        file.close()
        self.close()

        self.changed.emit()

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
        self.move(400,100)
        self.setFixedSize(600,800)
        self.initUI()

    def initUI(self):
        self.infoLabel = QLabel()
        self.infoLabel.setText('软件说明：\n\n'
                               '感谢您使用测试版本的JUICE。\n\n'
                               'JUICE是一个基于python与Qt5用户界面库实现的"番茄钟"demo，用来帮助您更专注于自己的工作和学习。\n\n'
                               '番茄钟，又称番茄工作法，是将自己每项工作拆解划分以"25分钟"为单位，全力专注一件事情，完成后彻底放松"5分钟"，'
                               '并思考自己所安排的工作是否合理、是否需要调整后续工作安排的，一种高效工作方法。\n'
                               '更多关注番茄钟、番茄工作法，可以阅读书籍《番茄工作法》\n\n'
                               '软件功能\n\n'
                               '- 生成番茄钟\n'
                               '点击屏幕右下角的"+"，您可以输入文字，创建一个新的番茄钟模板，如"开会"、"撰写文档"等。\n'
                               '默认的番茄钟为25分钟，休息15分钟。\n'
                               '*注意：当前版本尚未支持删除已经创建的番茄钟模板，请您避免创建过多（抱歉）\n'
                               '根据番茄工作法的原则，建议您使用默认设置。因为如果25分钟专注不能完成一项"工作"的话，那么很可能这项工作还可以继续拆解。\n'
                               '当然，现代社会中万恶的企业们在不断压榨我们，很有可能有一项工作确实无法在25分钟内完成（比如说我们的会议）。'
                               '这个时候您可以进行设置\n\n'
                               '- 设置番茄钟\n'
                               '点击屏幕左下方的"齿轮"，您可以对"后续"新创建的番茄钟进行设置。\n'
                               '设置项目包括，一个番茄钟的时长、每次休息的时长和工作时候番茄钟的背景音效。\n'
                               '*注意，这里的设置，都不会影响当前正在播放的番茄钟，影响的是完成选项后再新建或开启计时的番茄钟。\n\n'
                               '- 番茄钟的使用\n'
                               '创建好番茄钟后，您可以在屏幕中央的下拉菜单中选择对应工作的番茄钟。\n'
                               '选择好后，点击播放按钮，番茄钟开始计时；如果中途工作被打断，点击暂停按钮，番茄钟暂停计时。\n'
                               '一个番茄钟结束后，会自动进入到"休息钟"，休息时间无法暂停。\n'
                               '*注意：点击播放\暂停按钮下的"关闭"按钮，将会关闭当前运作中的番茄钟。\n\n\n'
                               '后续版本规划：\n'
                               '- 添加番茄钟删除功能。\n'
                               '- 增加统计功能，即统计一天工作中，您完成的番茄钟个数、工作内容分布和被打搅（番茄钟暂停）时长。\n'
                               '- 增加背景音乐静音功能。\n'
                               '- 自定义音乐的导入功能。\n'
                               '- 最小化到托盘功能。')
        self.infoLabel.setWordWrap(True)
        grid = QGridLayout(self)
        grid.addWidget(self.infoLabel,0,0,4,4)
        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tomato = TomatoWindow()
    sys.exit(app.exec_())
