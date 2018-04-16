#!/usr/bin/python

import smbus
import math
import time
import RPi.GPIO as GPIO

#Global Variables this will modify 
yrot=0.0; 

#Scaling Factor to level bot 
makeMeLevelY=0 

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

motor1 = GPIO.PWM(D1,500)
motor2 = GPIO.PWM(D2,500)
motor1.start(0)
motor2.start(0)
DC=0.0

while True: 
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

	yrot1=getGyro() 
	yrot2=getGyro()
	yrot3=getGyro()
	yrot4=getGyro()
	yrot5=getGyro()

	yrot=(yrot1+yrot2+yrot3+yrot4+yrot5)/5

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
		theP=70;
		if 0<=yrot<=1:DC=theP+1
		elif 1<yrot<=2:DC=theP+2
		elif 2<yrot<=3:DC=theP+3
		elif 3<yrot<=4:DC=theP+4
		elif 4<yrot<=5:DC=theP+5
		elif 5<yrot<=6:DC=theP+6
		elif 6<yrot<=7:DC=theP+7
		elif 7<yrot<=8:DC=theP+8
		elif 8<yrot<=9:DC=theP+9
		elif 9<yrot<=10:DC=theP+10
		elif 10<yrot<=11:DC=theP+11
		elif 11<yrot<=12:DC=theP+12
		elif 12<yrot<=13:DC=theP+13
		elif 13<yrot<=14:DC=theP+14
		elif 14<yrot<=15:DC=theP+15
		elif 15<yrot<=16:DC=theP+16
		elif -0>yrot>=-1:DC=theP+1
		elif -1>yrot>=-2:DC=theP+2
		elif -2>yrot>=-3:DC=theP+3
		elif -3>yrot>=-4:DC=theP+4
		elif -4>yrot>=-5:DC=theP+5
		elif -5>yrot>=-6:DC=theP+6
		elif -6>yrot>=-7:DC=theP+7
		elif -7>yrot>=-8:DC=theP+8
		elif -8>yrot>=-9:DC=theP+9
		elif -9>yrot>=-10:DC=theP+10
		elif -10>yrot>=-11:DC=theP+11
		elif -11>yrot>=-12:DC=theP+12
		elif -12>yrot>=-13:DC=theP+13
		elif -13>yrot>=-14:DC=theP+14
		elif -14>yrot>=-15:DC=theP+15
		elif -15>yrot>=-16:DC=theP+16
			
		else: DC=0
		return DC 
	DC1=getDC()
	print (DC1,yrot)
	if yrot <0: forward()
	else: reverse()
	
