#!/usr/bin/python

import smbus
import math
import time
import RPi.GPIO as GPIO
import sys

from RPi import GPIO
from time import sleep

f = open("TestDisDawg.txt", "w+")

# Encoder variables
encoderA1 = 18
encoderB1 = 15
encoderA2 = 8
encoderB2 = 25

motorDir1 = 0
motorDir2 = 0

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68  # This is the address value read via the i2cdetect command

GPIO.setmode(GPIO.BCM)

GPIO.setup(encoderA1, GPIO.IN)
GPIO.setup(encoderB1, GPIO.IN)
GPIO.setup(encoderA2, GPIO.IN)
GPIO.setup(encoderB2, GPIO.IN)

GPIO.add_event_detect(encoderA1, GPIO.RISING)
GPIO.add_event_detect(encoderB1, GPIO.RISING)
GPIO.add_event_detect(encoderA2, GPIO.RISING)
GPIO.add_event_detect(encoderB2, GPIO.RISING)

# Global Variables this will modify
yrot = 0.0;

# Scaling Factor to level bot
makeMeLevelY = 6

# Controller Variables
A1 = 6  # M3
A2 = 13  # M4
B1 = 20  # M1
B2 = 21  # M2
D1 = 12  # PWMB
D2 = 26  # PWMA

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(A1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)
GPIO.setup(B1, GPIO.OUT)
GPIO.setup(B2, GPIO.OUT)
GPIO.setup(D1, GPIO.OUT)
GPIO.setup(D2, GPIO.OUT)

GPIO.output(A1, False)
GPIO.output(A2, False)
GPIO.output(B1, False)
GPIO.output(B2, False)

motor1 = GPIO.PWM(D1, 2000)
motor2 = GPIO.PWM(D2, 2000)
motor1.start(0)
motor2.start(0)

#Modify
DC = 0.0


def forward():
    GPIO.output(A1, True)
    GPIO.output(A2, False)
    GPIO.output(B1, False)
    GPIO.output(B2, True)
    motor1.ChangeDutyCycle(DC)
    motor2.ChangeDutyCycle(DC)


def reverse():
    GPIO.output(A1, False)
    GPIO.output(A2, True)
    GPIO.output(B1, True)
    GPIO.output(B2, False)
    motor1.ChangeDutyCycle(DC)
    motor2.ChangeDutyCycle(DC)


def stop():
    GPIO.output(A1, False)
    GPIO.output(A2, False)
    GPIO.output(B1, False)
    GPIO.output(B2, False)
    motor1.ChangeDutyCycle(0)
    motor2.ChangeDutyCycle(0)

def getDC():
    global DC
    if 1 <= yrot <= 1.5:
            DC = 92
    elif 1.5 < yrot <= 2:
            DC = 95
    elif 2 < yrot <= 3.5:
            DC = 98
    elif 3.5 < yrot <= 40:
            DC = 100
    elif 40 < yrot <= 50:
            DC = 100
    elif 50 < yrot <= 60:
            DC = 100
    elif 60 < yrot:
            DC = 0
    elif -1.25 >= yrot >= -1.5:
            DC = 70
    elif -1.5 > yrot >= -2:
            DC = 80
    elif -2 > yrot >= -3:
            DC = 95
    elif -3 > yrot >= -40:
            DC = 100
    elif -40 > yrot >= -50:
            DC = 100
    elif -50 > yrot >= -60:
            DC = 100
    elif yrot < -60:
            DC = 0
    else:
            DC = 0
    return

def getGyro():

    global yrot
    yrotI=yrot

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

    bus.write_byte_data(address, power_mgmt_1, 0)
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    xrot = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    yrot = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

    deltaY=yrotI-yrot
    if deltaY>.35:
        yrot = yrot + makeMeLevelY
    else: yrot-yrotI
    return

while True:

    start = time.time()

    getGyro()
    getDC()
		if 1<=yrot<=1.25:DC=90
		elif 1.25<yrot<=1.75:DC=92
		elif 1.75<yrot<=2.5:DC=94
		elif 2.5<yrot<=3:DC=100
		elif 3<yrot<=50:DC=100
		elif 50<yrot<=60:DC=100
		elif 60<yrot:DC=0
		elif -1.25>=yrot>=-1.5:DC=75
		elif -1.5>yrot>=-1.75: DC=82.5
		elif -1.75>yrot>=-2.5:DC=95
		elif -2.5>yrot>=-40:DC=100
		elif -40>yrot>=-50:DC=100
		elif -50>yrot>=-60:DC=100
		elif yrot<-60: DC=0
		else: DC=0
		return DC
   
    print(DC, yrot)
    time1 = time.time() - start
    f.write("%r, %r\r\n"%(DC,yrot))
    if yrot < 0:
        forward()
    elif yrot > 0:
        reverse()
    elif yrot == 0:
        stop()
f.close()
sys.end()
