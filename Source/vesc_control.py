class VESCControl():
	def __init__(self, serial_port, has_sensor=False, start_heartbeat=True, baudrate=115200, timeout=0.05):
		self.pyvesc = __import__('pyvesc')
		self.vesc = self.pyvesc.VESC(serial_port, has_sensor, start_heartbeat, baudrate, timeout)

	def set_servo(self, angle):
		assert angle >= 0 and angle <= 1
		self.vesc.set_servo(angle)
		
	def set_throttle(self, throttle):
		assert throttle >= -1 and throttle <= 1
		self.vesc.set_duty_cycle(throttle)

	def reset(self):
		self.set_servo(0.5)
		self.set_throttle(0)

class VESCControl_Dummy():
	def __init__(self):
		pass

	def set_servo(self, angle):
		pass

	def set_throttle(self, throttle):
		pass

	def reset(self):
		pass