from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():
    description_launch_path = PathJoinSubstitution(
        [FindPackageShare('robot_description'), 'launch', 'description.launch.py']
    )


    default_robot_launch_path = PathJoinSubstitution(
        [FindPackageShare('robot_bringup'), 'launch', 'default_robot.launch.py']
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(default_robot_launch_path),
        )
    ])