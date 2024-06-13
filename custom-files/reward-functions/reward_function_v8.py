def reward_function(params):
    '''
    Optimized for Bowtie_track
    '''
    
    # Read input parameters
    wp = params['closest_waypoints'][1]
    speed = params['speed']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # weights for distinct reward types
    w1 = 4
    w2 = 1
    
    
    MIN_REWARD = 1e-3
    
    
    
    if wp in (list(range(70,128)) + list(range(152, 49))):
        if speed >= 2:
            return MIN_REWARD
     
    distance_from_center_scaled = distance_from_center / (track_width / 2.0)
        
    reward = (w1 * speed) + (w2 * distance_from_center_scaled)

    return reward

