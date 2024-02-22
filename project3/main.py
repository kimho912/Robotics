#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
								InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import I2CDevice

import sys
import time

"""
	NOTES:
	- 
"""

class InfraredSensor():
	def __init__(self, port):
		self.sensor = I2CDevice(port, 0x01)
	def get_zone (self):
		"""Returns Zone that IR signal is observed in."""
		return int. from_bytes(self.sensor.read(0x42, length=1), "little")

	def get_strength(self):
		"""Returns an array with the relative strength of IR in each zone."""
		retArray = []
		for i in range(5):
			strength = int.from_bytes(self.sensor.read(0x43+i, length=1), "little")
			retArray.append (strength)
		return retArray
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

MOVE_SPEED = -200
home_line = Color.BLUE
goal_line = Color.RED

# Flags
homeFlag = True
middleFlag = False

# Create your objects here.
ev3 = EV3Brick()
lw = Motor(Port.C)
rw = Motor(Port.B)
gr = GyroSensor(Port.S3)
cr = ColorSensor(Port.S4)
sonic = UltrasonicSensor(Port.S2)
ir = InfraredSensor(Port.S1)

# returns max index and strength of IR signal
# -1 for either val returned indicates no ball detected or bad reading.
def maxidx(arr):
	maxval = -1
	ind = -1
	for i in range(len(arr)):
		if arr[i] > maxval and arr[i] > 0:
			maxval = arr[i]
			ind = i
	return ind, maxval

# resets angle within range of 360
def reset(gr):
	ang = gr.angle()
	if ang > 355 and ang < 370:
		gr.reset_angle(0)

home_line_start = time.perf_counter()
home_flag = 0
# logic for what bot should do when line is detected
def detect_line(cr,lw,rw):
	global home_line_start
	global home_line
	global goal_line
	global home_flag
	global MOVE_SPEED
	home_line_end = time.perf_counter()
	end = 0
	# home_flag only 0 befor 1.5 seconds, scanning for home side
	if home_flag == 0:
		if cr.color() == Color.BLUE:
			home_line = Color.BLUE
			goal_line = Color.RED
			home_flag = 1
			ev3.screen.print("BLUE")
		if cr.color() == Color.RED:
			home_line = Color.RED
			goal_line = Color.BLUE
			home_flag = 1
			ev3.screen.print("RED")
	# after 1.5 seconds, detect logic kicks in
	if home_line_end - home_line_start > 1.5:
		if (cr.color() == goal_line):
			# for 180 and -180
			if gr.angle() in range(135, 225) or gr.angle() in range(-225, -135):
				start = time.perf_counter()
				while end - start < 1.5:
					lw.run(MOVE_SPEED)
					rw.run(MOVE_SPEED)
					end = time.perf_counter()
			# right
			if gr.angle() in range(45,135) or gr.angle() in range(-225, -315):
				start = time.perf_counter()
				while end - start < 0.5:
					lw.run(MOVE_SPEED)
					rw.run(-MOVE_SPEED)
					end = time.perf_counter()
				while end - start < 2:
					lw.run(MOVE_SPEED)
					rw.run(MOVE_SPEED)
					end = time.perf_counter()
			# left
			# changed line 109-115 where lw, put rw
			elif gr.angle() in range(-135, -45) or gr.angle() in range(315, 225):
				start = time.perf_counter()
				while end - start < 0.5:
					rw.run(MOVE_SPEED)
					lw.run(-MOVE_SPEED)
					end = time.perf_counter()
				while end - start < 1:
					rw.run(MOVE_SPEED)
					lw.run(MOVE_SPEED)
					end = time.perf_counter()
			else:
				start = time.perf_counter()
				while end - start < 2:
					lw.run(-MOVE_SPEED)
					rw.run(-MOVE_SPEED)
					end = time.perf_counter()
		(_,detect_ball) = maxidx(ir.get_strength())
		if cr.color() == home_line and detect_ball == -1:
			lw.run_time(-MOVE_SPEED, 1000, wait = False)
			rw.run_time(-MOVE_SPEED, 2000, wait = True)
		# logic for when needing to go back into home side
		if cr.color() == home_line and detect_ball != -1:
			strength = 0
			while (1):
				(dir,strength) = maxidx(ir.get_strength())
				if strength > 20:
					if dir == 2:
						if gr.angle() in range(45, 200) or gr.angle() in range(-355, -225):
							lw.run(-MOVE_SPEED)
							rw.run(MOVE_SPEED)
						if gr.angle() in range(-200, -45) or gr.angle() in range(255, 355):
							lw.run(MOVE_SPEED)
							rw.run(-MOVE_SPEED)
				if strength > 9:
					if dir == 1:
						if gr.angle() in range(45, 200) or gr.angle() in range(-355, -225):
							lw.run(-MOVE_SPEED)
							rw.run(MOVE_SPEED)
						if gr.angle() in range(-200, -45) or gr.angle() in range(255, 355):
							lw.run(MOVE_SPEED)
							rw.run(-MOVE_SPEED)
				if strength > 5:
					strength  = 5
				elif sonic.distance() < 220 and ball_location != -1:
					if gr.angle() in range(25,155) or gr.angle() in range(-245, -335):
						rw.run_time(MOVE_SPEED, 500, wait = False)
						lw.run_time(-MOVE_SPEED, 500, wait = True)
					elif gr.angle() in range(-155, -25) or gr.angle() in range(335, 245):
						lw.run_time(MOVE_SPEED, 500, wait = False)
						rw.run_time(-MOVE_SPEED, 500, wait = True)
					else:
						lw.run_time(-MOVE_SPEED, 500, wait = False)
						rw.run_time(-MOVE_SPEED, 500, wait = True)
						# back up from wall and turn
						lw.run_time(MOVE_SPEED, 500, wait = False)
						rw.run_time(-MOVE_SPEED, 500, wait = True)
				if cr.color() == home_line and strength != -1 and gr.angle() in range(-90, 90):
					start5 = time.perf_counter()
					while(1):
						end5 = time.perf_counter()
						if end5-start5 > 5:
							break
					break
				elif dir == 0:
					# lw.run(MOVE_SPEED/(5*strength))
					lw.stop()
					rw.run(MOVE_SPEED/strength)
				elif dir == 1:
					lw.run(-MOVE_SPEED/(2*strength))
					rw.run(MOVE_SPEED/strength)
				elif dir == 2:
					lw.run(MOVE_SPEED/strength)
					rw.run(MOVE_SPEED/strength)
				elif dir == 2 and gr.angle() in range(90, 180):
					lw.run(-MOVE_SPEED/(2*strength))
					rw.run(MOVE_SPEED/strength)
				# left wheel faster when neg ang means bot facing bottom left corner
				elif dir == 2 and gr.angle() in range(-90, -180):
					lw.run(MOVE_SPEED/strength)
					rw.run(-MOVE_SPEED/(2*strength))
				elif dir == 3:
					rand = 0
					lw.run(MOVE_SPEED/strength)
					rw.run(-MOVE_SPEED/(2*strength))
				elif dir == 4:
					rand = 0
					lw.run(MOVE_SPEED/strength)
					# rw.run(MOVE_SPEED/(5*strength))
					rw.stop()
					
go_forward_on_start = 0

# Actions
# ball following while ball is dected and not detected
def ball_folling(lw,rw,ball_location,cr,gr,rand,strength):
	reset(gr)
	global go_forward_on_start
	if(ball_location == -1):
		reset(gr)
		start = time.perf_counter()
		end = 0
		if(rand == 0):
			if go_forward_on_start == 0:	
				while (end-start < 1.5 ):
					detect_line(cr,lw,rw)
					lw.run(MOVE_SPEED)
					rw.run(MOVE_SPEED)
					end = time.perf_counter()
					go_forward_on_start = 1
			else:
				while (end-start < 0.5 ):
					detect_line(cr,lw,rw)
					lw.run(MOVE_SPEED)
					rw.run(MOVE_SPEED)
					end = time.perf_counter()
			rand = 1
		elif(rand == 1):
			while(end-start < 0.5):
				detect_line(cr,lw,rw)
				lw.run(-MOVE_SPEED)
				rw.run(MOVE_SPEED)
				end = time.perf_counter()
			rand = 2
		else:
			while(end-start < 0.5):
				detect_line(cr,lw,rw)
				lw.run(MOVE_SPEED)
				rw.run(-MOVE_SPEED)
				end = time.perf_counter()
			rand = 0
	if ball_location == 0:
		lw.run(MOVE_SPEED/(5*strength))
		rw.run(MOVE_SPEED)
	if ball_location == 1:
		rand = 0
		lw.run(MOVE_SPEED/(4*strength))
		rw.run(MOVE_SPEED)
	if ball_location == 2:
		rand = 0
		lw.run(MOVE_SPEED)
		rw.run(MOVE_SPEED)
	if ball_location == 3:
		rand = 0
		lw.run(MOVE_SPEED)
		rw.run(MOVE_SPEED/(4*strength))
	if ball_location == 4:
		rand = 0
		lw.run(MOVE_SPEED)
		rw.run(MOVE_SPEED/(5*strength))
	return rand

# Write your program here.
gr.reset_angle(0)
ball_location = -1
rand = 0
print_slow = 0
angle_flag = 0
while 1:
	ev3.screen.print( maxidx(ir.get_strength()))
	if angle_flag == 0:
		same_angle_time1 = time.perf_counter()
		same_angle1 = gr.angle()
		angle_flag = 1
	if gr.angle() == same_angle1 and angle_flag == 1:
		same_angle_time2 = time.perf_counter()
		if same_angle_time2-same_angle_time1 >= 3:	
			lw.run_time(-MOVE_SPEED, 700, wait = False)
			rw.run_time(-MOVE_SPEED, 700, wait = True)
			lw.run_time(MOVE_SPEED, 700, wait = False)
			rw.run_time(-MOVE_SPEED, 700, wait = True)
			angle_flag = 0
	if gr.angle() != same_angle1:
		angle_flag = 0
	
	(ball_location,strength) = maxidx(ir.get_strength())
	if sonic.distance() < 220 and ball_location == -1:
		lw.run_time(-MOVE_SPEED, 500, wait = False)
		rw.run_time(-MOVE_SPEED, 500, wait = True)
		# back up from wall and turn
		lw.run_time(MOVE_SPEED, 500, wait = False)
		rw.run_time(-MOVE_SPEED, 500, wait = True)
		detect_ball = -1
		start = time.perf_counter()
		end=0
		while detect_ball == -1 and (end - start) < 2:	
			lw.run(MOVE_SPEED/1.5)
			rw.run(-MOVE_SPEED/1.5)
			(_,detect_ball) = maxidx(ir.get_strength())
			end = time.perf_counter()
			# ev3.screen.print(end - start)
			reset(gr)
	elif sonic.distance() < 220 and ball_location != -1:
		if gr.angle() in range(25,155) or gr.angle() in range(-245, -335):
			rw.run_time(MOVE_SPEED, 500, wait = False)
			lw.run_time(-MOVE_SPEED, 500, wait = True)
		elif gr.angle() in range(-155, -25) or gr.angle() in range(335, 245):
			lw.run_time(MOVE_SPEED, 500, wait = False)
			rw.run_time(-MOVE_SPEED, 500, wait = True)
		else:
			lw.run_time(-MOVE_SPEED, 500, wait = False)
			rw.run_time(-MOVE_SPEED, 500, wait = True)
			# back up from wall and turn
			lw.run_time(MOVE_SPEED, 500, wait = False)
			rw.run_time(-MOVE_SPEED, 500, wait = True)
		detect_ball = -1
		start = time.perf_counter()
		end=0
		reset(gr)

	# ev3.screen.print(ball_location)
	reset(gr)
	rand = ball_folling(lw,rw,ball_location,cr,gr,rand,strength)
	# crossed the goal line
	detect_line(cr,lw,rw)
	print_slow += 1
	
	


