import sys

filename = 'data/testFile.txt'
file = open(filename, 'a')
if not file:
	print 'unable to open'
else:
	file.write('\x00')
	file.close()