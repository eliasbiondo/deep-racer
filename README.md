# AWS DeepRacer Reward Function

This repository contains the implementation of a reward function for the AWS DeepRacer. The reward function is a critical component of the reinforcement learning model, as it provides feedback to the vehicle during the training process. The aim is to encourage the DeepRacer to stay on the track, drive at optimal speeds, align with the track's direction, and make steady progress.

## Reward Function Overview

The `reward_function` takes a dictionary of parameters as input and returns a floating-point number representing the reward. The parameters include the vehicle's distance from the center of the track, its speed, the steering angle, whether all wheels are on the track, the progress made, and the track's waypoints.

The function penalizes the vehicle for going off-track or steering too sharply, which could indicate potential oversteering or oscillation. Conversely, it rewards the vehicle for aligning with the track's direction and for faster speeds, with a bias toward higher speeds to encourage the model to increase speed appropriately.

## Parameters

The reward function uses the following parameters from the AWS DeepRacer environment:

- `track_width`: The width of the track.
- `distance_from_center`: The distance of the vehicle from the centerline of the track.
- `speed`: The current speed of the vehicle.
- `steering_angle`: The current steering angle of the vehicle.
- `all_wheels_on_track`: Flag to indicate if the vehicle has all wheels on the track.
- `progress`: The percentage of the track completed by the vehicle.
- `waypoints`: A list of waypoints defining the track.
- `closest_waypoints`: Indices of the closest waypoints ahead and behind the vehicle.
- `heading`: The vehicle's heading in degrees.

## Reward Strategy

The reward function employs the following strategy:

- **On-Track Check**: Penalizes the vehicle heavily if it goes off-track.
- **Distance From Center**: Penalizes the vehicle if it's too far from the centerline of the track.
- **Alignment**: Rewards the vehicle for aligning its heading with the track's direction.
- **Speed**: Rewards the vehicle for maintaining a higher speed, with a preference for even higher speeds.
- **Steering**: Penalizes the vehicle if the steering angle is too high, which can be indicative of oversteering.
- **Progress**: Rewards the vehicle for making progress along the track.

## Hyperparameters

The training of the AWS DeepRacer model utilizes the following hyperparameters:

- **Gradient descent batch size**: 64
- **Entropy**: 0.01
- **Discount factor**: 0.99
- **Loss type**: Huber
- **Learning rate**: 0.0003
- **Number of experience episodes between each policy-updating iteration**: 20
- **Number of epochs**: 10

## Action Space

The action space for the AWS DeepRacer is defined as follows:

- **Type**: Continuous
- **Speed**: [ 0.7 : 2.5 ] m/s
- **Steering angle**: [ -30 : 30 ] °

## Training Framework and Algorithm

The AWS DeepRacer model is trained using the following framework and algorithm:

- **Framework**: Tensorflow
- **Reinforcement learning algorithm**: Proximal Policy Optimization (PPO)
- **Training duration**: 4 hours

## Usage

To use this reward function, copy the code from `reward_function.py` into the AWS DeepRacer console's reward function editor. Train your model with the function to incentivize the desired behaviors outlined above.

## Contributing

Contributions to the reward function are welcome. If you have ideas on how to improve the function, please feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
