class TurnSystem():
    def __init__(self, left_turn_angle, straight_angle, right_turn_angle, left_turn_throttle, 
            straight_throttle, right_turn_throttle, left_sleep_time, straight_sleep_time, right_sleep_time):
        # Initialize hardcoded turning parameters
        self.left_turn_angle = left_turn_angle
        self.straight_angle = straight_angle
        self.right_turn_angle = right_turn_angle
        self.left_turn_throttle = left_turn_throttle
        self.straight_throttle = straight_throttle
        self.right_turn_throttle = right_turn_throttle
        self.left_sleep_time = left_sleep_time
        self.straight_sleep_time = straight_sleep_time
        self.right_sleep_time = right_sleep_time

    def input_turn(self):
        input_dir = input("Detected stop sign. Awaiting user input...\n")
        if input_dir == 'a':
            return(self.left_turn_angle, self.left_turn_throttle, self.left_sleep_time)
        elif input_dir == 'd':
            return(self.right_turn_angle, self.right_turn_throttle, self.right_sleep_time)
        else:
            return(self.straight_angle, self.straight_throttle, self.straight_sleep_time)