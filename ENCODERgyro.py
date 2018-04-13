from RPi import GPIO
#!/usr/bin/python

import smbus
import math
import time

f=open("EGtesting.txt","w+")

A1 = 12
B1 = 10
A2 = 24
B2 = 22


GPIO.setmode(GPIO.BOARD)
GPIO.setup(A1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(A2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation():
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)
    
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
    radians = math.atan2(accel_xout_scaled, dist(accel_yout_scaled,accel_zout_scaled))
    return -math.degrees(radians)

def get_x_rotation():
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)
    
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
    radians = math.atan2(accel_yout_scaled, dist(accel_yout_scaled,accel_zout_scaled))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)


counter1 = 0
counter2 = 0
complexcounter = 0
gyrosum = 0
gyroaverage = 0

clkLastState1 = GPIO.input(A1)
clkLastState2 = GPIO.input(A2)

try:
          
          while True:
                complexcounter += 1
                clkState1 = GPIO.input(A1)
                dtState1 = GPIO.input(B1)
                clkState2 = GPIO.input(A2)
                dtState2 = GPIO.input(B2)  
                if 550 < complexcounter <= 600 :
                        gyrosum += get_y_rotation()
                if complexcounter == 601 :
                        gyroaverage = gyrosum/50
                        gyrosum = 0
                        f.write("x: %r" , get_x_rotation(),  "y: %r" , gyroaverage, "\r\n")
                if complexcounter == 5001 :
                        complexcounter -= 5001
                if clkState1 != clkLastState1:
                        if dtState1 != clkState1:
                                counter1 += 1
                        else:
                                counter1 -= 1
                        f.write(counter1 "\n")
                if clkState2 != clkLastState2:
                        if dtState2 != clkState2:
                                counter2 += 1
                        else:
                                counter2 -= 1
                        f.write(counter2 "\n")                
                clkLastState1 = clkState1
                clkLastState2 = clkState2
finally:
          GPIO.cleanup()
