# Import misc packages
from sys import argv
import cv2 as cv2
import numpy as np
from vesc_control import *
from stop_sign_detector import *

# Import relevant sections of the codebase
from vesc_control import VESCControl, VESCControl_Dummy
from oakd_control import OAKDControl, OAKDControl_Dummy
from stop_sign_detector import StopSignDetector

class Robot:
	def __init__(self, args):
		# Hyperparameters belong in this section
		#self.image_width = 320
		#elf.image_height = 180

		self.image_width = 416
		self.image_height = 416
		self.throttle = .06

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
			self.vesc = VESCControl(self.vesc_serial)
			self.vesc.reset()

		# Initialize related objects (e.g. line follower)
		self.stop_sign_detector = StopSignDetector()
	
	"""
	Main function for running through the intersection.
	Handles line following, stopping at stopsign, etc
	Please write the majority of the code in other files (e.g. stop_sign_detector.py)
	"""
	def run_intersection(self):
		avg_len = 10
		stop_sign_size_list = [0 * avg_len]
		self.vesc.set_throttle(self.throttle)
		while(True):
			try:
				# All loop body code belongs in here
				# Hyperparameters belong in the init function
				frame = self.camera.get_frame()
				detections = self.camera.get_detections()
				frame, bbox = self.stop_sign_detector.draw_bounding_boxes(frame, detections)

				cv2.imshow("Frame", frame)
				cv2.waitKey(50)

				if bbox is None:
					continue
				
				frame = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
				cv2.imshow("Stop Sign", frame)

				stop_sign_size = frame.shape[0] * frame.shape[1]
				stop_sign_size_list[-1] = stop_sign_size
				for i in range(len(stop_sign_size_list) - 1):
					stop_sign_size_list[i] = stop_sign_size_list[i+1]
				stop_sign_size = sum(stop_sign_size_list) / avg_len
				print(stop_sign_size)

				if (stop_sign_size) > 650:
					self.vesc.set_throttle(0)
					break


			except KeyboardInterrupt:
				break
		print("Task completed.")

robot = Robot(argv)
robot.run_intersection()