import curses
import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)

def stop_all_motors():
    kit2.motor1.throttle = 0
    kit2.motor2.throttle = 0
    kit1.stepper1.release()
    kit1.stepper2.release()

def control_dc_motors(key):
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
        kit2.motor1.throttle = 0
        kit2.motor2.throttle = 0

def control_stepper_motors(key, stdscr):
    steps_per_action = 10 
    if key in [ord('i'), ord('k'), ord('j'), ord('l')]:
        for _ in range(steps_per_action):
            if key == ord('i'):
                kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            elif key == ord('k'):
                kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            elif key == ord('j'):
                kit1.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            elif key == ord('l'):
                kit1.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(0.000005)  

        kit1.stepper1.release()
        kit1.stepper2.release()

def main(stdscr):
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.timeout(100) 

    try:
        while True:
            key = stdscr.getch()
            stdscr.clear()

            if key in [ord('w'), ord('s'), ord('a'), ord('d'), ord('e')]:
                control_dc_motors(key)
                stdscr.addstr(0, 0, f"DC Motor Key Pressed: {chr(key)}")

            elif key in [ord('i'), ord('k'), ord('j'), ord('l')]:
                control_stepper_motors(key, stdscr)

            elif key == ord('q'):
                break

            stdscr.refresh()
    except KeyboardInterrupt:
        pass
    finally:
        stop_all_motors()  

if __name__ == '__main__':
    curses.wrapper(main)
