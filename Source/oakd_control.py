import cv2 as cv2

class OAKDControl():
	def __init__(self, image_width=320, image_height=180):
		assert image_width > 0 and image_height > 0

		self.dai = __import__('depthai')

		# Create pipeline
		self.pipeline = self.dai.Pipeline()

		# Define the source and the output
		camRgb = self.pipeline.create(self.dai.node.ColorCamera)
		xoutRgb = self.pipeline.create(self.dai.node.XLinkOut)
		xoutRgb.setStreamName("rgb")

		# Set relevant properties of camera pipeline
		camRgb.setPreviewSize(image_width, image_height)
		camRgb.setInterleaved(False)
		camRgb.setColorOrder(self.dai.ColorCameraProperties.ColorOrder.RGB)
		camRgb.setFps(20)

		# Link the preview to the output
		camRgb.preview.link(xoutRgb.input)

		# Connect to device and start pipeline
		self.device = self.dai.Device(self.pipeline)

		# Output queue will be used to get the rgb frames from the output defined above
		self.qRgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

	def get_frame(self):
		# Wait until new data has arrived, blocking call
		inRgb = self.qRgb.get()
		return inRgb.getCvFrame()

class OAKDControl_Dummy():
	def __init__(self, file_name, image_width=320, image_height=180):
		# Store the video file's name
		assert type(file_name) is str
		self.file_name = file_name

		# Store the image height and width for resizing
		self.image_width = image_width
		self.image_height = image_height

		# Create a video capture object
		self.video = cv2.VideoCapture(self.file_name)

	def get_frame(self):
		# Return a frame from the video that has been resized to match spec
		return cv2.resize(self.video.read()[1], (self.image_width, self.image_height))