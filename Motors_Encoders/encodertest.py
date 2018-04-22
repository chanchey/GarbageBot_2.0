import time
import RPi.GPIO as GPIO

f=open("encoder.txt","w+")

GPIO.setmode(GPIO.BOARD) ##Physical pins
GPIO.setwarnings(False)

#Encoder variables
encoderA1=38 ## Physical pins - channel A
encoderB1=40 ## Physical pins - channel B
olda1c = 0
a1c = 0
direction1 = 'X' ## Neither forward or backward
diff=0

GPIO.setup(encoderA1, GPIO.IN) ## normal polarity at motors
GPIO.setup(encoderB1, GPIO.IN)

def A1count(encoderA1):
        global a1c, direction1
        
        if GPIO.input(encoderB1): ## B1 leading A1
            direction1 = 'Rev' ## CCW
            a1c -= 1
        else:
            direction1 = 'Fwd' ## CW
            a1c += 1

## Always looking for encoderA1 rising edge
GPIO.add_event_detect(encoderA1,GPIO.RISING,callback=A1count)

while(True):
    
    direction1 = 'X'
    diff = a1c - olda1c
    speed = diff /.1
    olda1c = a1c
    time.sleep(.1)
    print("countA1 = {}, direction1 = {}, speed = {}".format(a1c, direction1, speed))
    f.write("countA1:%.6r direction1:%.5r speed:%.5r\r\n" %(a1c, direction1, speed))

GPIO.cleanup()
