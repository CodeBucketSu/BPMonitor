''' This is the class to receive and unpack the data
received from serial port'''

import sys
from array import array
import numpy as np
from struct import *
from PyQt4.QtCore import QObject, SIGNAL


fmt = '<196h'
signalNames = ['energy', 'BP1', 'BP2', 'acc1_x', 'acc1_y', 'acc1_z',\
                'acc2_x', 'acc2_y', 'acc2_z', 'ecg']
offsetDict = {'energy':13, 'BP1':14, 'BP2':64, \
                'acc1_x':114, 'acc1_y':119, 'acc1_z':124,\
                'acc2_x':129, 'acc2_y':134, 'acc2_z':139,\
                'ecg':144}
lengthDict = {'energy':1, 'BP1':50, 'BP2':50, \
                'acc1_x':5, 'acc1_y':5, 'acc1_z':5,\
                'acc2_x':5, 'acc2_y':5, 'acc2_z':5,\
                'ecg':50}



class DataHolder(object):
    '''This is the class responsible for unpacking and the storage
    of the data received from serial port'''
    def __init__(self):
        ''' Initialzation work.'''

        # New raw data received from serial which can be incomplete.
        self.new_raw_data = ''

        # Current raw data that has not been processed.
        # Make sure all the packages contained in self.curr_raw_data
        # are complete except the last one.
        # Though it may contain debug messages which should end with 
        # '\n'.
        self.curr_raw_data = ''	

        # All of the package received from serial.
        self.all_packages = []
        self.num_packages = 0

        # Signals unpack from the packages
        self.signals = {}
        for sigName in signalNames:
            self.signals[sigName] = array('l')

        # The time sequence.
        self.time_seq = array('f')
        self.curr_time = 0.0

        # Object to emit a signal
        self.qtobj = QObject()


    def __form_curr_data(self):
        ''' Join self.new_raw_data to self.last_segment_raw_data
        to form self.curr_raw_data.'''
        self.curr_raw_data = self.curr_raw_data + \
        						self.new_raw_data

    def __split_curr_data(self):
        ''' Extract complete packages from self.curr_raw_data and add
        them into self.packages.
        Extract debug messages and print them.
        '''
        while True:
            '''In this while loop, we only process the start part of 
            self.curr_raw_data.'''

            #print 'len(curr_data) = ', len(self.curr_raw_data)
            if len(self.curr_raw_data) < 4:
                #print "*** len < 4: break. ***"
                break

            # Judge whether there is package contained in 
            # self.curr_raw_data.
            try:
                idx_start_package = self.curr_raw_data.index\
                                           ('\xff\xff\xff\xff')
            except ValueError:
                # No start flag exists! This is a debug message, let's
                # print it! However, maybe there is an incomplete start
                # flag in the end of self.curr_raw_data, so let's keep 
                # the last 3 bytes.
                #print '### no package start flag! ###'
                print self.curr_raw_data
                self.curr_raw_data = self.curr_raw_data[-3:-1]
                break
            
            #print '    idx = ', idx_start_package
            # We're here because there do exists a start flag!
            if idx_start_package > 0:
                if idx_start_package > 3:
                    #print '    **** idx > 3 ****'
                	# There is debug messages before the first package.
                    #print self.curr_raw_data[3:idx_start_package]
                    self.curr_raw_data = self.curr_raw_data\
                    						[idx_start_package:]
                    continue

                else:
                    #print '    *** 0 < idx <= 3 ***'
                    # There is no debug messages at the beginning.
                    self.curr_raw_data = self.curr_raw_data\
                    						[idx_start_package:]
                    continue

            # We're here because self.curr_raw_data starts with a 
            # complete start flag.
            # Let's see whether there is enough space for a complete 
            # package. 
            if len(self.curr_raw_data) < 392:
                #print '    *** len < 392: break ***'
                break

            else:
                #print '    *** len > 392 ***'
                # There may be a complete package, but we can't be sure.
                if self.curr_raw_data[388:392] == '\xf0\xf0\xf0\xf0':
                    # Congratulations! Here is the package!
                    #print '    *** find a package!! ***'
                    self.all_packages.append(self.curr_raw_data[:392])
                    self.curr_raw_data = self.curr_raw_data[392:]
                    continue

                else:
                    #Oops! Still no complete pacakge at the beginning!
                    self.curr_raw_data = self.curr_raw_data[1:]
                    continue        

    def __unpack_a_package_into_signals(self, raw_data):
        ''' Unpack a complete package into self.signals.'''
        #print "DataHolder: unpack a package"
        data = list(unpack(fmt, raw_data))
        #print '    package: ', data[0:12]
        for sig in signalNames:
            self.signals[sig].extend(data[offsetDict[sig] : \
                            offsetDict[sig]+lengthDict[sig]])
        self.time_seq.extend(np.linspace(0.001, 0.05, 50) + self.curr_time)
        self.curr_time += 0.05
        #print '    curr_time = ', self.curr_time
        #print '    len(BP1) = ', len(self.signals['BP1'])
        #print '    len(acc1_x) = ', len(self.signals['acc1_x'])
        #print '    len(time)  = ', len(self.time_seq)

    def on_receive_data(self, new_data):
        ''' Do the whole job every time a piece of new data arrives.
        Extract signals from input data and print debug messages if 
        there exist any.'''
        self.new_raw_data = new_data
        self.__form_curr_data()
        self.__split_curr_data()
        for package in self.all_packages[self.num_packages:\
                                        len(self.all_packages)]:
            self.__unpack_a_package_into_signals(package)
            self.qtobj.emit(SIGNAL("UpdateCurve"))
        self.num_packages = len(self.all_packages)
        #print '    num_packages = ', self.num_packages


