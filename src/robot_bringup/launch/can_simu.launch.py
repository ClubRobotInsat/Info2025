import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch.actions import RegisterEventHandler
from launch.event_handlers.on_process_start import OnProcessStart
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():

    can_rx = Node(
        package='can_robot',
        executable='can_rx',
        output='screen'
    )

    can_tx = Node(
        package='can_robot',
        executable='can_tx',
        output='screen'
    )

    return LaunchDescription([
        can_tx,
        can_rx,
    ])
    