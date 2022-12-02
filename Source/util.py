class RunningAverager():
	def __init__(self, history_len = 10, initial_value = 0):
		self.history_len = history_len
		self.initial_value = initial_value
		self.state = [self.initial_value] * self.history_len

	"""
	Add a new value and compute a new average
	@param value the latest value
	@return the average of the last history_len values
	"""
	def update(self, value):
		for i in range(self.history_len - 1):
			self.state[i] = self.state[i + 1]
		self.state[-1] = value
		return sum(self.state) / self.history_len

	"""
	Reset the state of the averager
	"""
	def reset(self):
		self.state = [self.initial_value] * self.history_len
