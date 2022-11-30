import cv2 as cv2
import numpy as np

class LineFollower():
	def __init__(self, turn_divisor = 100000, crop = (0, 320, 0, 180), lower_blue = (90, 0, 30), upper_blue = (140, 255, 255),
				lower_green = (40, 0, 30), upper_green =  (80, 255, 255)):
		# HSV filter values for blue and green
		self.lower_blue = lower_blue
		self.upper_blue = upper_blue
		self.lower_green = lower_green
		self.upper_green = upper_green
		# Crop is (xmin, xmax, ymin, ymax)
		self.crop = crop
		self.turn_divisor = turn_divisor

	"""
	Computes the steering values for the car given a frame
	@param frame the BGR frame to process
	@return servo_angle the proposed angle of the servo
	"""
	def get_new_steering(self, frame):
		# Crop the image to a small region
		frame = frame[self.crop[2]:self.crop[3], self.crop[0]:self.crop[1], :]
		
		# Filter for blues and greens in the cropped region
		frame = self.filter_blue_green(frame)
		
		# Count the number of blues and greens
		green_count = np.count_nonzero(frame[1])
		blue_count = np.count_nonzero(frame[0])

		# Compare the two counts and generate steering values
		return np.clip((green_count - blue_count) / self.turn_divisor, -0.5, 0.5) + 0.5
	
	"""
	Filters for the colors blue and green in a frame
	@param frame the BGR frame to filter
	@return frame the filtered BGR frame
	"""
	def filter_blue_green(self, frame):
		# Convert to an HSV frame
		hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# Filter for blues and greens
		blue, red, green = cv2.split(frame)
		blue_mask = cv2.inRange(hsv_frame, self.lower_blue, self.upper_blue)
		blue = np.bitwise_and(blue, blue_mask)
		green_mask = cv2.inRange(hsv_frame, self.lower_green, self.upper_green)
		green = np.bitwise_and(green, green_mask)

		# Zero the red channel because we don't need it
		red = np.zeros_like(red)

		# Merge the filtered channels back together
		frame = cv2.merge([blue, green, red])
		return frame