# !/usr/bin/python

import smbus
import math
import time
from threading import Thread
# Scaling Factor to level bot
makeMeLevelY = 0.0

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Open Test File for Writing to excel

f = open("testing1.csv", "w+")

# Set Time to see total time
ptime=0.0
rtime=0.0


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


bus = smbus.SMBus(1)
address = 0x68  # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)


def getGyro():
    global yrot, ptime
    while True:
        sptime=time.time()
        starttime = time.time()
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)

        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        yrot = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        etime = time.time()
        ptime = etime - sptime
    return

def getTime():
    global rtime
    iStart=time.time()
    while rtime<30:    
        rtime=time.time()-iStart
        print ("Time Elapsed: %r"%rtime)
        time.sleep(1)
    return 

t1=Thread(target=getGyro)
t2=Thread(target=getTime)
t1.start()
t2.start()
while rtime<30:
    f.write("%r, %r, %r\r\n" %(yrot,ptime,rtime))

t1.exit()
t2.exit()


