class Timer:
    def __init__(self, wait_time):
        self.current_time = 0
        # current time that has passed
        self.wait_time = wait_time
        # time to wait for
        self.frame_count = 0
        # current frame
        self.count_down_time = 0
        # time until time is up

    def reset_timer(self):
        self.frame_count = 0
        # reset the timer for new use

    def time_check(self, frame_rate):
        self.frame_count += 1
        # increase frame count by 1
        self.current_time = self.frame_count / frame_rate
        # set the current time to the frame count over the frame rate (get frames per second as to be 1 frame for x seconds passed)

        self.count_down_time = self.wait_time - self.current_time
        # set the count down time to the wait time - the time that has passed

        if self.count_down_time <= 0:
            self.reset_timer()
            return True
        else:
            return False
        # reset the timer if it hits 0 by default