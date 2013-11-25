''' 
Blood Pressure Monitor 
version 1.0
Copyright 2013 SNARC_UCAS 
author: Frank Su
'''

import sys
from array import array
import numpy as np
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from guiqwt.plot import PlotManager, CurvePlot
from guiqwt.builder import make
from PyQt4.QtCore import QObject, SIGNAL
from time import sleep

from serial.tools import list_ports
import serial

from DataHolder import DataHolder
from MySerial import DataReceiver
from PlottingHelper import *


signalNames = ['energy', 'BP1', 'BP2', 'acc1_x', 'acc1_y', 'acc1_z',\
                'acc2_x', 'acc2_y', 'acc2_z', 'ecg']
BP_ECG_signal_names = {'BP1': ['BP1'], 'BP2': ['BP2'], 'ecg': ['ecg']}
ACC_signal_names = {'acc1': ['acc1_x', 'acc1_y', 'acc1_z'],\
                'acc2': ['acc2_x', 'acc2_y', 'acc2_z']}


DT = 0.001


class PlottingWindow(QWidget):
    """
    PlottingWindow is the class of the main window containing the 
    plottng curves
    """
    def __init__(self):
    	QMainWindow.__init__(self)
        # init the window for the app
        self.setWindowTitle('UCare Blood Pressure Monitor')
        #self.resize(640, 480)
        #self.statusBar().showMessage('There is nothing now.')
        self.setWindowIcon(QIcon('icon/icon.png'))
        # add a menu
        # add a toolbar

        # set the layout box for plotting
        vbox = QVBoxLayout()

        # initialize the plot_helpers
        self.bp_ecg_plot_helper = PlottingHelper(self, BP_ECG_signal_names, 1000)
        self.acc_plot_helper = PlottingHelper(self, ACC_signal_names, 100)
        for key, curve_plot in self.bp_ecg_plot_helper.curve_plots.items():
            vbox.addWidget(curve_plot)

        for key, curve_plot in self.acc_plot_helper.curve_plots.items():
            vbox.addWidget(curve_plot)

        self.setLayout(vbox)

        # the dataHolder
        self.data_holder = DataHolder()

        # the serial port controller
        self.data_receiver = DataReceiver()
        port = list_ports.comports()
        print port
        self.serial_settings = {"port":'Com8', "baud":115200, "bytesize":8,\
                                "parity":"N", "stopbits":1, "timeout":1}
        self.connect(self.data_receiver.qtobj, SIGNAL("NewData"),\
                     self.data_holder.on_receive_data)
        self.connect(self.data_holder.qtobj, SIGNAL("UpdateCurve"),\
                     self.update_curves)
        if self.data_receiver.open(self.serial_settings):
            print "successfully opened."
            sleep(0.1)
            self.data_receiver.start()

    def update_curves(self):
        ''' update the curves'''
        self.bp_ecg_plot_helper.update_curves(self.data_holder.time_seq, \
                                                self.data_holder.signals, 5)
        self.acc_plot_helper.update_curves(self.data_holder.time_seq\
                                [0:len(self.data_holder.time_seq):10], \
                                self.data_holder.signals, 5)

    def main():
        app = QApplication(sys.argv)
        main = PlottingWindow()
        main.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()