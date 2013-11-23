'''
Blood Pressure Monitor 
version 1.0
Copyright 2013 SNARC_UCAS 
author: Frank Su
'''

import os
import platform
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from DataReceiver import *
from PlottingHelper import *
from DataHolder import *

from SerialSettingsDialog import *

__version__ = "1.0"

DT = 0.001
signalNames = ['energy', 'BP1', 'BP2', 'acc1_x', 'acc1_y', 'acc1_z',\
                'acc2_x', 'acc2_y', 'acc2_z', 'ecg']
BP_ECG_signal_names = {'BP1': ['BP1'], 'BP2': ['BP2'], 'ecg': ['ecg']}
ACC_signal_names = {'acc1': ['acc1_x', 'acc1_y', 'acc1_z'],\
                'acc2': ['acc2_x', 'acc2_y', 'acc2_z']}


class MainWindow(QMainWindow):
    ''' This is the main window of the BPMonitor.
    '''

    def __init__(self, parent=None):
        ''' This is the initializer of the main window
        '''
        super(MainWindow, self).__init__(parent)
        #=======================================
        # initial the member field
        #=======================================
        self.interval_in_seconds = 5
        self.q_time_elapsed = QTime(0, 0, 0, 0)

        # Data receiver
        self.data_receiver = DataReceiver()
        self.serial_settings = {"port":'Com8', "baud":115200, \
                                "bytesize":8, "parity":"N", \
                                "stopbits":1, "timeout":1}
        
        # Data holder
        self.data_holder = DataHolder()
        self.connect(self.data_receiver.qtobj, SIGNAL("NewData"),\
                     self.data_holder.on_receive_data)

        # Plot_helpers
        self.bp_ecg_plot_helper = PlottingHelper(self, \
        	                      BP_ECG_signal_names, 1000)
        self.acc_plot_helper = PlottingHelper(self, \
        	                      ACC_signal_names, 100)


        #=======================================
        # Set central widget
        #=======================================
        self.setWindowTitle('UCare BP Monitor')
        self.setWindowIcon(QIcon('icon/icon.png'))
        self.plotwidget = QWidget()
        self.vbox = QVBoxLayout()

        # Add plotting widget to the vbox
        for key, curve_plot in self.bp_ecg_plot_helper.curve_plots.items():
            self.vbox.addWidget(curve_plot)

        for key, curve_plot in self.acc_plot_helper.curve_plots.items():
            self.vbox.addWidget(curve_plot)

        self.plotwidget.setLayout(self.vbox)
        self.setCentralWidget(self.plotwidget)
        self.connect(self.data_holder.qtobj, SIGNAL("UpdateCurve"),\
                     self.update_curves)

        #=======================================
        # Set dock windows
        #=======================================
        #self.

        #=======================================
        # Set statusbar
        #=======================================
        self.statusbar = self.statusBar()
        self.label_time_elapsed = QLabel()
        self.label_time_elapsed.setText(self.q_time_elapsed.toString())
        self.statusbar.addPermanentWidget(self.label_time_elapsed)

        #=======================================
        # Set actions
        #=======================================
        # Open a file
        tip_text = 'Open an existing data file.'
        open_file_action = self.create_action('&Open a file', \
            self.open_file, QKeySequence.Open, 'icon\open.png',\
            tip_text, False)

        # Save the file
        tip_text = 'Save data into a file.'
        save_file_action = self.create_action('&Save into file', \
            self.save_file, QKeySequence.Save, 'icon\save.png',\
            tip_text, False)

        # Bluetooth settings
        tip_text = 'Settings of bluetooth.'
        bt_settings_action = self.create_action('&Bluetooth Settings',\
        	self.bt_settings, 'Ctrl+B', 'icon\settings.png',\
        	tip_text, False)

        # Plotting start
        tip_text = 'Start ploting the signals.'
        self.start_action = self.create_action('Start | &Continue plotting.',\
        	self.start_plot, 'Ctrl+C', 'icon\start.png', \
        	tip_text, True)

        # Plotting pause
        tip_text = 'Pause the plotting.'
        self.pause_action = self.create_action('&Pause the plotting.', \
        	self.pause_plot, 'Ctrl+P', 'icon\pause.png',\
        	tip_text, True)

        # Plotting stop
        tip_text = 'Stop the plotting.'
        self.stop_action = self.create_action('&End the plotting.', \
        	self.stop_plot, 'Ctrl+E', 'icon\stop.png',\
        	tip_text, True)

        # Set the plotting actions into a action group
        plot_group = QActionGroup(self)
        self.add_actions(plot_group, (self.start_action, self.pause_action, \
        					self.stop_action))

        # Scale the plotting


        #=============================================
        # Set the tool bar
        #=============================================
        # the file toolbar
        file_tool_bar = self.addToolBar("File")
        file_tool_bar.setObjectName("FileToolBar")
        self.add_actions(file_tool_bar, (open_file_action, \
                         save_file_action))

        # the bluetooth toolbar
        bt_tool_bar = self.addToolBar("Bluetooth")
        bt_tool_bar.setObjectName("Bluetooth")
        self.add_actions(bt_tool_bar, (bt_settings_action, ))

        # the plotting toolbar
        plot_tool_bar = self.addToolBar("Plotting")
        plot_tool_bar.setObjectName("Plotting")
        self.add_actions(plot_tool_bar, (self.start_action, self.pause_action, \
        					self.stop_action, None))

        self.scale_spinbox = QSpinBox()
        self.scale_spinbox.setRange(1, 50)
        self.scale_spinbox.setValue(5)
        self.scale_spinbox.setSuffix('s')
        scale_label = QLabel('Seconds to plot.')
        self.connect(self.scale_spinbox, SIGNAL('valueChanged(int)'), self.scale_changed)

        plot_tool_bar.addWidget(scale_label)
        plot_tool_bar.addWidget(self.scale_spinbox)

        #=============================================
        # Set the menu bar
        #=============================================
        # the file menu
        file_menu = self.menuBar().addMenu('&File')
        self.add_actions(file_menu, (open_file_action, save_file_action))

        # the bluetooth menu
        bt_menu = self.menuBar().addMenu('&Bluetooth')
        self.add_actions(bt_menu, (bt_settings_action, ))

    
    def add_actions(self, target, actions):
        '''helps add actions to the target, which is either a menubar or \
        a toolbar.'''
        for action in actions:
            if action is None:
        	    target.addSeparator()
            else:
                target.addAction(action)


    def update_curves(self):
        ''' update the curves'''
        if self.start_action.isChecked():
            self.bp_ecg_plot_helper.update_curves(self.data_holder.time_seq,\
                                        self.data_holder.signals, \
                                        self.interval_in_seconds)
            self.acc_plot_helper.update_curves(self.data_holder.time_seq\
                                [0:len(self.data_holder.time_seq):10],\
                                self.data_holder.signals, \
                                self.interval_in_seconds)

    def create_action(self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        '''This is a action_helper helps to create an action'''
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def open_file(self):
    	''' Open an existing data file'''
    	print 'MainWindow.open_file() was triggered.'

    def save_file(self):
    	''' Save the data received from bluetooth into a file'''
    	print 'MainWindow.save_file() was triggered.'

    def bt_settings(self):
    	''' Let user set the parameters of bluetooth connection.'''
    	print 'MainWindow.bt_settings() was triggered.'
        dialog = SerialSettingsDialog(self)
        if dialog.exec_():
            self.serial_settings = dialog.settings()
            print self.serial_settings
        
            if self.data_receiver.open(self.serial_settings):
                if self.data_receiver.serial.isOpen():
                    print 'Open serial successfully'
                    sleep(0.1)
                    self.data_receiver.start()
                    self.start_action.setChecked(True)
                else:
                    print "Serial port is not open."
            else:
                print "Unable to open serial port."


    def start_plot(self):
    	''' Start or restart plotting the signals.'''
    	print 'MainWindow.start_plot() was triggered.'

    def pause_plot(self):
    	''' Pause plotting the signals.'''
    	print 'MainWindow.pause_plot() was triggered.'

    def stop_plot(self):
    	''' Stop plotting the signals.'''
    	print 'MainWindow.start_plot() was triggered.'

    def scale_changed(self):
        ''' Update the scale factor.'''
        self.interval_in_seconds = self.scale_spinbox.value()
        print ' scale_spinbox triggered. Plot %d seconds.' \
                % self.interval_in_seconds




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    sys.exit(app.exec_())