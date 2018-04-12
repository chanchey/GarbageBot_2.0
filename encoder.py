from RPi import GPIO
from time import sleep

#Encoder globals

Ae1 = 12	#GPIO18 encoder
Be1 = 10	#GPIO15 encoder
Ae2 = 24	#GPIO08 encoder
Be2 = 22	#GPIO25 encoder

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Ae1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Be1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Ae2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Be2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

encoderCounter1 = 0
encoderCounter2 = 0

def getEncoder():

	clkLastState1 = GPIO.input(Ae1)
	clkLastState2 = GPIO.input(Ae2)

	clkState1 = GPIO.input(Ae1)
	dtState1 = GPIO.input(Be1)
	clkState2 = GPIO.input(Ae2)
	dtState2 = GPIO.input(Be2)
                
	if clkState1 != clkLastState1:
		if dtState1 != clkState1:
			encoderCounter1 += 1
		else:
			encoderCounter1 -= 1
		return encoderCounter1
	if clkState2 != clkLastState2:
		if dtState2 != clkState2:
			encoderCounter2 += 1
		else:
			encoderCounter2 -= 1
		return encoderCounter2                
	clkLastState1 = clkState1
	clkLastState2 = clkState2
	sleep(0.01)
	return
getEncoder()
print("Motor1:%d Motor2:%d", %(encoderCounter1, encoderCounter2))
