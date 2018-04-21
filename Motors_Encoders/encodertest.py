import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Encoder variables
encoderA1=18
encoderB1=15
encoderA2=8
encoderB2=25

a1counter=0
a2counter=0

olda1c = 0
olda2c = 0
a1c = 0
b1c = 0
a2c = 0
b2c = 0
direction1 = 0
direction2 = 0

#Controller Variables 
A1 = 6	#M3
A2 = 13	#M4
B1 = 20	#M1
B2 = 21	#M2
D1 = 12	#PWMB
D2 = 26	#PWMA

#set GPIO numbering mode and define output pins

GPIO.setup(encoderA1, GPIO.IN)
GPIO.setup(encoderB1, GPIO.IN)
GPIO.setup(encoderA2, GPIO.IN)
GPIO.setup(encoderB2, GPIO.IN)

GPIO.setup(A1,GPIO.OUT)
GPIO.setup(A2,GPIO.OUT)
GPIO.setup(B1,GPIO.OUT)
GPIO.setup(B2,GPIO.OUT)
GPIO.setup(D1,GPIO.OUT)
GPIO.setup(D2,GPIO.OUT)

motor1 = GPIO.PWM(D1,2000)
motor2 = GPIO.PWM(D2,2000)
motor1.start(0)
motor2.start(0)
DC=100

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

def A1count(encoderA1):
        a1cT = a1c + 1
        if (GPIO.input(encoderB1)):
            direction1 = 0
        else:
            direction1 = 1  
     
def A2count(encoderA1):
        a2c = a2c + 1
        if (GPIO.input(encoderB2)):
            direction2 = 0
        else:
            direction2 = 1
       
GPIO.add_event_detect(encoderA1,GPIO.RISING, callback=A1count)
#GPIO.add_event_detect(encoderB1,GPIO.RISING)
GPIO.add_event_detect(encoderA2,GPIO.RISING, callback=A2count)
#GPIO.add_event_detect(encoderB2,GPIO.RISING, callback=B2count)


while(True):

        time.sleep(.1)
        print("count1 = {}, direction1 = {}".format(a1c, direction1))
        print("count2 = {}, direction2 = {}".format(a2c, direction2))

        diff = a1c - olda1c
        speed = diff / .1
        olda1c = a1c
        forward()
