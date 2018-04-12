from RPi import GPIO
from time import sleep

A1 = 12
B1 = 10
A2 = 24
B2 = 22


GPIO.setmode(GPIO.BOARD)
GPIO.setup(A1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(A2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter1 = 0
counter2 = 0

clkLastState1 = GPIO.input(A1)
clkLastState2 = GPIO.input(A2)

try:
  
        while True:
                clkState1 = GPIO.input(A1)
                dtState1 = GPIO.input(B1)
                clkState2 = GPIO.input(A2)
                dtState2 = GPIO.input(B2)
                
                if clkState1 != clkLastState1:
                        if dtState1 != clkState1:
                                counter1 += 1
                        else:
                                counter1 -= 1
                        print counter1
                if clkState2 != clkLastState2:
                        if dtState2 != clkState2:
                                counter2 += 1
                          else:
                                counter2 -= 1
                        print counter2                
                clkLastState1 = clkState1
                clkLastState2 = clkState2
                sleep(0.01)
finish
        GPIO.cleanup()
