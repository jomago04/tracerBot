import curses 
import time
from adafruit_motorkit import MotorKit
form adafruit_motor import stepper 

dcmotors = MotorKit(address=0x60)

def hault():
    kit1.motor1.throttle = 0 
    kit1.motor1.throttle