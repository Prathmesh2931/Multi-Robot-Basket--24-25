from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, SetEnvironmentVariable, 
                            IncludeLaunchDescription, SetLaunchConfiguration)
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    gz_share = get_package_share_directory('ros_gz_sim')
    pkg_share = get_package_share_directory('rbcon_sim')
    
    defaultWorld = PathJoinSubstitution([pkg_share, "sdf", "basketball_arena.sdf"])
    

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(PathJoinSubstitution([gz_share, 'launch', 'gz_sim.launch.py'])),
                    launch_arguments=[("gz_args", defaultWorld)]
            )
    

    bridge_config = PathJoinSubstitution([pkg_share, "config", "bridge_config.yaml"])
    ros_ign_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge', parameters=[{"config_file": bridge_config}])


    return LaunchDescription([
        gazebo,
        ros_ign_bridge
    ])
