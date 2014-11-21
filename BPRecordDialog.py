# -*- coding: UTF-8 -*-

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class BPRecordDialog(QDialog):

    def __init__(self, parent=None):
        super(BPRecordDialog, self).__init__(parent)
        self.setWindowTitle(u"请输入血压值")

        # 收缩压
        self.systolicPressureEdit = QLineEdit()
        # 舒张压
        self.diastolicPressureEdit = QLineEdit()
        validator = QIntValidator(0, 500, self)
        self.systolicPressureEdit.setValidator(validator)
        self.diastolicPressureEdit.setValidator(validator)

        vbox = QVBoxLayout()
        # 收缩压
        widget1 = QWidget()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel(u"收缩压"))
        hbox1.addWidget(self.systolicPressureEdit)
        hbox1.addWidget(QLabel('mmHg'))
        widget1.setLayout(hbox1)
        # 舒张压
        widget2 = QWidget()
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel(u"舒张压"))
        hbox2.addWidget(self.diastolicPressureEdit)
        hbox2.addWidget(QLabel('mmHg'))
        widget2.setLayout(hbox2)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | 
                                    QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        vbox.addWidget(widget1)
        vbox.addWidget(widget2)
        vbox.addWidget(buttonBox)

        self.setLayout(vbox)

        self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

        


    def accept(self):
        self.record = {"BPsys": str(self.systolicPressureEdit.text()), 
                        "BPdia": str(self.diastolicPressureEdit.text())}
        QDialog.accept(self)

    def getBP(self):
        return self.record

