def reward_function(params):
    '''
    Dynamic speed threshold and distance. Speed reward
    has an extra weight of 3 at the end of the function.
    ABS_STEERING_THRESHOLD penalize distance to avoid zig-zag
    '''
    
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    abs_steering = abs(params['steering_angle']) # Only need the absolute steering angle
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    
    
    MIN_REWARD = 1e-3
    # Set the speed threshold based your action space
    SPEED_THRESHOLD = 1.0
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15 

    # dynamic distance reward
    distance_reward = 1- (distance_from_center/track_width*0.5)**0.4 

    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        distance_reward*= 0.8

    # dynamic speed reward
    speed_diff = abs(1.0-speed)
    max_speed_diff = 0.2#set it carefully in range [0.01,0.3]

    max_speed_diff = 0.2
    speed_diff = abs(1.0-speed) 
    speed_reward = max(MIN_REWARD, 1-((speed_diff/max_speed_diff)**0.5 ))
        
    reward = distance_reward + speed_reward*3

    return float(reward)