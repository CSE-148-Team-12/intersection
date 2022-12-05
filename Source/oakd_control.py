import cv2 as cv2
import numpy as np

class OAKDControl():
	def __init__(self, image_width=320, image_height=180):
		assert image_width > 0 and image_height > 0

		self.dai = __import__('depthai')

		# Create pipeline
		self.pipeline = self.dai.Pipeline()

		# Define the source
		camRgb = self.pipeline.create(self.dai.node.ColorCamera)

		# Define the stereo depth perception
		monoLeft = self.pipeline.create(self.dai.node.MonoCamera)
		monoRight = self.pipeline.create(self.dai.node.MonoCamera)
		self.depth = self.pipeline.create(self.dai.node.StereoDepth)
		
		# Define the source output
		xoutRgb = self.pipeline.create(self.dai.node.XLinkOut)

		# Define the depth output
		xout = self.pipeline.create(self.dai.node.XLinkOut)

		# Name the streams
		xoutRgb.setStreamName("rgb")
		xout.setStreamName("depth")

		# Set relevant properties of camera pipeline
		camRgb.setPreviewSize(image_width, image_height)
		camRgb.setResolution(self.dai.ColorCameraProperties.SensorResolution.THE_720_P) # Previously THE_1080_P
		camRgb.setInterleaved(False)
		camRgb.setColorOrder(self.dai.ColorCameraProperties.ColorOrder.BGR)
		camRgb.setFps(20)

		# Set the resolutions of the mono cameras
		monoLeft.setResolution(self.dai.MonoCameraProperties.SensorResolution.THE_720_P)
		monoLeft.setBoardSocket(self.dai.CameraBoardSocket.LEFT)
		monoRight.setResolution(self.dai.MonoCameraProperties.SensorResolution.THE_720_P)
		monoRight.setBoardSocket(self.dai.CameraBoardSocket.RIGHT)

		# Set relevant properties of depth perception camera
		self.depth.setDefaultProfilePreset(self.dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
		self.depth.initialConfig.setMedianFilter(self.dai.MedianFilter.KERNEL_7x7)
		self.depth.setLeftRightCheck(True) # Better occlusion handling
		self.depth.setExtendedDisparity(True) # Closer-in minimum depth
		self.depth.setSubpixel(False) # Better accuracy for longer distances

		# Link the preview to the output
		camRgb.preview.link(xoutRgb)

		# Link the mono cameras to the depth perception
		monoLeft.out.link(self.depth.left)
		monoRight.out.link(self.depth.right)
		self.depth.disparity.link(xout.input)

		# Connect to device and start pipeline
		self.device = self.dai.Device(self.pipeline)

		# Output queue will be used to get the rgb frames from the output defined above
		self.qRgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
		self.q = self.device.getOutputQueue(name="depth", maxSize=4, blocking=False)

	def get_frame(self):
		# Wait until new data has arrived, blocking call
		inRgb = self.qRgb.get()
		return inRgb.getCvFrame()

	def get_depth(self):
		# return the depth
		inDep = self.q.get()
		frame = inDep.getCvFrame()
		frame = (frame * (255 / self.depth.initialConfig.getMaxDisparity())).astype(np.uint8)
		return frame #cv2.applyColorMap(frame, cv2.COLORMAP_JET)

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

	def get_depth(self):
		return cv2.resize(self.video.read()[1], (self.image_width, self.image_height))