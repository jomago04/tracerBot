import curses
import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

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
    if key == ord('w'):
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = 1.0
    elif key == ord('s'):
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = -1.0
    elif key == ord('a'):
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = -1.0
    elif key == ord('d'):
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = 1.0
    elif key == ord('e'):
        # Stop motors if 'e' is pressed
        kit2.motor1.throttle = 0
        kit2.motor2.throttle = 0

def control_stepper_motors(key, stdscr):
    steps = 20
    if key == ord('i'):
        for _ in range(steps):
            kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
        stdscr.addstr(1, 0, "Pitch: Up")
    elif key == ord('k'):
        for _ in range(steps):
            kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
        stdscr.addstr(1, 0, "Pitch: Down")
    elif key == ord('j'):
        for _ in range(steps):
            kit1.stepper2.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
        stdscr.addstr(2, 0, "YAW: Left")
    elif key == ord('l'):
        for _ in range(steps):
            kit1.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
        stdscr.addstr(2, 0, "YAW: Right")
        
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
