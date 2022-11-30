# Import misc packages
from sys import argv
import cv2 as cv2

# Import relevant sections of the codebase
from vesc_control import VESCControl, VESCControl_Dummy
from oakd_control import OAKDControl, OAKDControl_Dummy

class Robot:
	def __init__(self, args):
		# Hyperparameters belong in this section
		self.image_width = 320
		self.image_height = 180

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

		# Initialize related objects (e.g. line follower)
	
	"""
	Main function for running through the intersection.
	Handles line following, stopping at stopsign, etc
	Please write the majority of the code in other files (e.g. stop_sign_detector.py)
	"""
	def run_intersection(self):
		while(True):
			try:
				# All loop body code belongs in here
				# Hyperparameters belong in the init function
				cv2.imshow("Frame", self.camera.get_frame())
				cv2.waitKey(33)


			except KeyboardInterrupt:
				break
		print("Task completed.")

robot = Robot(argv)
robot.run_intersection()