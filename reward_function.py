import math

def reward_function(params):
    """
    Calculates the reward for the AWS DeepRacer based on various parameters related to its position and movement on the track.

    The reward function encourages the vehicle to stay on track, maintain a direction aligned with the upcoming waypoint, 
    and maximize its speed, while penalizing excessive steering.

    Parameters:
    - params (dict): A dictionary containing several pieces of data provided by the AWS DeepRacer environment:
        - track_width (float): The width of the track.
        - distance_from_center (float): The distance of the vehicle from the centerline of the track.
        - speed (float): The current speed of the vehicle.
        - steering_angle (float): The current steering angle of the vehicle.
        - all_wheels_on_track (bool): Flag to indicate if the vehicle has all wheels on the track.
        - progress (float): The percentage of the track completed by the vehicle.
        - waypoints (list of tuples): A list of waypoints defining the track.
        - closest_waypoints (list of ints): Indices of the closest waypoints ahead and behind the vehicle.
        - heading (float): The vehicle's heading in degrees.

    Returns:
    - float: The calculated reward for the current state of the vehicle.
    """

    # Extracting parameters for calculations
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    steering = abs(params['steering_angle'])  # Use absolute value to simplify calculations
    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Starting with a base reward
    reward = 1.0

    # Penalize heavily if the vehicle is not on the track to discourage off-track driving
    if not all_wheels_on_track:
        return 1e-3  # Near-zero reward signals to the model that this is undesirable

    # Penalize if the vehicle is too far from the center, as it's close to going off-track
    if distance_from_center > track_width * 0.5:
        return 1e-3  # Again, a small reward to discourage this behavior

    # Calculate the direction of the track using the waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)  # Convert radians to degrees for comparison

    # Calculate the absolute difference between the track direction and vehicle's heading
    direction_diff = abs(track_direction - heading)
    
    # Reward the vehicle for being aligned with the track direction
    # The closer the vehicle's heading is to the track direction, the higher the reward
    direction_reward = max(1.0 - (direction_diff / 30.0), 0.0)
    reward *= direction_reward

    # Reward for higher speeds, squared to disproportionately favor higher speeds
    # This encourages the model to increase speed where appropriate
    speed_reward = speed ** 2
    reward += speed_reward

    # Define a threshold for penalizing high steering angles
    # High steering angles may indicate potential oversteering or oscillation
    ABS_STEERING_THRESHOLD = 15.0
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8  # Apply a penalty by reducing the reward

    # Reward incremental progress along the track
    # This helps to encourage the vehicle to make continuous progress
    progress_reward = progress / 100.0
    reward += progress_reward

    # Return the final reward value, ensuring it's a float for consistency
    return float(reward)