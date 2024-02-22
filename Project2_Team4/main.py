#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
import sys
import math
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

MOVE_SPEED = 300
WALL_SENS_DIST = 150
WANDER_TURN_TIME = 825
WANDER_FWD_TIME = 900
WANDER_BACK_TIME = 900

LEFT = True
LEFT_COUNT = 0

# Create your objects here.
ev3 = EV3Brick()
lw = Motor(Port.C)
rw = Motor(Port.B)
lt = TouchSensor(Port.S4)
rt = TouchSensor(Port.S1)
cr = ColorSensor(Port.S2)
sonic = UltrasonicSensor(Port.S3)
wind = Motor(Port.A)

# Write your program here.

def true_wander(lw, rw, cr, sonic, speed, ev3, wind, lt, rt):
	global LEFT
	global LEFT_COUNT
	inner_bool = LEFT
	print(inner_bool, LEFT)
	bumpCount = 0
	while 1:
		while 1:
			# Drive until bump wall
			lw.run_time(speed, WANDER_FWD_TIME, then=Stop.HOLD, wait=False)
			rw.run_time(speed, WANDER_FWD_TIME, then=Stop.HOLD, wait=True)
			goal_check(cr, ev3, wind, lw, rw)
			if lt.pressed() or rt.pressed():
				break
		# Drive backward away from wall
		lw.run_time(-speed, WANDER_BACK_TIME, then=Stop.HOLD, wait=False)
		rw.run_time(-speed, WANDER_BACK_TIME, then=Stop.HOLD, wait=True)
		goal_check(cr, ev3, wind, lw, rw)
		# Turn to left
		if LEFT == True:
			if bumpCount == 3:
				print("right")
				rw.run_time(-speed, WANDER_TURN_TIME, then=Stop.HOLD, wait=False)
				lw.run_time(speed, WANDER_TURN_TIME, then=Stop.HOLD, wait=True)
				goal_check(cr, ev3, wind, lw, rw)
			else:
				lw.run_time(-speed, WANDER_TURN_TIME, then=Stop.HOLD, wait=False)
				rw.run_time(speed, WANDER_TURN_TIME, then=Stop.HOLD, wait=True)
				goal_check(cr, ev3, wind, lw, rw)
		# Turn right on every other go of the loop
		elif LEFT == False:
			if bumpCount == 3:
				print("left")
				lw.run_time(-speed, WANDER_TURN_TIME, then=Stop.HOLD, wait=False)
				rw.run_time(speed, WANDER_TURN_TIME, then=Stop.HOLD, wait=True)
				goal_check(cr, ev3, wind, lw, rw)
			else:
				rw.run_time(-speed, WANDER_TURN_TIME, then=Stop.HOLD, wait=False)
				lw.run_time(speed, WANDER_TURN_TIME, then=Stop.HOLD, wait=True)
				goal_check(cr, ev3, wind, lw, rw)
		# bumpCount increase and loop again until 10 bumps occur
		bumpCount += 1
		if bumpCount == 4:
			LEFT_COUNT += 1
			if LEFT == False:
				LEFT_COUNT += 1
			if LEFT_COUNT == 2:
				LEFT = not LEFT
				LEFT_COUNT = 0
			break
	# After 3 bumps, drive until wall is bumped
	while 1:
		lw.run(speed)
		rw.run(speed)
		goal_check(cr, ev3, wind, lw, rw)
		if lt.pressed() or rt.pressed():
			break
	# Drive backward away from wall
	lw.run_time(-speed, WANDER_BACK_TIME, then=Stop.HOLD, wait=False)
	rw.run_time(-speed, WANDER_BACK_TIME, then=Stop.HOLD, wait=True)
	goal_check(cr, ev3, wind, lw, rw)
	while 1:
		# Spin until wall is found, break back into wander at < WALL_SENS_DIST
		# Should go back directly into wall()
		rw.run_time(-speed, 450, then=Stop.HOLD, wait=False)
		lw.run_time(speed, 450, then=Stop.HOLD, wait=True)
		goal_check(cr, ev3, wind, lw, rw)
		if(sonic.distance() < WALL_SENS_DIST):
			break

def wander(lw, rw, cr, sonic, speed, ev3, wind, lt, rt):
	movement_selector = 1
	while(1):
		goal_check(cr, ev3, wind, lw, rw)
		if(lt.pressed()):
			# If lt pressed and distance > 360, turn left
			if(sonic.distance() > 360):
				rw.stop()
				lw.run_time(-speed, 1000, wait=True)
				if(sonic.distance() < WALL_SENS_DIST):
					break				
			else:
				lw.stop()
				rw.run_time(-speed,900, wait=True)
				if(sonic.distance() < WALL_SENS_DIST):
					break
		elif(rt.pressed()):
			# If rt pressed and distance > 360, turn left
			if(sonic.distance() > 360):
				rw.stop()
				lw.run_time(-speed, 1000, wait=True)
				if(sonic.distance() < WALL_SENS_DIST):
					break
			else:
				lw.stop()
				rw.run_time(-speed, 900, wait=True)
				if(sonic.distance() < WALL_SENS_DIST):
					break
		else:
			# Do not delete. Alter value so that results are better
			# if distance < WALL_SENS_DIST, go back into wall
			# else, true_wander()
			lw.run_time(-speed, 0, wait=False)
			rw.run_time(speed, 0, wait=True)
			if(sonic.distance() < WALL_SENS_DIST):
				break
			else:
				goal_check(cr, ev3, wind, lw, rw)
				true_wander(lw, rw, cr, sonic, speed, ev3, wind, lt, rt)
				while 1:
					# always return state of LEFT but turn if sonic distance too large
					if(sonic.distance() > WALL_SENS_DIST):
						lw.run_time(-speed, 300, then=Stop.HOLD, wait=False)
						rw.run_time(speed, 300, then=Stop.HOLD, wait=True)
					else:
						break
				break

def goal_check(cr, ev3, wind, lw, rw):
	if(cr.color() == Color.WHITE or cr.color() == Color.BLUE or cr.color() == Color.YELLOW):
		lw.stop()
		rw.stop()
		wind.run_time(1000,10000,wait=True)
		sys.exit()

def wall(lw, rw, cr, sonic, speed, ev3, wind, lt, rt):
	start = time.time()
	time_flag = 0
	fflag = 0
	while(1):
		goal_check(cr, ev3, wind, lw, rw)
		if(lt.pressed() or rt.pressed()):
			wander(lw, rw, cr, sonic, speed, ev3, wind, lt, rt)
				
		else:
			goal_check(cr, ev3, wind, lw, rw)
			if(time_flag == 0 and (sonic.distance() >= WALL_SENS_DIST and sonic.distance() <= 3000)):
				start = time.time()
				time_flag = 1
			if(sonic.distance() >= WALL_SENS_DIST and sonic.distance() <= 3000):
				end = time.time()
				if(end-start >= 2.25):
					# May need to be changed to true_wander
					# true_wander(lw, rw, cr, sonic, speed, ev3, wind, lt, rt)
					wander(lw, rw, cr, sonic, speed, ev3, wind, lt, rt)
					start = 0
					time_flag = 0
				else:
					lw.run(speed/2.66)
					rw.run(speed)
			if(sonic.distance() >= 95 and sonic.distance() <= WALL_SENS_DIST):
				time_flag = 0
				start = 0
				lw.run(speed/2.66)
				rw.run(speed)
			elif(sonic.distance() >= 65 and sonic.distance() < 95):
				time_flag = 0
				start = 0
				lw.run(speed)
				rw.run(speed)
			elif(sonic.distance() < 65):
				time_flag = 0
				start = 0
				lw.run(speed)
				rw.run(speed/2)

wall(lw, rw, cr, sonic, MOVE_SPEED, ev3, wind, lt, rt)
