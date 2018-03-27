#!/usr/bin/python
import smbus
import math
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
#Define Functions for Reading and Writing 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
  
#Loop that Will Run Continuous 
while True:
    bus = smbus.SMBus(1) # bus 
    address = 0x6b      # via i2cdetect
 
# Activate to be able to address the module
    bus.write_byte_data(address, power_mgmt_1, 1)
 

 
    gyroskop_xout = read_word_2c(0x29)
    gyroskop_yout = read_word_2c(0x2b)
    gyroskop_zout = read_word_2c(0x2d)
 
    print "X: ", ("%5d" % gyroskop_xout),"Y: ", ("%5d" % gyroskop_yout), "Z: ", ("%5d" % gyroskop_zout)
