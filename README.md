# M7 — Global Coordinate Velocity (ROS 2)

ROS 2 Python node that subscribes to `/joint_states`, estimates differential-drive robot velocity, and prints its X/Y velocity components in a global frame to the terminal.

## Output
- `Vx`: estimated global X velocity (m/s)
- `Vy`: estimated global Y velocity (m/s)
- `Omega`: angular velocity (rad/s)
- `Theta`: estimated heading (degrees)

## Requirements
- ROS 2 with `rclpy`
- `sensor_msgs`
- A robot/simulator publishing wheel joint velocities on `/joint_states`

## Configure robot joint names
The default parameters are:
- Wheel radius: `0.10 m`
- Wheel separation: `0.45 m`
- Left wheel joint: `base_left_wheel_joint`
- Right wheel joint: `base_right_wheel_joint`

Check the actual names first:
```bash
ros2 topic echo /joint_states
```

If your model uses different joint names, pass them as parameters when running the node.

## Build
Place this package directory under `~/ros2_ws/src/`, then run:
```bash
cd ~/ros2_ws
colcon build --packages-select simple_mover
source install/setup.bash
```

## Run
Start the robot simulation first, then:
```bash
ros2 run simple_mover global_velocity
```

Example with custom joint names:
```bash
ros2 run simple_mover global_velocity --ros-args \
  -p left_joint:=left_wheel_joint \
  -p right_joint:=right_wheel_joint \
  -p wheel_radius:=0.10 \
  -p wheel_separation:=0.45
```

## How it works
For wheel angular velocities `omega_left` and `omega_right`:
- `v = r * (omega_right + omega_left) / 2`
- `omega = r * (omega_right - omega_left) / L`
- `Vx = v * cos(theta)`
- `Vy = v * sin(theta)`

The heading `theta` is estimated by integrating `omega` from an initial heading of zero. This is dead reckoning, not an absolute global pose measurement, and can drift over time. For a more accurate global-frame velocity, use the simulator's odometry or TF pose/orientation if available.

## Troubleshooting
- If the node only says it is waiting, verify `/joint_states` is publishing.
- Confirm the left and right joint names match the names in the topic.
- The message must contain wheel velocities and valid, advancing timestamps.
- Check that wheel radius and separation match your robot model.
