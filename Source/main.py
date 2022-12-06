# Import misc packages
from sys import argv
import cv2 as cv2
import numpy as np
from time import sleep

# Import relevant sections of the codebase
from vesc_control import VESCControl, VESCControl_Dummy
from oakd_control import OAKDControl, OAKDControl_Dummy
from stop_sign_detector import StopSignDetector
from line_follower import LineFollower
from util import RunningAverager
from turn_system import TurnSystem

class Robot:
	def __init__(self, args):
		# Hyperparameters belong in this section
		self.image_width = 640
		self.image_height = 360
		self.fps = 20
		
		# LineFollower arguments
		self.turn_divisor = 17500
		self.blue_green_crop = (-101, -1, 0, self.image_width)
		# Daytime thresholds
		#self.lower_blue = (90, 20, 160) #increased sat from 0 to 20
		#self.upper_blue = (140, 255, 255)
		#self.lower_green = (40, 20, 30) # reduced saturation from 100 to 20
		#self.upper_green = (80, 255, 255)
		# Night time thresholds
		#self.lower_blue = (90, 20, 100) # Increased threshold from 30 to 50
		#self.upper_blue = (140, 150, 255)
		#self.lower_green = (40, 40, 100)
		#self.upper_green = (80, 150, 150)
		# Night time thresholds 2
		#self.lower_blue = (90, 35, 100) # Increased threshold from 30 to 50
		#self.upper_blue = (140, 150, 255)
		self.lower_blue = (90, 35, 100)
		self.upper_blue = (140, 255, 255)
		self.lower_green = (40, 50, 80)
		self.upper_green = (80, 255, 255)


		# Stop sign algorithm parameters
		self.stop_sign_sleep = 0.9
		self.stop_sign_history_len = 5
		self.stop_sign_threshold = 45 # was working well on 50
		self.depth_radius = 5
		self.min_bbox_size = (40, 40)

		# Vesc parameters
		self.throttle = 0.03
		self.vesc_history_len = 4

		#turn parameters
		self.move_in_time = 0.2
		self.left_angle = 0.05
		self.straight_angle = 0.5
		self.right_angle = 1
		self.left_throttle = 0.025
		self.straight_throttle = 0.02
		self.right_throttle = 0.02
		self.left_sleep_time = 3
		self.straight_sleep_time = 2
		self.right_sleep_time = 2


		# Required constants belong in this section
		self.vesc_serial = '/dev/serial/by-id/usb-STMicroelectronics_ChibiOS_RT_Virtual_COM_Port_304-if00'

		# Check if we should try to drive the real car
		assert len(args) in [1, 2]
		self.dev_environment = len(args) > 1
		
		# Initialize relevant hardware
		if self.dev_environment:
			print("Initializing a development environment...")
			# Initialize dummy vesc and camera
			self.camera = OAKDControl_Dummy(file_name=argv[1], image_width=self.image_width, image_height=self.image_height)
			self.vesc = VESCControl_Dummy()
		else:
			print("Initializing a test environment...")
			# Initialize real vesc and camera
			self.camera = OAKDControl(image_width=self.image_width, image_height=self.image_height)
			#self.vesc = VESCControl_Dummy()
			self.vesc = VESCControl(self.vesc_serial)
			self.vesc.reset()
			

		# Initialize related objects (e.g. line follower)
		self.stop_sign_detector = StopSignDetector(threshold = self.stop_sign_threshold, depth_radius = self.depth_radius, 
			min_bbox_size = self.min_bbox_size, history_len = self.stop_sign_history_len)
		self.line_follower = LineFollower(turn_divisor = self.turn_divisor, crop = self.blue_green_crop,
			lower_blue = self.lower_blue, upper_blue = self.upper_blue, lower_green = self.lower_green,
			upper_green = self.upper_green)
		self.vesc_averager = RunningAverager(history_len = self.vesc_history_len, initial_value = 0.5)
		self.turn_system = TurnSystem(self.left_angle, self.straight_angle, self.right_angle, self.left_throttle, 
			self.straight_throttle, self.right_throttle, self.left_sleep_time, self.straight_sleep_time, self.right_sleep_time)

	def line_follow(self, frame, show_image = False):
		_, steering = self.line_follower.get_new_steering(frame, show_image = show_image)
		steering = self.vesc_averager.update(steering)
		self.vesc.set_servo(steering)
		self.vesc.set_throttle(self.throttle)
	
	"""
	Main function for running through the intersection.
	Handles line following, stopping at stopsign, etc
	Please write the majority of the code in other files (e.g. stop_sign_detector.py)
	"""
	def run_intersection(self):
		while(True):
			try:
				print("Following lines until a stop sign is reached")
				while(True):
					# Follow the lines until a stop sign is reached
					frame = self.camera.get_frame(show_image = False)
					depth = self.camera.get_depth(show_image = False)
					self.line_follow(frame, show_image = True)
					cv2.waitKey(int(1 / self.fps * 1000))

					# If we see a stop sign, break the loop
					if self.stop_sign_detector.detect_stop_sign(frame, depth, show_image = True):
						
						# Follow the lines for self.stop_sign_sleep seconds
						print(f'Following lines for {self.stop_sign_sleep} more seconds')
						for _ in range(0, int(self.stop_sign_sleep * self.fps)):							
							frame = self.camera.get_frame(show_image = True)
							self.line_follow(frame, show_image = False)
							cv2.waitKey(int(1 / self.fps * 1000))

						# Reset the vesc when we get to the line
						print("Stopping car")
						self.vesc.reset()
						break

				# Wait for user input and fetch required turing parameters once inputted
				steering, throttle, sleep_time = self.turn_system.input_turn()

				# Reset the vesc averager so we don't have old weightings
				self.vesc_averager.initial_value = steering
				self.vesc_averager.reset()

				self.vesc.set_throttle(self.throttle)
				sleep(self.move_in_time)

				# Set the vesc servo and throttle for sleep_time seconds
				self.vesc.set_servo(steering)
				self.vesc.set_throttle(throttle)
				sleep(sleep_time)

			except KeyboardInterrupt:
				break
		print("Task completed.")
		self.vesc.reset()

robot = Robot(argv)
robot.run_intersection()