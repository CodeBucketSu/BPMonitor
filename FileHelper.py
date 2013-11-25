'''This is a class that helps write the signals received from 
bluetooth in to a file and read from already exsited file.'''

import sys
from PyQt4.QtCore import QDateTime

class FileHelper():

	def __init__(self):
		self.file = None
		filename = 'data/' + \
				QDateTime.currentDateTime().\
				toString('yyyy_MM_dd_hh_mm')
		self._filename = str(filename)


	def openFileToWrite(self, filename=None):
		'''Open a file to write to.'''
		if filename:
			self._filename = filename
		self.file = open(self._filename, 'a', -1)

	def writeToFile(self, data):
		'''Write data into file.'''
		self.file.write(data)

	def closeFile(self):
		'''Close the file.'''
		self.file.close()

	def isOpen(self):
		'''return true if file is open.'''
		if self.file:
			return True
		else:
			return False

if __name__ == '__main__':
	fh = FileHelper()
	print fh.isOpen()
	fh.openFileToWrite()
	print fh.isOpen()