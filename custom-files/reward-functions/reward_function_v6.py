class Reward:
    def __init__(self, verbose=False, track_time=False):
        self.prev_speed = 0
        
    def reward_fun(self, params):
        speed = params['speed']
        reward = 0
        if (speed > self.prev_speed) and (self.prev_speed > 0):
            reward += 10
        self.prev_speed = speed  # update the previous speed
        return reward  # return the calculated reward

reward_obj = Reward()

def reward_function(params):
    reward = reward_obj.reward_fun(params)
    return float(reward)