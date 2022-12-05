import cv2 as cv2
import numpy as np
from util import RunningAverager

class StopSignDetector():
	def __init__(self, threshold = 650, history_len = 10, bbox_color = (255, 255, 255), bbox_thickness = 2, bbox_font_color = (255,255,255)):
		self.labelMap = [
			"person",         "bicycle",    "car",           "motorbike",     "aeroplane",   "bus",           "train",
			"truck",          "boat",       "traffic light", "fire hydrant",  "stop sign",   "parking meter", "bench",
			"bird",           "cat",        "dog",           "horse",         "sheep",       "cow",           "elephant",
			"bear",           "zebra",      "giraffe",       "backpack",      "umbrella",    "handbag",       "tie",
			"suitcase",       "frisbee",    "skis",          "snowboard",     "sports ball", "kite",          "baseball bat",
			"baseball glove", "skateboard", "surfboard",     "tennis racket", "bottle",      "wine glass",    "cup",
			"fork",           "knife",      "spoon",         "bowl",          "banana",      "apple",         "sandwich",
			"orange",         "broccoli",   "carrot",        "hot dog",       "pizza",       "donut",         "cake",
			"chair",          "sofa",       "pottedplant",   "bed",           "diningtable", "toilet",        "tvmonitor",
			"laptop",         "mouse",      "remote",        "keyboard",      "cell phone",  "microwave",     "oven",
			"toaster",        "sink",       "refrigerator",  "book",          "clock",       "vase",          "scissors",
			"teddy bear",     "hair drier", "toothbrush"
		]
		self.bbox_color = bbox_color
		self.bbox_thickness = bbox_thickness
		self.bbox_font_color = bbox_font_color
		self.threshold = threshold
		self.history_len = history_len
		self.averager = RunningAverager(history_len = self.history_len)

	"""
	Get a single bounding box representing a stop sign
	@return bbox a list of four elements representing the box
		xmin, ymin, xmax, ymax
	"""
	def get_avg_bounding_box(self, frame, detections):
		xmin, xmax, ymin, ymax, confidence, count = 0, 0, 0, 0, 0, 0
		found_stop_sign = False
		# Compute average xmin, xmax, ymin, and ymax for stop signs
		for detection in detections:
			if self.labelMap[detection.label] == "stop sign" and detection.confidence > 50:
				found_stop_sign = True
				xmin += detection.xmin
				ymin += detection.ymin
				xmax += detection.xmax
				ymax += detection.ymax
				confidence += detection.confidence
				count += 1
		# If we didn't find a box, return None
		if not found_stop_sign:
			return None
		return list(np.array([xmin, ymin, xmax, ymax, confidence]) / count)

	def get_minmax_bounding_box(self, frame, detections):
		bbox = [frame.shape[0], frame.shape[1], 0, 0, 0]
		for detection in detections:
			if detection.xmin < bbox[0]:
				bbox[0] = detection.xmin
			if detection.ymin < bbox[1]:
				bbox[1] = detection.ymin
			if detection.xmax > bbox[2]:
				bbox[2] = detection.xmax
			if detection.ymax > bbox[3]:
				bbox[3] = detection.ymax
			bbox[4] += detection.confidence
		if len(detections) != 0:
			bbox[4] = bbox[4] / len(detections)
		return bbox

	# nn data, being the bounding box locations, are in <0..1> range - they need to be normalized with frame width/height
	def frame_norm(self, frame, bbox):
		normVals = np.full(len(bbox), frame.shape[0])
		normVals[::2] = frame.shape[1]
		return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

	def draw_bounding_boxes(self, frame, detections):
		bbox = self.get_avg_bounding_box(frame, detections)
		# If we didn't find a stop sign, return no bounding box
		if bbox == None:
			return (frame, None)
		
		# Store confidence and normalize the bbox to fit the image
		confidence = bbox[4]
		bbox = self.frame_norm(frame, (bbox[0], bbox[1], bbox[2], bbox[3]))

		# Draw a bounding box on the image
		cv2.putText(frame, f"{int(confidence)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, self.bbox_font_color)
		frame = cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), self.bbox_color, self.bbox_thickness)
		return (frame, bbox)

	"""
	Returns a boolean of whether we should stop
	@param frame the raw image frame
	@param detections the detections of the neural network
	@param show_image whether to imshow the stop sign bounding box
	@return boolean representing whether we should stop
	"""
	def detect_stop_sign(self, frame, detections, show_image = False):
		# Draw bounding boxes using the detections
		box_frame, bbox = self.draw_bounding_boxes(frame, detections)
		
		# If we don't see a stop sign at all, return
		if bbox is None:
			return False

		# Draw images if required
		if show_image:
			cv2.imshow("Stop Sign Detection", box_frame)
			cv2.waitKey(50)

		# Compute the size of the bounding box and update the running average
		stop_sign_size = (bbox[3] - bbox[1]) * (bbox[2] - bbox[0])
		stop_sign_size = self.averager.update(stop_sign_size)
		print(stop_sign_size)

		# Stop if we see a stop sign
		return stop_sign_size > self.threshold