import time
from adafruit_motorkit import motorkit

kit = MotorKit()

kit.motor1.throttle = 1.0
time.sleep(0.2)

kit.motor1.throttle = 0