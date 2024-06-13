'''
https://medium.com/@syedbelalhyder/learn-aws-deepracer-tricks-to-optimize-your-reward-function-170af9d40602
'''
import math

class Reward:
    def __init__(self, verbose=False, track_time=False):
        self.prev_speed = 0
        self.prev_steering_angle = 0
        
    def reward_fun(self, params):
        speed = params['speed']
        speed_reward = 0
        if (speed > self.prev_speed) and (self.prev_speed > 0):
            speed_reward += 10
        self.prev_speed = speed  # update the previous speed
        
        prev_steering_angle = self.prev_steering_angle
        steering_angle = params['steering_angle']
        self.prev_steering_angle = steering_angle
        steering_diff = abs(steering_angle - prev_steering_angle)
        
        reward_steering_smoothness = math.exp(-0.5 * steering_diff)
        
        
        reward = speed_reward + reward_steering_smoothness
        
        return reward  # return the calculated reward

reward_obj = Reward()


def angle_between_points(first_point, x, third_point):
    """Calculates the angle between two line segments formed by three points."""
    first_dx = first_point[0] - x
    first_dy = first_point[1] - 0
    third_dx = third_point[0] - x
    third_dy = third_point[1] - 0
    angle = math.atan2(third_dy, third_dx) - math.atan2(first_dy, first_dx)
    return math.degrees(angle)

def get_line_points(x1, y1, x2, y2, distance=0.1):
    dx = x2 - x1
    dy = y2 - y1
    line_length = math.sqrt(dx ** 2 + dy ** 2)
    num_points = int(line_length / distance) + 1
    x_steps = dx / (num_points - 1)
    y_steps = dy / (num_points - 1)
    line_points = [(x1 + i * x_steps, y1 + i * y_steps) for i in range(num_points)]
    return line_points

def find_next_three_waypoints(params):
    waypoints = params['waypoints']
    next_points = (list(range(params['closest_waypoint'][1], params['closest_waypoint'][1] + 3)))
    for i in range(len(next_points)):
        if next_points[i] > len(waypoints):
            next_points[i] -= len(waypoints)
    return next_points



def reward_function(params):
    # PARAMS
    x = params['x']
    y = params['y']
    waypoints = params['waypoints']
    heading = params['heading']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # CONSTANTS
    MIN_REWARD = 1e-3
       
    ### PREV AND POST SPEED DATA REWARD
    reward_prev_post = reward_obj.reward_fun(params)

    next_points = find_next_three_waypoints(params)

    # Get Destination coordinates
    x_forward = waypoints[next_points[2]][0]
    y_forward = waypoints[next_points[2]][1]
    
    optimal_heading = math.degrees(math.atan2(y_forward - y, x_forward - x))
    heading_diff = abs(optimal_heading - heading)
    if heading_diff > 180:
        heading_diff = 360 - heading_diff
    
    reward_alignment = math.cos(math.radians(heading_diff))
    
    ### SPEED CURVATURE
    # Calculate curvature
    first_point = waypoints[next_points[0]]
    third_point = waypoints[next_points[2]]
    curvature = angle_between_points(first_point, x, third_point)

    # Optimal speed based on curvature
    min_speed, max_speed = 1, 4
    # Changed to continuous function for optimal speed calculation
    optimal_speed = max_speed - (curvature / 180) * (max_speed - min_speed)

    # Calculate reward for speed
    speed_diff = abs(params['speed'] - optimal_speed)
    reward_speed = math.exp(-0.5 * speed_diff)
        
    reward = reward_alignment*4 + reward_prev_post*3 + reward_speed*2
    
    return float(reward)