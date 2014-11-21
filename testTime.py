from datetime import *
from time import *

start = datetime.now()
sleep(2)
end = datetime.now()
interval = end - start
print start
print end
print interval
print interval.seconds
print interval.microseconds



