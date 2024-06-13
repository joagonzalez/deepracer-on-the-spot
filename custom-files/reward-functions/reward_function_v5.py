def reward_function(params):
    '''
    Optimized for Bowtie_track
    '''
    
    # Read input parameters
    wp = params['closest_waypoints'][1]
    speed = params['speed']
    
    MIN_REWARD = 1e-3
    
    if wp in (list(range(70,128)) + list(range(152, 49))):
        if speed >= 2:
            return MIN_REWARD

    return speed