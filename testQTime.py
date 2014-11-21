from PyQt4.QtCore import *
from PyQt4.QtGui import *


def OnTimer():
    print 'Get Timer'

timer=QTimer()
QObject.connect(timer,SIGNAL("timeout()"), OnTimer)
timer.start( 1000 )


