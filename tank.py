import RPi.GPIO as GPIO
import keyboard

# Define GPIO pins and other constants
print("test")
Motor_A_EN = 4
Motor_B_EN = 17
Motor_A_Pin1 = 26
Motor_A_Pin2 = 21
Motor_B_Pin1 = 27
Motor_B_Pin2 = 18

pwm_A = None
pwm_B = None

# Initialize the motors and PWM
def setup():
    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)

    pwm_A = GPIO.PWM(Motor_A_EN, 1000)
    pwm_B = GPIO.PWM(Motor_B_EN, 1000)

# Function to stop the motors
def motorStop():
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)

# Control motor A based on direction (forward, backward, stop)
def motor_A(status, speed):
    if status == 'forward':
        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        pwm_A.start(100)
        pwm_A.ChangeDutyCycle(min(max(speed, 0), 100))  # Ensure speed is within 0-100 range
    elif status == 'backward':
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
        pwm_A.start(0)
        pwm_A.ChangeDutyCycle(min(max(speed, 0), 100))  # Ensure speed is within 0-100 range
    elif status == 'stop':
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)

# Control motor B based on direction (forward, backward, stop)
def motor_B(status, speed):
    if status == 'forward':
        GPIO.output(Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        pwm_B.start(100)
        pwm_B.ChangeDutyCycle(min(max(speed, 0), 100))  # Ensure speed is within 0-100 range
    elif status == 'backward':
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.HIGH)
        pwm_B.start(0)
        pwm_B.ChangeDutyCycle(min(max(speed, 0), 100))  # Ensure speed is within 0-100 range
    elif status == 'stop':
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)

# Main loop
def main():
    setup()
    speed_set = 100  # Set the default speed
    motor_A_direction = 'stop'
    motor_B_direction = 'stop'

    try:
        while True:
            # Check if 'W' is held
            if keyboard.is_pressed('w'):
                motor_A_direction = 'backward'
                motor_B_direction = 'forward'
            # Check if 'S' is held
            elif keyboard.is_pressed('s'):
                motor_A_direction = 'forward'
                motor_B_direction = 'backward'
            # Check if 'A' is held
            elif keyboard.is_pressed('a'):
                motor_A_direction = 'forward'
                motor_B_direction = 'forward'
            # Check if 'D' is held
            elif keyboard.is_pressed('d'):
                motor_A_direction = 'backward'
                motor_B_direction = 'backward'
            else:
                motor_A_direction = 'stop'
                motor_B_direction = 'stop'

            motor_A(motor_A_direction, speed_set)
            motor_B(motor_B_direction, speed_set)

    except KeyboardInterrupt:
        pass
    finally:
        # Clean up on exit
        motorStop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
