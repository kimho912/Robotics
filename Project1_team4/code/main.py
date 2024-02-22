
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
import math
import path_functions as pf
import path_node as pn
import path as p
import time

TURN_SPEED = 40
MOVE_SPEED = 180
ANGLE = 120
TILE_DEGREE = 630

def BotForward(left_wheel, right_wheel, ev3):
	left_wheel.run_target(MOVE_SPEED, TILE_DEGREE, wait=False)
	right_wheel.run_target(MOVE_SPEED, TILE_DEGREE)
	left_wheel.reset_angle(0)
	right_wheel.reset_angle(0)

def BotBackward(left_wheel, right_wheel, ev3):
	left_wheel.run_target(MOVE_SPEED, -1*TILE_DEGREE, wait=False)
	right_wheel.run_target(MOVE_SPEED, -1*TILE_DEGREE)
	left_wheel.reset_angle(0)
	right_wheel.reset_angle(0)

def BotLeft(left_wheel, right_wheel, ev3):
	gyro.reset_angle(0)
	angle2 = ANGLE
	wait_f = False
	while(1):
		left_wheel.run_target(TURN_SPEED, -1*angle2, wait=False)
		right_wheel.run_target(TURN_SPEED, angle2)
		ang = gyro.angle()
		left_wheel.reset_angle(0)
		right_wheel.reset_angle(0)
		if wait_f:
			time.sleep(0.25)
		if(ang <= -50):
			angle2 = 1
		if(ang <= -92):
			ev3.screen.print(ang)
			left_wheel.run_target(TURN_SPEED, 5)
			break

def BotRight(left_wheel, right_wheel, ev3):	
	gyro.reset_angle(0)
	angle2 = ANGLE
	wait_f = False
	while(1):
		left_wheel.run_target(TURN_SPEED, angle2, wait=False)
		right_wheel.run_target(TURN_SPEED, -1*angle2)
		ang = gyro.angle()
		left_wheel.reset_angle(0)
		right_wheel.reset_angle(0)
		if wait_f:
			time.sleep(0.25)
		if(ang >= 50):
			angle2 = 1			
		if(ang >= 85):
			ev3.screen.print(ang)
			if ang > 90:
				left_wheel.run_target(TURN_SPEED, -1*angle2, wait=False)
				right_wheel.run_target(TURN_SPEED, angle2)
			
			right_wheel.run_target(TURN_SPEED, 5)
			break
def BotRight45(left_wheel, right_wheel, ev3):	
	gyro.reset_angle(0)
	angle2 = ANGLE/2
	wait_f = False
	while(1):
		left_wheel.run_target(TURN_SPEED, angle2, wait=False)
		right_wheel.run_target(TURN_SPEED, -1*angle2)
		ang = gyro.angle()
		left_wheel.reset_angle(0)
		right_wheel.reset_angle(0)
		ev3.screen.print(ang)
		if wait_f:
			time.sleep(0.25)
		if(ang >= 30):
			angle2 = 1
			wait_f = True
		if(ang >= 44):
			ev3.screen.print(ang)
			break

def BotLeft45(left_wheel, right_wheel, ev3):	
	angle2 = ANGLE/2
	gyro.reset_angle(0)
	wait_f = False
	while(1):
		left_wheel.run_target(TURN_SPEED, -angle2, wait=False)
		right_wheel.run_target(TURN_SPEED, 1*angle2)
		ang = gyro.angle()
		left_wheel.reset_angle(0)
		right_wheel.reset_angle(0)
		if wait_f:
			time.sleep(0.25)
		if(ang <= -33):
			angle2 = 1
			wait_f = True		
		if(ang <= -45):
			ev3.screen.print(ang)
			break
def BotDiagonal(left_wheel, right_wheel):
	left_wheel.run_target(MOVE_SPEED, TILE_DEGREE/2, wait=False)
	right_wheel.run_target(MOVE_SPEED, TILE_DEGREE/2)
	left_wheel.reset_angle(0)
	right_wheel.reset_angle(0)

def BotCenter(left_wheel, right_wheel, ev3):		
	BotRight(left_wheel, right_wheel, ev3)	
	BotDiagonal(left_wheel, right_wheel)	
	BotLeft(left_wheel, right_wheel, ev3)
	BotDiagonal(left_wheel, right_wheel)

ev3 = EV3Brick()
left_wheel = Motor(Port.C)
right_wheel = Motor(Port.B)
gyro = GyroSensor(Port.S4)

path = p.findpath()
print(path)
BotCenter(left_wheel, right_wheel, ev3)
gyro.reset_angle(0)

right_f, up_f, down_f, left_f = True, False, False, False
for i in path:
	ev3.screen.print(i)
	if i == "right":
		if right_f == True:
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = True, False, False, False
		elif up_f == True:
			BotRight(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel,ev3)
			right_f, up_f, down_f, left_f = True, False, False, False
		elif down_f == True:
			BotLeft(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = True, False, False, False
		elif left_f == True:
			BotRight(left_wheel, right_wheel, ev3)
			BotRight(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = True, False, False, False
	elif i == "up":
		if right_f == True:
			BotLeft(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, True, False, False
		elif up_f == True:
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, True, False, False
		elif down_f == True:
			BotLeft(left_wheel, right_wheel, ev3)
			BotLeft(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel)
			right_f, up_f, down_f, left_f = False, True, False, False
		elif left_f == True:
			BotRight(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, True, False, False
	elif i == "down":
		if right_f == True:
			BotRight(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, False, True, False
		elif up_f == True:
			BotRight(left_wheel, right_wheel, ev3)
			BotRight(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, False, True, False
		elif down_f == True:
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, False, True, False
		elif left_f == True:
			BotLeft(left_wheel, right_wheel,ev3)
			right_f, up_f, down_f, left_f = False, False, True, False
	elif i == "left":
		if right_f == True:
			BotBackward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, False, False, True
		elif up_f == True:
			BotLeft(left_wheel, right_wheel,ev3)
			BotForward(left_wheel, right_wheel)
			right_f, up_f, down_f, left_f = False, False, False, True
		elif down_f == True:
			BotRight(left_wheel, right_wheel, ev3)
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, False, False, True
		elif left_f == True:
			BotForward(left_wheel, right_wheel, ev3)
			right_f, up_f, down_f, left_f = False, False, False, True			

if right_f == True:
	BotLeft(left_wheel, right_wheel, ev3)
	BotLeft45(left_wheel, right_wheel, ev3)	
	BotDiagonal(left_wheel, right_wheel)
elif up_f == True:	
	BotLeft45(left_wheel, right_wheel, ev3)	
	BotDiagonal(left_wheel, right_wheel)
elif down_f == True:
	BotRight(left_wheel, right_wheel, ev3)
	BotRight45(left_wheel, right_wheel, ev3)	
	BotDiagonal(left_wheel, right_wheel)
elif left_f == True:
	BotRight45(left_wheel, right_wheel, ev3)	
	BotDiagonal(left_wheel, right_wheel)
