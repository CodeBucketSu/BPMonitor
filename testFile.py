import sys
import os

filename = 'data/testFile1.txt'
file = open(filename, 'a')
message = {"Event": 'keyName', "Time": 123123123123123}
print message
file.write(str(message)+'\n')
file.write(str(message)+'\n')

file.close()
newFileName = 'data/testDir/movedFile'
(dir, name) = os.path.split(newFileName)
os.mkdir(dir)
os.rename(filename, newFileName)