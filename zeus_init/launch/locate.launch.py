import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import GroupAction
from launch_ros.actions import Node, PushRosNamespace
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    share_dir = get_package_share_directory('zeus_init')

    # Paths to configuration files
    slam_config_1 = PathJoinSubstitution([share_dir, "config", "localizationConfig.yaml"])
    # slam_config_2 = PathJoinSubstitution([share_dir, "config", "localizationConfig_2.yaml"])
    ekf_config_1 = PathJoinSubstitution([share_dir, "config", "ekf.yaml"])
    # ekf_config_2 = PathJoinSubstitution([share_dir, "config", "ekf_2.yaml"])

    # Robot 1 Group
    robot1_group = GroupAction([
        # PushRosNamespace('r1'),
        Node(
            package='slam_toolbox',
            executable='localization_slam_toolbox_node',
            name="slam_toolbox_localization_1",
            parameters=[slam_config_1],
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_1',
            parameters=[ekf_config_1],
        ),
    ])

    # Robot 2 Group
    robot2_group = GroupAction([
        # PushRosNamespace('r2'),
        Node(
            package='slam_toolbox',
            executable='localization_slam_toolbox_node',
            name="slam_toolbox_localization_2",
            parameters=[slam_config_1],
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_2',
            parameters=[ekf_config_1],
        ),
    ])
    
    pose=Node(
            package='zeus_init',
            executable='pub_pose_r1.py',
            name='pub_pose_r1',
            output='screen',
            )

    return LaunchDescription([robot1_group, robot2_group,pose])
