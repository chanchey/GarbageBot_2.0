# !/usr/bin/python

import threadingTest
import smbus
import math
import time
from threading import Thread



t1=Thread(target=getGyro)
t1.start()

while True:
    print("Yrotation: %r"%yrot)
    f.write("Yrotation: %r\r\n"%yrot)
