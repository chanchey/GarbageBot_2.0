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
		elif 16<yrot<=17:DC=theP+17
		elif 17<yrot<=18:DC=theP+18
		elif 18<yrot<=19:DC=theP+19
		elif 19<yrot<=20:DC=theP+20
		elif 20<yrot<=21:DC=theP+21
		elif 21<yrot<=22:DC=theP+22
		elif 22<yrot<=23:DC=theP+23
		elif 23<yrot<=24:DC=theP+24
		elif 24<yrot<=25:DC=theP+25
		elif 25<yrot<=26:DC=theP+26
		elif 26<yrot<=27:DC=theP+27
		elif 27<yrot<=28:DC=theP+28
		elif 28<yrot<=29:DC=theP+29
		elif 29<yrot<=30:DC=theP+30
		elif 30<yrot<=31:DC=theP+31
		elif 31<yrot<=32:DC=theP+32
		elif 32<yrot<=33:DC=theP+33
		elif 33<yrot<=34:DC=theP+34
		elif 34<yrot<=35:DC=theP+35
		elif 35<yrot<=36:DC=theP+36
		elif 36<yrot<=37:DC=theP+37
		elif 37<yrot<=38:DC=theP+38
		elif 38<yrot<=39:DC=theP+39
		elif 39<yrot<=40:DC=theP+40
		elif 40<yrot<=41:DC=theP+41
		elif 41<yrot<=42:DC=theP+42
		elif 42<yrot<=43:DC=theP+43
		elif 43<yrot<=44:DC=theP+44
		elif 44<yrot<=45:DC=theP+45
		elif 45<yrot<=46:DC=theP+46
		elif 46<yrot<=47:DC=theP+47
		elif 47<yrot<=48:DC=theP+48
		elif 48<yrot<=49:DC=theP+49
		elif 49<yrot<=50:DC=theP+50
			
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
		elif -16>yrot>=-17:DC=theP+17
		elif -17>yrot>=-18:DC=theP+18
		elif -18>yrot>=-19:DC=theP+19
		elif -19>yrot>=-20:DC=theP+20
		elif -20>yrot>=-21:DC=theP+21
		elif -21>yrot>=-22:DC=theP+22
		elif -22>yrot>=-23:DC=theP+23
		elif -23>yrot>=-24:DC=theP+24
		elif -24>yrot>=-25:DC=theP+25
		elif -25>yrot>=-26:DC=theP+26
		elif -26>yrot>=-27:DC=theP+27
		elif -27>yrot>=-28:DC=theP+28
		elif -28>yrot>=-29:DC=theP+29
		elif -29>yrot>=-30:DC=theP+30
		elif -30>yrot>=-31:DC=theP+31
		elif -31>yrot>=-32:DC=theP+32
		elif -32>yrot>=-33:DC=theP+33
		elif -33>yrot>=-34:DC=theP+34
		elif -34>yrot>=-35:DC=theP+35
		elif -35>yrot>=-16:DC=theP+35
		elif -36>yrot>=-16:DC=theP+36
			
		else: DC=0
		return DC 
	DC1=getDC()
	print (DC1,yrot)
	if yrot <0: forward()
	else: reverse()
	
