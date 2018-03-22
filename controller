import xbox
import time
import math
import RPi.GPIO as GPIO

PIN = 18
PWMA1 = 6 
PWMA2 = 13
PWMB1 = 20
PWMB2 = 21
D1 = 12
D2 = 26

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

    
joy = xbox.Joystick()

print "Xbox controller sample: Press Back button to exit"
# Loop until back button is pressed


    
try:
    while not joy.Back():
        def set_motor(A1,A2,B1,B2):
            GPIO.output(PWMA1,A1)
            GPIO.output(PWMA2,A2)
            GPIO.output(PWMB1,B1)
            GPIO.output(PWMB2,B2)
        

        if(joy.leftY() > .2):
            set_motor(1,0,1,0)
            print "FORWARD 1 0 1 0"
        elif(joy.leftY() < -.2):
            set_motor(0,1,0,1)
            print "REVERSE 0 1 0 1"
        else:
            throttle = 0

        if(joy.rightX() > .2):
            set_motor(1,0,0,1)
            print "RIGHT 1 0 0 1"
        elif(joy.rightX() < -.2):
            set_motor(0,1,1,0)
            print "LEFT 0 1 1 0"
        else:
            turn = 0

        if(throttle == 0 and turn == 0):
            set_motor(0,0,0,0)
            print "STOP 0 0 0 0"
        #time.sleep(.1)
        print chr(13),
    joy.close()

finally:
    GPIO.cleanup()
