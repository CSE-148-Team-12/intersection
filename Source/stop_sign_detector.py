import cv2 as cv2
import numpy as np
from util import RunningAverager

class StopSignDetector():
	def __init__(self, threshold = 65, depth_radius = 5, min_bbox_size = (20, 20), history_len = 10, 
			bbox_color = (255, 255, 255), bbox_font_color = (255, 255, 255), bbox_thickness = 2):
		self.bbox_color = bbox_color
		self.bbox_thickness = bbox_thickness
		self.bbox_font_color = bbox_font_color
		self.depth_radius = depth_radius
		self.min_bbox_size = min_bbox_size
		self.threshold = threshold
		self.history_len = history_len
		self.averager = RunningAverager(history_len = self.history_len)

	"""
	Uses an XML stop sign detector to create a bounding box around the stop sign
	@param frame the frame to process
	@return (frame, bboxes) tuple containing frame and list of bounding box tuples
	"""
	def xml_detector(self, frame):
		# Convert to gray and run the cascade classifier to find octagons
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
		stop_data = cv2.CascadeClassifier('Data/stop_sign.xml')
		found = stop_data.detectMultiScale(frame_gray, minSize = self.min_bbox_size)
		bboxes = []
		if len(found) > 0:
			# Iterate over bounding boxes
			for (x, y, width, height) in found:

				# Draw a rectangle on the raw frame
				frame = cv2.rectangle(frame, (x + height, y + width), (x, y),  
					self.bbox_color, self.bbox_thickness)

				# Add the bounding box to the bbox list
				bboxes.append((x, y, x + height, y + width))
		else:
			# If there are no bounding boxes, return None
			return (frame, None)
		return (frame, bboxes)

	"""
	Compute the average depth map value of the stop sign
	@param depth the depth map
	@param bbox the bounding box
	@return (depth, int) depth frame with rectangle and a number representing the 
		average depth to the stop sign
	"""
	def find_average_bbox_depth(self, depth, bbox):
		# Check that the box is big enough for us to compute a center of radius depth_radius
		assert bbox[3] - bbox[1] > self.depth_radius * 2
		assert bbox[2] - bbox[0] > self.depth_radius * 2

		# Crop the depth map to contain only the stop sign
		stop_sign = depth[bbox[1]:bbox[3], bbox[0]:bbox[2]]

		# Find the center of the stop sign
		midpoint = (int(stop_sign.shape[0] / 2), int(stop_sign.shape[1] / 2))
		upper_bound = (midpoint[0] + self.depth_radius, midpoint[1] + self.depth_radius)
		lower_bound = (midpoint[0] - self.depth_radius, midpoint[1] - self.depth_radius)

		# Crop a box with radius self.depth_radius around the midpoint
		stop_sign = stop_sign[lower_bound[1]:upper_bound[1], lower_bound[0]:upper_bound[0]]

		# Compute the average depth
		bbox_depth = np.mean(stop_sign)

		# Draw the filter on the full depth frame
		cv2.rectangle(depth, (lower_bound[0] + bbox[0], lower_bound[1] + bbox[1]), 
			(upper_bound[0] + bbox[0], upper_bound[1] + bbox[1]), self.bbox_color, self.bbox_thickness)

		# Average the depth in the new cropped box
		return (depth, bbox_depth)

	"""
	Iterates over all of the bboxes to find the one with the minimum depth
	We only want to keep the bbox closest to us (current stop sign)
	@param depth the depth frame
	@param bboxes the list of bboxes
	@return (min_depth, bbox) the depth to the closest bbox and the closest bbox
	"""
	def find_min_bbox_depth(self, depth, bboxes):
		# This is a depth map, so we want bigger values
		min_depth, closest_bbox = -1, None

		# Iterate over the bounding boxes
		for bbox in bboxes:

			# Compute the average depth to this stop sign
			depth, bbox_depth = self.find_average_bbox_depth(depth, bbox)

			# If this stop sign is the closest, make it the min depth
			if bbox_depth > min_depth:
				min_depth = bbox_depth
				closest_bbox = bbox

			# Draw a bbox on the depth frame
			depth = cv2.rectangle(depth, (bbox[0], bbox[1]), (bbox[2], bbox[3]),  
				self.bbox_color, self.bbox_thickness)
			depth = cv2.putText(depth, f"{bbox_depth}", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, self.bbox_font_color)

		return (depth, min_depth, closest_bbox)
		

	"""
	Returns a boolean of whether we should stop
	@param frame the raw image frame
	@param detections the detections of the neural network
	@param show_image whether to imshow the stop sign bounding box
	@return boolean representing whether we should stop
	"""
	def detect_stop_sign(self, frame, depth, show_image = False):
		# Draw bounding boxes using the detections
		box_frame, bboxes = self.xml_detector(frame)

		# If we don't see a stop sign at all, return
		if bboxes is None:
			return None

		# Find the minimum depth bounding box
		depth, stop_sign_distance, bbox = self.find_min_bbox_depth(depth, bboxes)

		# Draw highlight boxes to signify the chosen stop sign
		box_frame = cv2.rectangle(box_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]),  
				(0, 0, 255), self.bbox_thickness)

		# If we are drawing bboxes on the pixels used for depth computations
		if show_image:
			cv2.imshow("Depth map computation", depth)
			cv2.imshow("Stop Sign Detection", box_frame)

		# Implement averaging for the last several values
		stop_sign_distance = self.averager.update(stop_sign_distance)

		return stop_sign_distance > self.threshold