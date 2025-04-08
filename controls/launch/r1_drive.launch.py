#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare 
from launch.substitutions import PathJoinSubstitution
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import ExecuteProcess
from launch.actions import DeclareLaunchArgument
from launch.actions import *
from launch_ros.actions import *

def generate_launch_description():
    drive_share=FindPackageShare(package="controls")
    uros_share=FindPackageShare(package="uros_init")
    name_arg=DeclareLaunchArgument("namespace",default_value="dhanush",description="namespace of Bots")
   
    namespace=LaunchConfiguration("namespace")
    joy = Node(name="joy_node", package="joy", executable="joy_node" , namespace=namespace)
    # joy = Node(name="joy_node", package="joy", executable="joy_node")

    teleop_config=PathJoinSubstitution([drive_share,"config","joystick.yaml"])
    teleop=Node(package="teleop_twist_joy" , executable="teleop_node" , name="teleop_node" ,parameters=[teleop_config] , namespace=namespace)

    # teleop_joy = Node(name="ps_control", package="dhanush", executable="ps_control.cpp", output='screen')
    # teleop_joy=ExecuteProcess(cmd=["ros2", "run", "controls", "dhanush_controls.py"], output='screen'  )  # Set namespace)
    control=ExecuteProcess(cmd=["ros2", "launch", "controls", "dhanush_control.py"], output='screen'  ,additional_env={"ROS_NAMESPACE": namespace})  # Set namespace)

    drive_system = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                drive_share, 'launch/common_drive.launch.py'
            ])]), launch_arguments=[("namespace","r1")])
    
    
    uros = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                uros_share, 'launch/init.launch.py'
            ])]))
    
    control_dhanush=Node(package="controls", executable="dhanush_control.py",namespace="r1")
    
    basket_tf=Node(package="sim_controller",executable="dist_basket",namespace="r1")
    
    allign_service=Node(package="service_handler",executable="bot_allign.py",namespace="r1")
    
    return  LaunchDescription([
        # name_arg,
        # joy,
        # teleop,
        # control,
        # uros,
        control_dhanush,
        drive_system,
        basket_tf,
        allign_service,
        
    ])
