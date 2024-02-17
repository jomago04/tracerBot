import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import keyboard

kit1 = MotorKit()
kit2 = MotorKit(address=0x61)

def stop_all_motors():
    kit2.motor1.throttle = 0
    kit2.motor2.throttle = 0
    kit1.stepper1.release()
    kit1.stepper2.release()

def control_dc_motors():
    if keyboard.is_pressed('w'):
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = 1.0
    elif keyboard.is_pressed('s'):
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = -1.0
    elif keyboard.is_pressed('a'):
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = -1.0
    elif keyboard.is_pressed('d'):
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = 1.0
    else:
        kit2.motor1.throttle = 0
        kit2.motor2.throttle = 0

def control_stepper_motors():
    if keyboard.is_pressed('i'):
        kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    elif keyboard.is_pressed('k'):
        kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
    elif keyboard.is_pressed('j'):
        kit1.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    elif keyboard.is_pressed('l'):
        kit1.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
    time.sleep(0.1) 

def main():
    try:
        while True:
            control_dc_motors()
            control_stepper_motors()
            time.sleep(0.1) 
    except KeyboardInterrupt:
        pass
    finally:
        stop_all_motors()  

if __name__ == "__main__":
    main()
