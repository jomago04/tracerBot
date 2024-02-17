import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import keyboard

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)

def stop_all_motors():
    kit2.motor1.throttle = 0
    kit2.motor2.throttle = 0
    kit1.stepper1.release()
    kit1.stepper2.release()

def control_dc_motors(direction):
    if direction == 'forward':
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = -1.0
    elif direction == 'backward':
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = 1.0
    elif direction == 'left':
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = 1.0
    elif direction == 'right':
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = -1.0
    elif direction == 'stop':
        kit2.motor1.throttle = 0
        kit2.motor2.throttle = 0

def control_stepper_motors(motor, direction):
    steps_per_action = 10
    stepper_motor = kit1.stepper1 if motor == 1 else kit1.stepper2
    step_direction = stepper.FORWARD if direction == 'forward' else stepper.BACKWARD
    for _ in range(steps_per_action):
        stepper_motor.onestep(direction=step_direction, style=stepper.DOUBLE)
        time.sleep(0.0005)  # adjust based on post press latency
    stepper_motor.release()

def setup_keyboard_listeners():
    # DC motor controls
    keyboard.add_hotkey('w', control_dc_motors, args=('forward',))
    keyboard.add_hotkey('s', control_dc_motors, args=('backward',))
    keyboard.add_hotkey('a', control_dc_motors, args=('left',))
    keyboard.add_hotkey('d', control_dc_motors, args=('right',))
    keyboard.add_hotkey('e', control_dc_motors, args=('stop',))

    # stepper motor controls
    keyboard.add_hotkey('i', control_stepper_motors, args=(1, 'forward',))
    keyboard.add_hotkey('k', control_stepper_motors, args=(1, 'backward',))
    keyboard.add_hotkey('j', control_stepper_motors, args=(2, 'forward',))
    keyboard.add_hotkey('l', control_stepper_motors, args=(2, 'backward',))

def main():
    print("Running... Press ESC to stop.")
    setup_keyboard_listeners()
    try:
        # use a blocking call to wait for ESC key, or use a loop to do other things
        keyboard.wait('esc')
    finally:
        stop_all_motors()
        print("Stopped.")

if __name__ == '__main__':
    main()
