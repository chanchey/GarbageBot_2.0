import RPi.GPIO as GPIO
import time
  
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.IN)
GPIO.setup(40, GPIO.IN)
  
def rising_A(True):
  print 'rising_A'
def rising_B(True):
	print 'rising_B'
    
while (True):
	GPIO.add_event_detect(38, GPIO.RISING, callback=rising_A)
	GPIO.add_event_detect(40, GPIO.RISING, callback=rising_B)
    
GPIO.cleanup()
