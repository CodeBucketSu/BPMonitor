'''This is a class that helps write the signals received from 
bluetooth in to a file and read from already exsited file.'''

import sys
from PyQt4.QtCore import QDateTime
from PyQt4.QtGui import QFileDialog
import os

POSTFIX_FOR_SIGNAL = '.uSig'
POSTFIX_FOR_EVENT = '.uEvent'

class FileHelper():
	def __init__(self):
		self.signalFile = None
		self.eventFile = None
		filename = 'data/' + \
				QDateTime.currentDateTime().\
				toString('yyyy_MM_dd_hh_mm')
		self._fileName = str(filename)

	def getFileName(self):
		return self._fileName

	def isSignalFileOpen(self):
		''' return true whether signal file is open. '''
		if self.signalFile:
			return True
		else:
			return False

	def isEventFileOpen(self):
		''' return true whether event file is open. ''' 
		if self.eventFile:
			return True
		else:
			return False

	def openSignalFileToWrite(self, fileName=None):
		''' Open a file to write signals to. '''
		if fileName:
			self._fileName = fileName;

		if self.isSignalFileOpen():
			self.closeSignalFile();

		self.signalFile = open(self._fileName + POSTFIX_FOR_SIGNAL, 'ab', -1)

	def openEventFileToWrite(self, fileName=None):
		''' Open a file to write signals to. '''
		if fileName:
			self._fileName = fileName;

		if self.isEventFileOpen():
			self.closeEventFile();
			
		self.eventFile = open(self._fileName + POSTFIX_FOR_EVENT, 'ab', -1)

	def openFilesToWrite(self):
		''' Open files for signal and event. '''
		self.openSignalFileToWrite()
		self.openEventFileToWrite()


	def closeSignalFile(self):
		''' close the signal file. '''
		if self.isSignalFileOpen():
			self.signalFile.close()

	def closeEventFile(self):
		''' close the event file. '''
		if self.isEventFileOpen():
			self.eventFile.close()

	def closeFiles(self):
		''' close the files. '''
		self.closeSignalFile()
		self.closeEventFile()

	def writeToSignalFile(self, data):
		''' write signal data into signal file. '''
		self.signalFile.write(data)

	def writeToEventFile(self, event):
		''' write to event file. '''
		self.eventFile.write(event + '\n')



if __name__ == '__main__':

	fh = FileHelper()
	#print fh.isOpen()
	fh.openFileToWrite()
	raw_input()
	#print fh.isOpen()
	fh.writeToFile('\xff\xff\xff')
	fh.closeFile()