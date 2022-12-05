import cv2 as cv2

class OAKDControl():
	def __init__(self, image_width=320, image_height=180):
		assert image_width > 0 and image_height > 0

		self.dai = __import__('depthai')

		self.nn_path = "Data/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob"

		# Create pipeline
		self.pipeline = self.dai.Pipeline()

		# Define the source
		camRgb = self.pipeline.create(self.dai.node.ColorCamera)

		# Define the detection network
		self.detectionNetwork = self.pipeline.create(self.dai.node.YoloDetectionNetwork)
		
		# Define the source output
		xoutRgb = self.pipeline.create(self.dai.node.XLinkOut)

		# Define the output of the neural netowrk
		nnOut = self.pipeline.create(self.dai.node.XLinkOut)

		# Name the streams
		xoutRgb.setStreamName("rgb")
		nnOut.setStreamName("nn")

		# Set relevant properties of camera pipeline
		camRgb.setPreviewSize(image_width, image_height)
		camRgb.setResolution(self.dai.ColorCameraProperties.SensorResolution.THE_1080_P)
		camRgb.setInterleaved(False)
		camRgb.setColorOrder(self.dai.ColorCameraProperties.ColorOrder.BGR)
		camRgb.setFps(20)
		
		# Define network specific settings
		self.detectionNetwork.setConfidenceThreshold(0.8)
		self.detectionNetwork.setNumClasses(80)
		self.detectionNetwork.setCoordinateSize(4)
		self.detectionNetwork.setAnchors([10, 14, 23, 27, 37, 58, 81, 82, 135, 169, 344, 319])
		self.detectionNetwork.setAnchorMasks({"side26": [1, 2, 3], "side13": [3, 4, 5]})
		self.detectionNetwork.setIouThreshold(0.7)
		self.detectionNetwork.setBlobPath(self.nn_path)
		self.detectionNetwork.setNumInferenceThreads(2)
		self.detectionNetwork.input.setBlocking(False)

		# Link the preview to the output
		camRgb.preview.link(self.detectionNetwork.input)
		self.detectionNetwork.passthrough.link(xoutRgb.input)
		self.detectionNetwork.out.link(nnOut.input)

		# Connect to device and start pipeline
		self.device = self.dai.Device(self.pipeline)

		# Output queue will be used to get the rgb frames from the output defined above
		self.qRgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
		self.qDet = self.device.getOutputQueue(name="nn", maxSize=4, blocking=False)

	def get_frame(self):
		# Wait until new data has arrived, blocking call
		inRgb = self.qRgb.get()
		return inRgb.getCvFrame()

	def get_detections(self):
		# Return the data from the neural network
		inDet = self.qDet.get()
		return inDet.detections

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