'''This is a dialog for setting the Bluetooth parameters'''


from PyQt4.QtCore import *
from PyQt4.QtGui import *

from serial.tools import list_ports

baudrate_list = ['115200', '57600', '38400', \
				'19200', '9600', '4800', \
				'2400', '1800', '1200', '600',]
bytesize_list = ['8', '7', '6', '5']
parity_list= ['None', 'Odd', 'Even', 'Mark', 'Space']
stopbits_list = ['1', '1.5', '2'] 
comports_list = []

class SerialSettingsDialog(QDialog):
	'''
	This is the class for setting the serials ports' parameters.
	'''
	def __init__(self, parent=None):
		'''initialize the dialog with default settings.'''
		super(SerialSettingsDialog, self).__init__(parent)

		# Get comports available
		comports_list = [str(port[0]) for port in list_ports.comports()]
		self.serial_settings = {'port':comports_list[0],\
								'baud':baudrate_list[0],\
								'bytesize':bytesize_list[0],\
								'parity':parity_list[0],\
								'stopbits':stopbits_list[0],\
								'timeout':1} 

		# Initialize the widgets
		self.ports_combobox = self.create_combobox(comports_list)
		ports_label = QLabel('Comports')
		self.baud_combobox = self.create_combobox(baudrate_list)
		baud_label = QLabel('Baudrate')
		self.bytesize_combobox = self.create_combobox(bytesize_list)
		bytesize_label = QLabel('Bytesize')
		self.parity_combobox = self.create_combobox(parity_list)
		parity_label = QLabel('Parity')
		self.stopbits_combobox = self.create_combobox(stopbits_list)
		stopbits_label = QLabel('Stopbits')

		self.timeout_spinbox = QDoubleSpinBox()
		self.timeout_spinbox.setRange(0.00, 5.00)
		self.timeout_spinbox.setValue(1.00)
		timeout_label = QLabel('Timeout')

		button_box = QDialogButtonBox(QDialogButtonBox.Ok | \
									QDialogButtonBox.Cancel)

		# Set the layout
		grid = QGridLayout()
		grid.addWidget(ports_label, 0, 0)
		grid.addWidget(self.ports_combobox, 0, 1)
		grid.addWidget(baud_label, 1, 0)
		grid.addWidget(self.baud_combobox, 1, 1)
		grid.addWidget(bytesize_label, 2, 0)
		grid.addWidget(self.bytesize_combobox, 2, 1)
		grid.addWidget(parity_label, 3, 0)
		grid.addWidget(self.parity_combobox, 3, 1)
		grid.addWidget(stopbits_label, 4, 0)
		grid.addWidget(self.stopbits_combobox, 4, 1)
		grid.addWidget(timeout_label, 5, 0)
		grid.addWidget(self.timeout_spinbox, 5, 1)
		grid.addWidget(button_box, 6, 0, 1, 2)

		self.setLayout(grid)

		# Connect dialog's signals to slots
		self.connect(button_box, SIGNAL('accepted()'),\
					self, SLOT('accept()'))
		self.connect(button_box, SIGNAL('rejected()'),\
					self, SLOT('reject()'))
		self.setWindowTitle("Set Serial Parameters")


	def create_combobox(self, list):
		'''Helps create a combobox with the input list.'''
		combobox = QComboBox()
		combobox.addItems(list)
		return combobox

	def settings(self):
		'''After the dialog is accepted, the parent will call
		this method to obtain the settings.'''
		return self.serial_settings

	def accept(self):
		'''accepted slot'''
		self.serial_settings['port'] = str(self.ports_combobox.currentText())
		self.serial_settings['baud'], ok = self.baud_combobox.currentText()\
												.toInt()
		self.serial_settings['bytesize'], ok = self.bytesize_combobox\
												.currentText().toInt()
		self.serial_settings['parity'] = str(self.parity_combobox.currentText()\
												.__getitem__(0))
		self.serial_settings['stopbits'], ok = self.stopbits_combobox\
												.currentText().toInt()
		self.serial_settings['timeout'] = self.timeout_spinbox.value()
		QDialog.accept(self)
		



