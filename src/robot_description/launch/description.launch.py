import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, EnvironmentVariable
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    robot_base = os.getenv('ROBOT_BASE', '2wd')
    
    urdf_path = PathJoinSubstitution(
        [FindPackageShare('robot_description'), 'urdf/robots', f"{robot_base}.urdf.xacro"]
    )
    
    rviz_config_path = PathJoinSubstitution(
        [FindPackageShare('robot_description'), 'rviz', 'description.rviz']
    )
    
    return LaunchDescription([
        # Arguments
        DeclareLaunchArgument(
            name='urdf',
            default_value=urdf_path,
            description='URDF path',
        ),
        
        DeclareLaunchArgument(
            name='publish_joints',
            default_value='true',
            description='Launch joint_state_publisher',
        ),
        
        DeclareLaunchArgument(
            name='rviz',
            default_value='false',
            description='Launch rviz',
        ),
        
        DeclareLaunchArgument(
            name="use_sim_time",
            default_value="false",
            description="Use simulation (Gazebo) clock if true",
        ),
        
        # Nodes
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            condition=IfCondition(LaunchConfiguration('publish_joints')),
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time')
            }],
        ),
        
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'robot_description': ParameterValue(Command(['xacro ', LaunchConfiguration('urdf')]))
            }],
        ),
        
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            condition=IfCondition(LaunchConfiguration('rviz')),
            arguments=['-d', rviz_config_path],
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time')
            }],
        )
    ])
