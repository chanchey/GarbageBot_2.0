# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import time, sys, tty, termios
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
# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
#screen = curses.initscr()
#curses.noecho()
#curses.cbreak()
#screen.keypad(True)

def GetMove():
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

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


    char = getch()
    if char == "w":
        forward()
        motor1.ChangeDutyCycle(50)
        motor2.ChangeDutyCycle(80)


    elif char == "s":
        reverse()
        motor1.ChangeDutyCycle(99)
        motor2.ChangeDutyCycle(99)


    elif char == "d":
        right()
        motor1.ChangeDutyCycle(25)
        motor2.ChangeDutyCycle(25)

    elif char == "a":
        left()
        motor1.ChangeDutyCycle(75)
        motor2.ChangeDutyCycle(75)

    time.sleep(.1)
    motor1.ChangeDutyCycle(0)
    motor2.ChangeDutyCycle(0)
    char = ""
    return 
while True:
    GetMove()
