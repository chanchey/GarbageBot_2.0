#!/usr/bin/python

import smbus
import math
import time

#Global Variables this will modify
yrot=0.0

#TimeStamp Constant
timestamp=0.0
i=0

#Open File 

f=open("testing.txt","w+")

#Scaling Factor to level bot 
makeMeLevelY=5.5

#Controller Variables 
# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import time, sys, tty, termios
A1 = 6	#M3
A2 = 13	#M4
B1 = 20	#M1
B2 = 21	#M2
D1 = 12	#PWMB
D2 = 26	#PWMA
#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(A1,GPIO.OUT)
GPIO.setup(A2,GPIO.OUT)
GPIO.setup(B1,GPIO.OUT)
GPIO.setup(B2,GPIO.OUT)
GPIO.setup(D1,GPIO.OUT)
GPIO.setup(D2,GPIO.OUT)
motor1 = GPIO.PWM(D1,500)
motor2 = GPIO.PWM(D2,500)
motor1.start(0)
motor2.start(0)
#motor1.ChangeDutyCycle(0)
#motor2.ChangeDutyCycle(0)

#Encoder Var
from RPi import GPIO
from time import sleep

#Encoder globals

Ae1 = 18	#GPIO18 encoder
Be1 = 15	#GPIO15 encoder
Ae2 = 	8	#GPIO08 encoder
Be2 = 25	#GPIO25 encoder


GPIO.setup(Ae1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Be1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Ae2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Be2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

encoderCounter1=0
encoderCounter2=0

clkLastState1 = GPIO.input(A1)
clkLastState2 = GPIO.input(A2)

#Ecoder Function 
def getEncoder1(count):
	clkLastState1 = GPIO.input(Ae1)

	clkState1 = GPIO.input(Ae1)
	dtState1 = GPIO.input(Be1)
                
	if clkState1 != clkLastState1:
		if dtState1 != clkState1:
			count += 1
		else:
			count -= 1	
	clkLastState1 = clkState1

	return count

def getEncoder2(count):
	clkLastState2 = GPIO.input(Ae2)

	clkState2 = GPIO.input(Ae2)
	dtState2 = GPIO.input(Be2)
                
	if clkState2 != clkLastState2:
		if dtState2 != clkState2:
			count += 1
		else:
			count -= 1                
	clkLastState2 = clkState2
		
	return count

#Controller Function 
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def forward():
        GPIO.output(A1, True)
        GPIO.output(A2, False)
        GPIO.output(B1, False)
        GPIO.output(B2, True)
def reverse():
        GPIO.output(A1, False)
        GPIO.output(A2, True)
        GPIO.output(B1, True)
        GPIO.output(B2, False)

def left():
        GPIO.output(A1, True)
        GPIO.output(A2, False)
        GPIO.output(B1, True)
        GPIO.output(B2, False)
        

def right():
        GPIO.output(A1, False)
        GPIO.output(A2, True)
        GPIO.output(B1, False)
        GPIO.output(B2, True)
        
#GPIO.output(A1, False)
#GPIO.output(A2, False)
#GPIO.output(B1, False)
#GPIO.output(B2, False)

#Gyro Function 
def getGyro ():

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

	def get_y_rotation(x,y,z):
		radians = math.atan2(x, dist(y,z))
		return -math.degrees(radians)

	def get_x_rotation(x,y,z):
		radians = math.atan2(y, dist(x,z))
		return math.degrees(radians)

	bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
	address = 0x68       # This is the address value read via the i2cdetect command

	# Now wake the 6050 up as it starts in sleep mode
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
	
	
	xrot= get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)  
	yrot= get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled) 
	
	yrot=yrot+makeMeLevelY
	
	return yrot

#While 
for i in range(600):
        char = getch()
        if char == "q":
                print 'Program Ended'
                break
        elif char == "w":
                forward()
                motor1.ChangeDutyCycle(65)
                motor2.ChangeDutyCycle(100)
	
	elif char == "s":
                reverse()
                motor1.ChangeDutyCycle(65)
                motor2.ChangeDutyCycle(100)
				                      
        elif char == "d":
                right()
                motor1.ChangeDutyCycle(65)
                motor2.ChangeDutyCycle(100)
                
        elif char == "a":
                left()
                motor1.ChangeDutyCycle(65)
                motor2.ChangeDutyCycle(100)
                
        time.sleep(.08)        
        motor1.ChangeDutyCycle(0)
        motor2.ChangeDutyCycle(0)
	timestamp=i*.001
	yrot=getGyro()
	encoderCounter1 = getEncoder1(encoderCounter1)
	encoderCounter2 = getEncoder2(encoderCounter2)
	f.write("Time:%.5r	Angle:%.5r	Key:%s	Encoder1:%r	Encoder2:%r \r\n " %(timestamp, yrot, char, encoderCounter1, encoderCounter2))
        if char == None:
		print 'nothing pressed'
GPIO.cleanup()
