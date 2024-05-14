import curses
from adafruit_motorkit import MotorKit

# Initialize the MotorKit instance for the board at address 0x60
kit = MotorKit(address=0x60)

def toggle_motor(motor_state):
    """
    Toggles the motor state between on and off.
    """
    if motor_state['running']:
        # Turn the motor off
        kit.motor3.throttle = 0
        motor_state['running'] = False
        print("Motor is now OFF.")
    else:
        # Turn the motor on at maximum power
        kit.motor3.throttle = 1.0
        motor_state['running'] = True
        print("Motor is now ON.")

def main(stdscr):
    # Clear screen
    stdscr.clear()
    # Hide cursor
    curses.curs_set(0)
    
    motor_state = {'running': False}
    
    stdscr.addstr("Press 't' to toggle the motor on/off. Press 'ESC' to exit.\n")
    while True:
        # Wait for next input
        k = stdscr.getch()
        
        if k == ord('t'):
            toggle_motor(motor_state)
        elif k == 27:  # ESC key
            break
    
    # Turn the motor off before exiting if it was left on
    if motor_state['running']:
        kit.motor3.throttle = 0

# Wrap the main function to initialize curses
curses.wrapper(main)
