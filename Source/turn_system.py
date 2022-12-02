class TurnSystem():
    def __init__(self, left_turn_angle, straight_angle, right_turn_angle, left_turn_throttle, straight_throttle, right_turn_throttle, time):
        self.left_turn_angle, self.straight_angle, self.right_turn_angle, self.left_turn_throttle, self.straight_throttle, self.right_turn_throttle, self.time = left_turn_angle, straight_angle, right_turn_angle, left_turn_throttle, straight_throttle, right_turn_throttle, time    

    def input_turn(self):
        input_dir = input("Detected stop sign. Awaiting user input...\n")
        if input_dir == 'w':
            return(self.straight_angle,self.straight_throttle, self.time)
        if input_dir == 'a':
            return(self.left_turn_angle,self.left_turn_throttle, self.time)
        if input_dir == 'd':
            return(self.right_turn_angle,self.right_turn_throttle, self.time)