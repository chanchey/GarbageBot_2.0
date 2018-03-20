import xbox
import time
import math
import RPi.GPIO as GPIO

GPIO_A1 = 23
GPIO_A2 = 22
GPIO_B1 = 27
GPIO_B2 = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
GPIO.setup(GPIO_A1, GPIO.OUT)
GPIO.setup(GPIO_A2, GPIO.OUT)
GPIO.setup(GPIO_B1, GPIO.OUT)
GPIO.setup(GPIO_B2, GPIO.OUT)

# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)
    
joy = xbox.Joystick()

print "Xbox controller sample: Press Back button to exit"
# Loop until back button is pressed


    
try:
    while not joy.Back():
        def set_motor(A1,A2,B1,B2):
            GPIO.output(GPIO_A1,A1)
            GPIO.output(GPIO_A2,A2)
            GPIO.output(GPIO_B1,B1)
            GPIO.output(GPIO_B2,B2)

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
        time.sleep(.1)
        print chr(13),
    joy.close()

finally:
    GPIO.cleanup()
