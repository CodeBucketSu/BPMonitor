class EcgHelper():
    '''
    EcgHelper implement all the ecg signal processing algorithms such as peak
    detection, heart rate calculation, etc.
    '''

    def computeHeartRate(self, ecg):
        ''' 
        Compute heart rate from ecg signal.
        Return a 2 * N array in which N is the number of cardiac cycle: 
            the 1st row is the position of the R wave peak of each cardiac cycle;
            the 2nd row is the heart rate of the corresponding cardiac cycle.
        '''
        return 

    def detectRpeaks(self, ecg):
        '''
        Locate all the R peaks' position from the ecg signal.
        Return a 1 * N array in which N is the number of cardiac cycle: 
            the 1st row is the position of the R wave peak of each cardiac cycle. 
        '''
        return 

    def computeHeartRate(self, peaks):
        '''
        Compute the heart rate from previous detected R peaks.
        '''
        return 