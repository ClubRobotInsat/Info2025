#!/usr/bin/python3

import rclpy
from rclpy.node import Node
import math
from std_msgs.msg import Float64MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import threading
import numpy as np
from geometry_msgs.msg import Quaternion
from tf_transformations import quaternion_from_euler


# Shared axes for velocity commands: [linear_x, linear_y, angular_z]
# For differential drive, linear_y is typically unused
axes = np.array([0,0,0], float) # (x,y,theta)

class Commander(Node):

    def __init__(self):
        super().__init__('commander')
        
        # Initialize wheel velocities
        self.wheel_vel = np.array([0,0,0,0], float)
        
        # Publishers
        self.publisher_ = self.create_publisher(Float64MultiArray, '/forward_velocity_controller/commands', 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)

        # Timer for control loop (200 Hz)
        timer_period = 0.005
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Robot parameters
        self.L = 0.135 # REAL distance from the robot center to wheel
        self.Rw = 0.041 # Radius ot the wheel

        # Scaling factors
        self.linear_vel_scale = 1.0 * 4.0 / 9.0 * 0.1 # m/s # Goal: 0.4m/s, going 0.9m/s
        self.angular_vel_scale = 1.0 * 4.0 / 9.0 * 0.1 # rad/s

        # Odometry variables
        self.prev_time = self.get_clock().now()
        self.x = 0.0 # Position x in meters
        self.y = 0.0 # Position y in meters
        self.theta = 0.0 # Orientation in radians

    def timer_callback(self):
        global axes

        # Extract velocities from axes
        v = axes[0] * self.linear_vel_scale # Linear velocity in m/s
        # y-axis is not used in differential drive
        omega = axes[2] * self.angular_vel_scale # Angular velocity in rad/s
  
        # Compute indivual wheel velocities
        # Differential drive kinematics
        v_left = (v - omega * self.L) / self.Rw
        v_right = -(v + omega * self.L) / self.Rw  
        
        self.wheel_vel[0] = v_left
        self.wheel_vel[2] = v_right      
        
        # Publish wheel velocities
        array_forPublish = Float64MultiArray(data=self.wheel_vel)
        self.publisher_.publish(array_forPublish)

        # Compute odometry
        current_time = self.get_clock().now()
        dt = (current_time - self.prev_time).nanoseconds / 1e9 # in seconds
        self.prev_time = current_time
        
        # Compute linear and angular velocities based on wheel velocities
        v_odom = (v_left + v_right) * self.Rw / 2.0
        omega_odom = (v_right - v_left) * self.Rw / self.L
        
        # Update robot pose
        delta_x = v_odom * math.cos(self.theta) * dt
        delta_y = v_odom * math.sin(self.theta) * dt
        delta_theta = omega_odom * dt
        
        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta
        
        self.theta = (self.theta + math.pi) % (2*math.pi) - math.pi # Normalize theta between -pi and pi
        
        # Create quaternion from yaw angle
        q = quaternion_from_euler(0, 0, self.theta)
        
        # Populate odometry message
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        
        # Set position
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])
        
        # Set velocity
        odom.twist.twist.linear.x = v_odom
        odom.twist.twist.linear.y = 0.0
        odom.twist.twist.angular.z = omega_odom
        
        # Publish odometry message
        self.odom_pub.publish(odom)



class CmdVel_subscriber(Node):
    def __init__(self):
        super().__init__('cmd_vel_subscriber')
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.listener_callback, 10)
        self.subscription

    def listener_callback(self, data):
        global axes
        msg = f"I heard: {data.linear.x} {data.linear.y} {data.angular.z}"
        self._logger.info(msg)
        axes[0] = data.linear.x
        axes[1] = data.linear.y
        axes[2] = data.angular.z


if __name__ == '__main__':
    rclpy.init(args=None)

    commander = Commander()
    cmd_vel_subscriber = CmdVel_subscriber()

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(commander)
    executor.add_node(cmd_vel_subscriber)

    executor_thread = threading.Thread(target=executor.spin, daemon=True)
    executor_thread.start()
    rate = commander.create_rate(2)
    try:
        while rclpy.ok():
            rate.sleep()
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
    executor_thread.join()

