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



def generate_launch_description():
    share_dir = get_package_share_directory('zeus_init')

    slamConfig = PathJoinSubstitution([share_dir, "config", "localizationConfig.yaml"])

    sync_slam = Node(
        package='slam_toolbox',
        executable='localization_slam_toolbox_node',
        name="slam_toolbox_localization",
        parameters=[slamConfig]
    )
    
    ekf_config = PathJoinSubstitution([share_dir, 'config', 'ekf.yaml'])
    robot_localization_node = Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[ekf_config]
)

    return LaunchDescription([
        sync_slam,
        robot_localization_node
    ])
