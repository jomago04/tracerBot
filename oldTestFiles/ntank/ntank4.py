import threading
import curses
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()

motor_states = {
    'dc_forward': False,
    'dc_backward': False,
    'dc_left': False,
    'dc_right': False,
    'stepper1_forward': False,
    'stepper1_backward': False,
    'stepper2_forward': False,
    'stepper2_backward': False,
}

def control_dc_motors():
    while True:
        if motor_states['dc_forward']:
            kit.motor1.throttle = 1.0
            kit.motor2.throttle = -1.0
        elif motor_states['dc_backward']:
            kit.motor1.throttle = -1.0
            kit.motor2.throttle = 1.0
        elif motor_states['dc_left']:
            kit.motor1.throttle = 1.0
            kit.motor2.throttle = 1.0
        elif motor_states['dc_right']:
            kit.motor1.throttle = -1.0
            kit.motor2.throttle = -1.0
        else:
            kit.motor1.throttle = 0
            kit.motor2.throttle = 0

        time.sleep(0.1)

def control_stepper_motor(motor_name, direction):
    motor = getattr(kit, motor_name)
    while motor_states[f'{motor_name}_{direction}']:
        motor.onestep(direction=getattr(stepper, direction), style=stepper.INTERLEAVE)
        time.sleep(0.01)
    motor.release()

def main(stdscr):
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    dc_thread = threading.Thread(target=control_dc_motors, daemon=True)
    dc_thread.start()

    while True:
        try:
            key = stdscr.getch()
            if key == ord('w'):
                motor_states['dc_forward'] = True
            elif key == ord('s'):
                motor_states['dc_backward'] = True
            elif key == ord('a'):
                motor_states['dc_left'] = True
            elif key == ord('d'):
                motor_states['dc_right'] = True
            elif key == ord('i'):
                if not motor_states['stepper1_forward']:
                    motor_states['stepper1_forward'] = True
                    threading.Thread(target=control_stepper_motor, args=('stepper1', 'FORWARD'), daemon=True).start()
                else:
                    motor_states['stepper1_forward'] = False
            elif key == ord('k'):
                if not motor_states['stepper1_backward']:
                    motor_states['stepper1_backward'] = True
                    threading.Thread(target=control_stepper_motor, args=('stepper1', 'BACKWARD'), daemon=True).start()
                else:
                    motor_states['stepper1_backward'] = False
            elif key == ord('j'):
                if not motor_states['stepper2_forward']:
                    motor_states['stepper2_forward'] = True
                    threading.Thread(target=control_stepper_motor, args=('stepper2', 'FORWARD'), daemon=True).start()
                else:
                    motor_states['stepper2_forward'] = False
            elif key == ord('l'):
                if not motor_states['stepper2_backward']:
                     motor_states['stepper2_backward'] = True
                    
            elif key == ord('u'): 
                for motor in motor_states.keys():
                    motor_states[motor] = False

            elif key == ord('e'):  
                break

        except Exception as e:
            print(f"Error: {e}")
            break


    for motor in motor_states.keys():
        motor_states[motor] = False
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)

