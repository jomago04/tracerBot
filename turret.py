import RPi.GPIO as GPIO
from DRV8825 import DRV8825
import keyboard
import time

# Initialize the motors
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor1.SetMicroStep('softward', 'fullstep')
Motor2.SetMicroStep('softward', 'fullstep')

def control_motor(motor, direction, steps, delay):
    motor.TurnStep(Dir=direction, steps=steps, stepdelay=delay)

def main():
    try:       
        while True:
            time.sleep(0.01)  # Short delay to reduce CPU usage
            if keyboard.is_pressed('s'):
                control_motor(Motor2, 'forward', 200, 0.00000005)
            elif keyboard.is_pressed('w'):
                control_motor(Motor2, 'backward', 200, 0.00000005)
            elif keyboard.is_pressed('d'):
                control_motor(Motor1, 'backward', 200, 0.00000005)
            elif keyboard.is_pressed('a'):
                control_motor(Motor1, 'forward', 200, 0.00000005)
            else:
                Motor1.Stop()
                Motor2.Stop()

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        Motor1.Stop()
        Motor2.Stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
