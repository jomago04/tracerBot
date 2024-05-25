import pygame
import sys
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit1 = MotorKit(address=0x60)
kit2 = MotorKit(address=0x61)

def stop_all_motors():
    kit2.motor1.throttle = 0
    kit2.motor2.throttle = 0
    kit1.stepper1.release()
    kit1.stepper2.release()

def control_dc_motors(action):
    if action == 'left':
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = 1.0
    elif action == 'right':
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = -1.0
    elif action == 'forward':
        kit2.motor1.throttle = 1.0
        kit2.motor2.throttle = -1.0
    elif action == 'backward':
        kit2.motor1.throttle = -1.0
        kit2.motor2.throttle = 1.0
    elif action == 'stop':
        kit2.motor1.throttle = 0
        kit2.motor2.throttle = 0

def control_stepper_motors(direction, motor):
    if motor == 'stepper1':
        if direction == 'forward':
            kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        elif direction == 'backward':
            kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    elif motor == 'stepper2':
        if direction == 'forward':
            kit1.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        elif direction == 'backward':
            kit1.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Robot Control")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                control_dc_motors('forward')
            elif event.key == pygame.K_s:
                control_dc_motors('backward')
            elif event.key == pygame.K_a:
                control_dc_motors('left')
            elif event.key == pygame.K_d:
                control_dc_motors('right')
            elif event.key == pygame.K_i:
                control_stepper_motors('forward', 'stepper1')
            elif event.key == pygame.K_k:
                control_stepper_motors('backward', 'stepper1')
            elif event.key == pygame.K_j:
                control_stepper_motors('forward', 'stepper2')
            elif event.key == pygame.K_l:
                control_stepper_motors('backward', 'stepper2')
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                control_dc_motors('stop')
            elif event.key in [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l]:
                kit1.stepper1.release()
                kit1.stepper2.release()

    pygame.display.flip()
    clock.tick(60) 

stop_all_motors()
pygame.quit()
