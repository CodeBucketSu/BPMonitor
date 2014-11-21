class BpHelper():
    '''BpHelper is responsible for calibraion and blood pressure calculation.'''

    def calibrate(self, ecg, ppg, measurements, formula):
        '''
        Calibrate the parameters of the relationship bwtween PWTT and BP.
        Input:
            ecg: ecg signal;
            ppg: ppg signal;
            measurements: an array of measurement events;
            formula: the formula of the relationship.
        Return: 
            the array of parameters.
        '''
        return 

    def calibrate(self, pwtt, bp, formula):
        '''
        Calibrate the parameters of the relationship bwtween PWTT and BP.
        Input:
            pwtt: pwtt calcutated before.
            bp: bp extract from measurement events.
            formula: the formula of the relationship.
        Return: 
            the array of parameters.
        '''
        return 