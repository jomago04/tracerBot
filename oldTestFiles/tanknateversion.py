import curses
import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
#nathan was here testing
# Initialize motor kits
kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)

def stop_all_motors():
    # Function to stop all motors
    kit2.motor1.throttle = 0
    kit2.motor2.throttle = 0
    # Add code to stop stepper motors if necessary

def control_dc_motors(key):
    # Control the DC motors (tank tracks)
    if key == ord('a'):
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = 1.0
    elif key == ord('d'):
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = -1.0
    elif key == ord('w'):
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = -1.0
    elif key == ord('s'):
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = 1.0
    elif key == ord('e'):
        # Stop motors if 'e' is pressed
        kit2.motor1.throttle = 0
        kit2.motor2.throttle = 0

def control_stepper_motors(key, stdscr):
    # Control the stepper motors (turret)
    if key == ord('i'):
        kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        stdscr.addstr(1, 0, "Stepper Motor 1: Forward")
    elif key == ord('k'):
        kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        stdscr.addstr(1, 0, "Stepper Motor 1: Backward")
    elif key == ord('j'):
        kit1.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        stdscr.addstr(2, 0, "Stepper Motor 2: Forward")
    elif key == ord('l'):
        kit1.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        stdscr.addstr(2, 0, "Stepper Motor 2: Backward")
    elif key == ord('e'):
        # Add code to stop stepper motors if necessary when 'e' is pressed
        pass  # Replace this with actual code to stop the stepper motors if needed
    time.sleep(0.1)  # Small delay after stepper motor control

def main(stdscr):
    # Set up curses environment
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.timeout(100)    # Timeout in milliseconds

    try:
        while True:
            key = stdscr.getch()
            stdscr.clear()

            # Control DC motors
            if key in [ord('w'), ord('s'), ord('a'), ord('d'), ord('e')]:
                control_dc_motors(key)
                stdscr.addstr(0, 0, f"DC Motor Key Pressed: {chr(key)}")

            # Control stepper motors
            elif key in [ord('i'), ord('k'), ord('j'), ord('l'), ord('e')]:
                control_stepper_motors(key, stdscr)

            # Exit
            elif key == ord('q'):
                break

            stdscr.refresh()
    except KeyboardInterrupt:
        pass
    finally:
        stop_all_motors()  # Ensure motors are stopped when the program exits

if __name__ == '__main__':
    curses.wrapper(main)
