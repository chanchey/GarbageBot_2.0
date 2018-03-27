import RPi.GPIO as io

io.setmode(io.BCM)

import sys, tty, termios, time

from time import sleep

motorl_in1_pin = 4

motorl_in2_pin = 17

io.setup(motor1_in1_pin, io.OUT)

io.setup(motor1_in2_pin, io.OUT)

motor2_in1_pin = 24

motor2_in2_pin = 25

io.setup(motor2_in1_pin, io.OUT)

io.setup(motor2_in2_pin, io.OUT)

def getch():

fd = sys.stdin.fileno()

old_settings = termios.tcgetattr(fd) True)

io.output(motorl_in2_pin, Fals

try:

tty.setraw(sys.stdin.fileno())

ch = sys.stdin.read(1)

finally:

termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

return ch

# Instructions for when the user has an interface

print("w/s: acceleration")

print("a/d: steering")

print("x: stop")

while True:

char = getch()

# The car will drive forward when the "w" key is pressed

if (char == "w"):

io.output(motor1_in1_pin, True)

io.output(motor1_in2_pin, False)

io.output(motor2 in1_pin, True)

io.output(motor2_in2_pin, False)

sleep(0.1)

io.output(motor1_in1_pin, False)

io.output(motor1_in2_pin, False)

io.output(motor2_in1_pin, False)

io.output(motor2_in2_pin, False)

# The car will reverse when the "s" key is pressed

elif(char == "s")

io.output(motor1_in1_pin, False)

io.output(motor1_in2_pin, True)

io.output(motor2_in1_pin, False)

io.output(motor2_in2_pin, True)

sleep(0.1)

io.output(motor1_in1_pin, False)

io.output(motor1_in2_pin, False)

io.output(motor2_in1_pin, False)

io.output(motor2 _in2_pin, False)

# The 'a" key will toggle the steering left

elif(char == "a"):

io.output(motor1_in1_pin, True)

io.output(motor1_in2_pin, False)

io.output(motor2_in1_pin, False)

io.output(motor2 in2_pin, False)

sleep(0.1)

io.output(motor1_in1_pin, False)

io.output(motor1_in2_pin, False)

io.output(motor2_in1_pin, False)

io.output(motor2 _in2_pin, False)

# The "d" key will toggle the steering right

elif(char == "d"):

io.output(motor1_in1_pin, False)

io.output(motor1_in2_pin, False)

io.output(motor2_in1_pin, True)

io.output(motor2 in2_pin, False)

sleep(0.1)

io.output(motor1_in1_pin, False)

io.output(motor1_in2_pin, False)

io.output(motor2_in1_pin, False)

io.output(motor2 _in2_pin, False)

# The "x" key will stop the car

io.output(motor1_in1_pin, False)

io.output(motor1_in2_pin, False)

io.output(motor2_in1_pin, False)

io.output(motor2 _in2_pin, False)

# save the file as car.py
