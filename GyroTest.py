#!/usr/bin/python
02
 
03
import smbus
04
import math
05
 
06
# Power management registers
07
power_mgmt_1 = 0x6b
08
power_mgmt_2 = 0x6c
09
 
10
def read_byte(adr):
11
    return bus.read_byte_data(address, adr)
12
 
13
def read_word(adr):
14
    high = bus.read_byte_data(address, adr)
15
    low = bus.read_byte_data(address, adr+1)
16
    val = (high << 8) + low
17
    return val
18
 
19
def read_word_2c(adr):
20
    val = read_word(adr)
21
    if (val >= 0x8000):
22
        return -((65535 - val) + 1)
23
    else:
24
        return val
25
 
26
def dist(a,b):
27
    return math.sqrt((a*a)+(b*b))
28
 
29
def get_y_rotation(x,y,z):
30
    radians = math.atan2(x, dist(y,z))
31
    return -math.degrees(radians)
32
 
33
def get_x_rotation(x,y,z):
34
    radians = math.atan2(y, dist(x,z))
35
    return math.degrees(radians)
36
 
37
bus = smbus.SMBus(0) # or bus = smbus.SMBus(1) for Revision 2 boards
38
address = 0x68       # This is the address value read via the i2cdetect command
39
 
40
# Now wake the 6050 up as it starts in sleep mode
41
bus.write_byte_data(address, power_mgmt_1, 0)
42
 
43
print "gyro data"
44
print "---------"
45
 
46
gyro_xout = read_word_2c(0x43)
47
gyro_yout = read_word_2c(0x45)
48
gyro_zout = read_word_2c(0x47)
49
 
50
print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
51
print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
52
print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)
53
 
54
print
55
print "accelerometer data"
56
print "------------------"
57
 
58
accel_xout = read_word_2c(0x3b)
59
accel_yout = read_word_2c(0x3d)
60
accel_zout = read_word_2c(0x3f)
61
 
62
accel_xout_scaled = accel_xout / 16384.0
63
accel_yout_scaled = accel_yout / 16384.0
64
accel_zout_scaled = accel_zout / 16384.0
65
 
66
print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
67
print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
68
print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
69
 
70
print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
71
print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
