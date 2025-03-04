from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, SetEnvironmentVariable, 
                            IncludeLaunchDescription, SetLaunchConfiguration)
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

import os
def generate_launch_description():
    desc_share = get_package_share_directory('shooting_set_description')
   
    
    dhanush_share =get_package_share_directory('DHANUSH_URDF_description')
    vyom_share=get_package_share_directory('vyom_new_description')
    
    
    
    # desc_share = get_package_share_directory('zeus_description')
    # gz_share = get_package_share_directory('ros_gz_sim')
    pkg_share = get_package_share_directory('rbcon_sim')
        

    display =  IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                vyom_share,
                'launch',
                'display.launch.py'
            ])
        ])
    )


    
    
    
    simulation =  IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                pkg_share,
                'launch',
                'rbcon_sim.launch.py'
            ])
        ])
    )
    

    spawn_multi =  IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                pkg_share,
                'launch',
                'spawn_multi.launch.py'
            ])
        ])
    )
    
    spawn_single =  IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                pkg_share,
                'launch',
                'spawn.launch.py'
            ])
        ])
    )

    return LaunchDescription([
        display,
        simulation,
        spawn_multi,
        # spawn_single
        # display_2
    ])
