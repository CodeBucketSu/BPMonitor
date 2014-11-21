# -*- coding: UTF-8 -*-

import sys
from functools import partial
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from EventButton import *
from BPRecordDialog import *


names = [u"开始测量", u"测量完成", \
         u"手臂上举", u"手臂平放", u"手臂下垂",\
         u"站起", u"坐下", u"其他事件"]
keyNames = ["StartMeasure", "FinishedMeasure", \
            "HandUp", "HandHoriz", "HandDown",\
            "StandUp", "SitDown", "OtherEvent"]
positions = [ (1, 0), (1, 1),\
        (3, 0), (3, 1), (3, 2),\
        (4, 0), (4, 1), 
        (5, 0) ]

class EventButtonsWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.qtobj = QObject()

        self.eventButtonGrid = QGridLayout()
        self.eventButtonGrid.addWidget(QLabel(u"血压测量"), 0, 0)
        self.eventButtonGrid.addWidget(QLabel(u"动作记录"), 2, 0)
        self.buttons = []
        for i, name in enumerate(names):
            button = EventButton(name, keyNames[i])
            button.setEnabled(False)
            self.eventButtonGrid.addWidget(button, positions[i][0], positions[i][1])
            func = partial(self.buttonClicked, keyNames[i])
            self.connect(button, SIGNAL("clicked()"), func)
            self.buttons.append(button)
        self.setLayout(self.eventButtonGrid)

    def startLogging(self):
        self.startTime = QDateTime.currentMSecsSinceEpoch()
        self.__enableButtons()

    def endLogging(self):
        self.startTime = None
        self.__disableButtons()



    def __enableButtons(self):
        for i, button in enumerate(self.buttons):
            if i is not 1:
                button.setEnabled(True)

    def __disableButtons(self):
        for i, button in enumerate(self.buttons):
            button.setEnabled(False)


    def buttonClicked(self, keyName):
        timeInterval = QDateTime.currentMSecsSinceEpoch() - self.startTime
        message = {"Event": keyName, "Time": timeInterval}
        if keyName is "StartMeasure":
            self.buttons[1].setEnabled(True)
            self.buttons[0].setEnabled(False)
        if keyName is "FinishedMeasure":
            dialog = BPRecordDialog(self)
            self.buttons[1].setEnabled(False)
            self.buttons[0].setEnabled(True)
            if dialog.exec_():
                message.update(dialog.getBP())
        self.qtobj.emit(SIGNAL("NewEvent"), message)



