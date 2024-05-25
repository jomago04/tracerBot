import curses
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import time

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)

stop_stepper = False  
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
        stop_all_motors()

def control_stepper_motors(key, stdscr):
    global stop_stepper

    if key == ord('u'):  
        stop_stepper = True
        stop_all_motors()
        stdscr.addstr(3, 0, "Stepper Motors Stopped")
        return

    stop_stepper = False

    def stepper_action(motor, direction, style):
        while not stop_stepper:
            motor.onestep(direction=direction, style=style)
            time.sleep(0.000005)
            if stop_stepper:
                break
    
    if key == ord('i'):
        stepper_action(kit1.stepper1, stepper.FORWARD, stepper.INTERLEAVE)
        stdscr.addstr(1, 0, "Stepper Motor 1: Forward")
    elif key == ord('k'):
        stepper_action(kit1.stepper1, stepper.BACKWARD, stepper.INTERLEAVE)
        stdscr.addstr(1, 0, "Stepper Motor 1: Backward")
    elif key == ord('j'):
        stepper_action(kit1.stepper2, stepper.FORWARD, stepper.INTERLEAVE)
        stdscr.addstr(2, 0, "Stepper Motor 2: Forward")
    elif key == ord('l'):
        stepper_action(kit1.stepper2, stepper.BACKWARD, stepper.INTERLEAVE)
        stdscr.addstr(2, 0, "Stepper Motor 2: Backward")
    elif key == ord('e'):
        stop_all_motors()
        kit1.stepper1.release() 
        kit1.stepper2.release()

def main(stdscr):
    global stop_stepper
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.timeout(1)  

    try:
        while True:
            key = stdscr.getch()
            stdscr.clear()

            if key in [ord('w'), ord('s'), ord('a'), ord('d'), ord('e')]:
                control_dc_motors(key)
                stdscr.addstr(0, 0, f"DC Motor Key Pressed: {chr(key)}")

            elif key in [ord('i'), ord('k'), ord('j'), ord('l'), ord('e'), ord('u')]:
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
