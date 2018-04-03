# import curses and GPIO
import curses
import RPi.GPIO as GPIO

A1 = 6
A2 = 13
B1 = 20
B2 = 21
#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(A1,GPIO.OUT)
GPIO.setup(A2,GPIO.OUT)
GPIO.setup(B1,GPIO.OUT)
GPIO.setup(B2,GPIO.OUT)

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
                GPIO.output(A1,True)
                GPIO.output(A2,False)
                GPIO.output(B1,True)
                GPIO.output(B2,False)
                
                char = 0
                
            elif char == curses.KEY_DOWN:
                GPIO.output(A1,False)
                GPIO.output(A2,True)
                GPIO.output(B1,False)
                GPIO.output(B2,True)
                
                char = 0
                
            elif char == curses.KEY_RIGHT:
                GPIO.output(A1,True)
                GPIO.output(A2,False)
                GPIO.output(B1,False)
                GPIO.output(B2,True)
                
                char = 0
                
            elif char == curses.KEY_LEFT:
                GPIO.output(A1,False)
                GPIO.output(A2,True)
                GPIO.output(B1,True)
                GPIO.output(B2,False)
                
                char = 0
                
            elif char == ord('s'):
                GPIO.output(A1,False)
                GPIO.output(A2,False)
                GPIO.output(B1,False)
                GPIO.output(B2,False)
                
                char = 0
             
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.output(A1,False)
    GPIO.output(A2,False)
    GPIO.output(B1,False)
    GPIO.output(B2,False)
    GPIO.cleanup()
