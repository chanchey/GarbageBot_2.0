#!/usr/bin/python

import smbus
import math
import time
import RPi.GPIO as GPIO

from RPi import GPIO
from time import sleep

f=open("Test1Data.txt","w+")

#Encoder variables
encoderA1=18
encoderB1=15
encoderA2=8
encoderB2=25

GPIO.setmode(GPIO.BCM)

GPIO.setup(encoderA1, GPIO.IN)
GPIO.setup(encoderB1, GPIO.IN)
GPIO.setup(encoderA2, GPIO.IN)
GPIO.setup(encoderB2, GPIO.IN)

GPIO.add_event_detect(encoderA1,GPIO.BOTH)
GPIO.add_event_detect(encoderB1,GPIO.BOTH)
GPIO.add_event_detect(encoderA2,GPIO.BOTH)
GPIO.add_event_detect(encoderB2,GPIO.BOTH)

#Global Variables this will modify 
yrot=0.0; 

#Scaling Factor to level bot 
makeMeLevelY= 8

#Controller Variables 
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

GPIO.output(A1, False)
GPIO.output(A2, False)
GPIO.output(B1, False)
GPIO.output(B2, False)

motor1 = GPIO.PWM(D1,2000)
motor2 = GPIO.PWM(D2,2000)
motor1.start(0)
motor2.start(0)
DC=0.0


while True:
    
        start=time.time()
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

    
	#yrotSum=0.0
	#for i in range(2):
	#	yrotSum += getGyro()
		
	#yrot=yrotSum/2
        yrot=getGyro()
	def forward():
            GPIO.output(A1, True)
            GPIO.output(A2, False)
            GPIO.output(B1, False)
            GPIO.output(B2, True)
            motor1.ChangeDutyCycle(DC1)
            motor2.ChangeDutyCycle(DC1)
    
	
	def reverse():
        	GPIO.output(A1, False)
        	GPIO.output(A2, True)
        	GPIO.output(B1, True)
        	GPIO.output(B2, False)
        	motor1.ChangeDutyCycle(DC1)
        	motor2.ChangeDutyCycle(DC1)
	
	def getDC():
		if 2<=yrot<=10:DC=75
		elif 10<yrot<=20:DC=77
		elif 20<yrot<=30:DC=79.5
		elif 30<yrot<=40:DC=81
		elif 40<yrot<=50:DC=82
		elif 50<yrot<=60:DC=85 
		elif 60<yrot:DC=0
		elif -2>=yrot>=-10:DC=75
		elif -10>yrot>=-20: DC=77
		elif -20>yrot>=-30:DC=83
		elif -40>yrot>=-40:DC=84
		elif -40>yrot>=-50:DC=85
		elif -50>yrot>=-60:DC=86
		elif yrot<-60: DC=0
		
		else: DC=0
		return DC
	            
#    		if GPIO.event_detected(encoderA1) & GPIO.event_detected(encoderB1):
#	    		print "forward"
#   		elif GPIO.event_detected(encoderA1) < GPIO.event_detected(encoderB1):
#	    		print 'reverse'
#    		else: print 'motorA not moving'
#
#    		if GPIO.event_detected(encoderA2) < GPIO.event_detected(encoderB2):
#	    		print 'forward'
#    		elif GPIO.event_detected(encoderA2) > GPIO.event_detected(encoderB2):
#	    		print 'reverse'
#    		else: print 'motorB not moving'
	DC1=getDC()
	shitA1 = GPIO.event_detected(encoderA1)
	shitA2 = GPIO.event_detected(encoderA2)
	shitB1 = GPIO.event_detected(encoderB1)
	shitB2 = GPIO.event_detected(encoderB2)
	print (DC1,yrot,shitA1,shitA2,shitB1,shitB2)
	time1=time.time()-start
	f.write("DC1:%5r	yrot:%.5r	time:%.5r\r\n" %(DC1, yrot, time1))
	#f.write("PWM:%.5r	yrot:%.5r\r\n" %(DC1,yrot))
	if yrot <0: forward()
	else: reverse()
f.close()