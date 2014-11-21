'''
Blood Pressure Monitor 
version 1.0
Copyright 2013 SNARC_UCAS 
author: Frank Su
'''

from PyQt4.QtGui import *

class EventButton(QPushButton):
    
    def __init__(self, text, keyName, parent=None):
        QPushButton.__init__(self, text, parent)
        self.keyName = keyName

    def getKeyName():
        return self.keyName