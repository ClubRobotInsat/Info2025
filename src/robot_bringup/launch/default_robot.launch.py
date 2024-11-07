from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, LaunchConfigurationEquals, LaunchConfigurationNotEquals


def generate_launch_description():
    description_launch_path = PathJoinSubstitution(
        [FindPackageShare('robot_description'), 'launch', 'description.launch.py']
    )
    
    robot_control_path = PathJoinSubstitution(
        [FindPackageShare('robot_control'), 'launch', 'robot_control.launch.py']
    )
    
    can_path = PathJoinSubstitution(
        [FindPackageShare('robot_bringup'), 'launch', 'can_simu.launch.py']
    )


    return LaunchDescription([
       
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(description_launch_path)
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(can_path)
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(robot_control_path)
        )
    ])