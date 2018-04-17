#!/usr/bin/python

import smbus
import math
import RPi.GPIO as GPIO
import time

f=open("EGtesting.txt","w+")
##ENCODER
A1 = 12
B1 = 10
A2 = 24
B2 = 22


GPIO.setmode(GPIO.BOARD)
GPIO.setup(A1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(A2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

counter1 = 0
counter2 = 0
complexcounter = 0

clkLastState1 = GPIO.input(A1)
clkLastState2 = GPIO.input(A2)

##MOTOR
PIN = 18
PWMA1 = 6 
PWMA2 = 13
PWMB1 = 20
PWMB2 = 21
D1 = 12
D2 = 26
motor1_in1_pin = 6	
motor1_in2_pin = 13

PWM = 50

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(PWMA1,GPIO.OUT)
GPIO.setup(PWMA2,GPIO.OUT)
GPIO.setup(PWMB1,GPIO.OUT)
GPIO.setup(PWMB2,GPIO.OUT)
GPIO.setup(D1,GPIO.OUT)
GPIO.setup(D2,GPIO.OUT)
p1 = GPIO.PWM(D1,500)
p2 = GPIO.PWM(D2,500)
p1.start(50)
p2.start(50)
##GYRO
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
gyrosum = 0
gyroaverage = 0
##PID
TIme = 0
DTE = 0
DTT = 0
end = 0
KP = 0
KI = 0
KD = 0
AP = 0
ITerm = 0
Decay = .9

##GYRO
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

##MOTOR
def set_motor(a1,a2,b1,b2):
	GPIO.output(PWMA1,a1)
	GPIO.output(PWMA2,a2)
	GPIO.output(PWMB1,b1)
	GPIO.output(PWMB2,b2)

def forward():
	GPIO.output(PWMA1,1)
	GPIO.output(PWMA2,0)
	GPIO.output(PWMB1,1)
	GPIO.output(PWMB2,0)
def reverse():
	GPIO.output(PWMA1,0)
	GPIO.output(PWMA2,1)
	GPIO.output(PWMB1,0)
	GPIO.output(PWMB2,1) 
	
	
def stop():
	set_motor(0.5,0.5,0.5,0.5)

def reverse():
	set_motor(0,1,0,1)

def right():
	set_motor(1,0,0,1)

def left():
	set_motor(0,1,1,0)

##PID
def PID(gyroaverage,lastgyroaverage,DTT,counter1,counter2):
        if -1 < gyroaverage < 1 :
                KP = 5
                KI = 0
                KD = 0
        elif -3 < gyroaverage < 3 :
                KP = 100/15
                KI = 0
                KD = 0
        else :
                KP = 10
                KI = 0
                KD = 0               
        ITerm = Decay*ITerm + KI*gyroaverage/DTT
	Lin = KP*gyroaverage + ITerm + KD*(gyroaverage-lastgyroaverage)*DTT
	Ang = AP * (counter1-counter2)
	A = Lin + Ang/2
	B = 1 - A
	C = Lin - Ang/2
	D = 1 - C
	set_motor(A,B,C,D)
try:
    stop()
    for num in range(1,50) :
        gyrosum += get_y_rotation()
        lastgyroaverage = gyroaverage
        gyroaverage = gyrosum/50
        gyrosum = 0
    while True:
                
        complexcounter += 1
        clkState1 = GPIO.input(A1)
        dtState1 = GPIO.input(B1)
        clkState2 = GPIO.input(A2)
        dtState2 = GPIO.input(B2)
        if end = 10:
            stop()
            break
        if complexcounter == 1 :
            TIme = time.time()
        if complexcounter == 550 :
            DTE = time.time() - TIme
            f.write("%r %r %r\n" %(counter1,counter2,DTE))
        if 550 < complexcounter <= 600 :
            gyrosum += get_y_rotation()
        if complexcounter == 601 :
            lastgyroaverage = gyroaverage
            gyroaverage = gyrosum/50
            gyrosum = 0
            DTT = time.time() - TIme
            f.write("x: %r y: %r dt: %r\r\n" %(0, gyroaverage,DTT))
            complexcounter = 0
            end+=1
##            PID(gyroaverage,lastgyroaverage,DTT,counter1,counter2)
            
        if clkState1 != clkLastState1:
            if dtState1 != clkState1:
                counter1 += 1
            else:
                counter1 -= 1
        if clkState2 != clkLastState2:
            if dtState2 != clkState2:
                counter2 += 1
            else:
                counter2 -= 1                
        clkLastState1 = clkState1
        clkLastState2 = clkState2
finally:
    GPIO.cleanup()
