'''This is the test of serial'''
from serial import *

print type(PARITY_NONE), PARITY_NONE, ' ', PARITY_ODD, ' ', PARITY_EVEN, ' ', PARITY_MARK, ' ',\
	PARITY_SPACE
print type(STOPBITS_ONE), STOPBITS_ONE, ' ', STOPBITS_ONE_POINT_FIVE, ' ', STOPBITS_TWO
print type(FIVEBITS), FIVEBITS, ' ', SIXBITS, ' ', SEVENBITS, ' ', EIGHTBITS  