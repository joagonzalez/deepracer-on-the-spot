def reward_function(params):
    '''
    Example of penalize steering, which helps mitigate zig-zag behaviors
    '''
    
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    abs_steering = abs(params['steering_angle']) # Only need the absolute steering angle
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    
    # Set the speed threshold based your action space
    SPEED_THRESHOLD = 1.0

    # dynamic distance reward
    distance_reward = 1- (distance_from_center/track_width*0.5)

    # dynamic speed reward
    speed_diff = abs(1.0-speed)
    max_speed_diff = 0.2#set it carefully in range [0.01,0.3]

    if speed_diff < max_speed_diff:
        speed_reward = 1-(speed_diff/max_speed_diff)**1 
    else:
        speed_reward = 0.001 #never set negative or zero rewards
            
    reward = distance_reward + speed_reward

    return float(reward)