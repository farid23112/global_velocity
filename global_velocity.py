#!/usr/bin/env python3
"""Estimate and print differential-drive robot velocity in global coordinates."""

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class GlobalVelocity(Node):
    def __init__(self):
        super().__init__("global_velocity")

        # Adjust these parameters to match the robot model.
        self.declare_parameter("wheel_radius", 0.10)
        self.declare_parameter("wheel_separation", 0.45)
        self.declare_parameter("left_joint", "base_left_wheel_joint")
        self.declare_parameter("right_joint", "base_right_wheel_joint")

        self.wheel_radius = float(self.get_parameter("wheel_radius").value)
        self.wheel_separation = float(
            self.get_parameter("wheel_separation").value
        )
        self.left_joint = str(self.get_parameter("left_joint").value)
        self.right_joint = str(self.get_parameter("right_joint").value)

        self.theta = 0.0
        self.last_time = None

        self.subscription = self.create_subscription(
            JointState, "/joint_states", self.joint_callback, 10
        )
        self.get_logger().info(
            "Global velocity node started; waiting for /joint_states."
        )

    def joint_callback(self, msg: JointState):
        try:
            left_idx = msg.name.index(self.left_joint)
            right_idx = msg.name.index(self.right_joint)
        except ValueError:
            # Joint names in this node must match the names published by the robot.
            return

        if len(msg.velocity) <= max(left_idx, right_idx):
            return

        omega_left = msg.velocity[left_idx]
        omega_right = msg.velocity[right_idx]

        # Differential-drive body-frame velocities.
        v = self.wheel_radius * (omega_right + omega_left) / 2.0
        omega = (
            self.wheel_radius
            * (omega_right - omega_left)
            / self.wheel_separation
        )

        stamp = msg.header.stamp
        current_time = stamp.sec + stamp.nanosec * 1e-9
        if current_time <= 0.0:
            self.get_logger().warn(
                "JointState timestamp is zero; waiting for valid timestamps.",
                throttle_duration_sec=5.0,
            )
            return

        if self.last_time is not None:
            dt = current_time - self.last_time
            if 0.0 < dt < 1.0:
                # Dead-reckoning estimate of heading, initialized at theta = 0.
                self.theta += omega * dt
                self.theta = math.atan2(
                    math.sin(self.theta), math.cos(self.theta)
                )

        self.last_time = current_time

        vx_global = v * math.cos(self.theta)
        vy_global = v * math.sin(self.theta)

        print(
            f"\rGlobal Velocity | "
            f"Vx: {vx_global:+.3f} m/s | "
            f"Vy: {vy_global:+.3f} m/s | "
            f"Omega: {omega:+.3f} rad/s | "
            f"Theta: {math.degrees(self.theta):+.1f} deg",
            end="",
            flush=True,
        )


def main(args=None):
    rclpy.init(args=args)
    node = GlobalVelocity()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\\nGlobal velocity node stopped.")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
