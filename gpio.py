# import curses and GPIO
import curses
import RPi.GPIO as GPIO

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
p1 = GPIO.PWM(D1,500)
p2 = GPIO.PWM(D2,500)
p1.start(50)
p2.start(50)
# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

try:
        while True:   
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                GPIO.output(A1,1)
                GPIO.output(A2,0)
                GPIO.output(B1,1)
                GPIO.output(B2,0)
                
                screen.clear()
                
                
            elif char == curses.KEY_DOWN:
                GPIO.output(A1,0)
                GPIO.output(A2,1)
                GPIO.output(B1,0)
                GPIO.output(B2,1)
                
                screen.clear()
                
            elif char == curses.KEY_RIGHT:
                GPIO.output(A1,1)
                GPIO.output(A2,0)
                GPIO.output(B1,0)
                GPIO.output(B2,1)
                
                screen.clear()
                
            elif char == curses.KEY_LEFT:
                GPIO.output(A1,0)
                GPIO.output(A2,1)
                GPIO.output(B1,1)
                GPIO.output(B2,0)
                
                screen.clear()
                
            elif char == ord('s'):
                GPIO.output(A1,0)
                GPIO.output(A2,0)
                GPIO.output(B1,0)
                GPIO.output(B2,0)
                
                screen.clear()
             
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.output(A1,0)
    GPIO.output(A2,0)
    GPIO.output(B1,0)
    GPIO.output(B2,0)
    GPIO.cleanup()

