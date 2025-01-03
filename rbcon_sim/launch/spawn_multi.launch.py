from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, SetEnvironmentVariable, 
                            IncludeLaunchDescription, SetLaunchConfiguration)
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

import os
def generate_launch_description():
    gz_share = get_package_share_directory('ros_gz_sim')
    pkg_share = get_package_share_directory('rbcon_sim')
    
    posx = LaunchConfiguration('x')
    posy2 = LaunchConfiguration('y2')
    posy = LaunchConfiguration('y')
    posz = LaunchConfiguration('z')

    posx_arg = DeclareLaunchArgument(
        'x',
        default_value='0.0'
    )
    posy2_arg = DeclareLaunchArgument(
        'y2',
        default_value='2.0'
    )
    posy_arg = DeclareLaunchArgument(
        'y',
        default_value='0.0'
    )
    posz_arg = DeclareLaunchArgument(
        'z',
        default_value='2.0'
    )
    
    spawner = Node(package="ros_gz_sim", executable="create", arguments=['-topic', '/r1/robot_description', 
                                                                         '-x', posx,
                                                                         '-y', posy,
                                                                         '-z', posz,
                                                                         '-name', 'r1'
                                                                         ])
    spawner2 = Node(package="ros_gz_sim", executable="create", arguments=['-topic', '/r2/robot_description', 
                                                                         '-x', posx,
                                                                         '-y', posy2,
                                                                         '-z', posz,
                                                                         '-name', 'r2'
                                                                         ])


    return LaunchDescription([
        posx_arg,        
        posy_arg,        
        posz_arg,        
        posy2_arg,        
        spawner,
        spawner2,
        
    ])
