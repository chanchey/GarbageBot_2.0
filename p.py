#!/usr/bin/python
# import curses and GPIO
import curses
import time, sys, tty, termios
import smbus
import math
import RPi.GPIO as GPIO

f=open("Ptesting.txt","w+")
##ENCODER
##A1 = 12
##B1 = 10
##A2 = 24
##B2 = 22
##
##
##GPIO.setmode(GPIO.BOARD)
##GPIO.setup(A1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##GPIO.setup(B1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##GPIO.setup(A2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##GPIO.setup(B2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##
##counter1 = 0
##counter2 = 0
complexcounter = 0
##
##clkLastState1 = GPIO.input(A1)
##clkLastState2 = GPIO.input(A2)
##MOTOR
A1 = 6
A2 = 13
B1 = 20
B2 = 21
D1 = 12
D2 = 26
#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(A1,GPIO.OUT)
GPIO.setup(A2,GPIO.OUT)
GPIO.setup(B1,GPIO.OUT)
GPIO.setup(B2,GPIO.OUT)
GPIO.setup(D1,GPIO.OUT)
GPIO.setup(D2,GPIO.OUT)
motor1 = GPIO.PWM(D1,100)
motor2 = GPIO.PWM(D2,100)
motor1.start(0)
motor2.start(0)
motor1.ChangeDutyCycle(0)
motor2.ChangeDutyCycle(0)
##GYRO
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
gyrosum = 0
gyroaverage = 0
lastgyroaverage = 0
firstgyroaverage = 0
##PID
TIme = 0
DTE = 0
DTT = 0
end = 0
KP = 0
KI = 0
KD = 0
AP = .01
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
	
GPIO.output(A1, False)
GPIO.output(A2, False)
GPIO.output(B1, False)
GPIO.output(B2, False)

##PID
def PID(gyroaverage,lastgyroaverage,DTT,ITerm): ##,counter1,counter2
        if -1 < gyroaverage < 1 :
                KP = 10/2
                KI = 0
                KD = 0
        elif -3 < gyroaverage < 3 :
                KP = 10/1.5
                KI = 0
                KD = 0
        elif -9.99 < gyroaverage < 9.99 :
                KP = 10
                KI = 0
                KD = 0                
        else :
                KP = 0
                KI = 0
                KD = 0               
##        ITerm = Decay*ITerm + KI*gyroaverage##/DTT
	Lin = KP*gyroaverage + KD*(gyroaverage-lastgyroaverage)##ITerm +##*DTT
##	Ang = AP * (counter1-counter2)
	LeftWheel = Lin ##+ Ang/2
	RightWheel = Lin ##- Ang/2
	if 0 <= LeftWheel :
            if 0 <= RightWheel :
                reverse()
            else :
                left()
        else :
            if 0 <= RightWheel :
                right()
            else :
                forward()
        print("PWM: %r\r\n" %LeftWheel)
        f.write("PWM: %r\r\n" %LeftWheel)
        motor1.ChangeDutyCycle(math.fabs(LeftWheel))
        motor2.ChangeDutyCycle(math.fabs(RightWheel))
        
##        return ITerm
try:
    
    for num in range(1,50) :
        gyrosum += get_y_rotation()
    lastgyroaverage = gyroaverage
    firstgyroaverage = gyrosum/50
    print("y: %r" %firstgyroaverage)
    f.write("y: %r" %firstgyroaverage)
    gyroaverage = 0
    gyrosum = 0
    while True:              
        complexcounter += 1
##        clkState1 = GPIO.input(A1)
##        dtState1 = GPIO.input(B1)
##        clkState2 = GPIO.input(A2)
##        dtState2 = GPIO.input(B2)
        if end == 500:
            motor1.ChangeDutyCycle(0)
            motor2.ChangeDutyCycle(0)
            GPIO.cleanup()
            sys.exit()
            break
        if complexcounter == 1 :
            TIme = time.time()
##        if complexcounter == 501 :
##            DTE = time.time() - TIme
##            f.write("%r %r %r\n" %(counter1,counter2,DTE))
        if complexcounter <= 5 :
            gyrosum += get_y_rotation()
        if complexcounter == 6 :
            lastgyroaverage = gyroaverage 
            gyroaverage = gyrosum/5 - firstgyroaverage
            gyrosum = 0
            DTT = time.time() - TIme
            print("x: %r y: %r dt: %r\r\n" %(0, gyroaverage,DTT))
            f.write("x: %r y: %r dt: %r\r\n" %(0, gyroaverage,DTT))
            complexcounter = 0
            end+=1
            PID(gyroaverage,lastgyroaverage,DTT,ITerm) ##ITerm = ## ,counter1,counter2
            
##        if clkState1 != clkLastState1:
##            if dtState1 != clkState1:
##                counter1 += 1
##            else:
##                counter1 -= 1
##        if clkState2 != clkLastState2:
##            if dtState2 != clkState2:
##                counter2 += 1
##            else:
##                counter2 -= 1                
##        clkLastState1 = clkState1
##        clkLastState2 = clkState2
finally:
    GPIO.cleanup()
