# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch.actions import (DeclareLaunchArgument, SetEnvironmentVariable, 
#                             IncludeLaunchDescription, SetLaunchConfiguration)
# from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution
# from launch_ros.actions import Node
# from launch.launch_description_sources import PythonLaunchDescriptionSource

# def generate_launch_description():
#     gz_share = get_package_share_directory('ros_gz_sim')
#     pkg_share = get_package_share_directory('rbcon_sim')
    
#     defaultWorld = PathJoinSubstitution([pkg_share, "sdf", "basketball_arena.sdf"])
    

#     gazebo = IncludeLaunchDescription(
#                 PythonLaunchDescriptionSource(PathJoinSubstitution([gz_share, 'launch', 'gz_sim.launch.py'])),
#                     launch_arguments=[("gz_args", defaultWorld)]
#             )
    

#     bridge_config = PathJoinSubstitution([pkg_share, "config", "bridge_config.yaml"])
#     ros_ign_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge', parameters=[{"config_file": bridge_config}])


#     return LaunchDescription([
#         gazebo,
#         ros_ign_bridge
#     ])


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

    default_world = PathJoinSubstitution([pkg_share, "sdf", "basketball_arena.sdf"])

    # Set Ignition environment variables for debugging
    ign_resource_path = SetEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH', 
        TextSubstitution(text=os.path.join(pkg_share, 'models'))
    )

    ign_system_plugin_path = SetEnvironmentVariable(
        'IGN_GAZEBO_SYSTEM_PLUGIN_PATH',
        TextSubstitution(text='/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins')
    )

    ign_debug = DeclareLaunchArgument(
        'ign_debug',
        default_value='4',  # Verbose level 4
        description='Set Ignition Gazebo verbosity level'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([gz_share, 'launch', 'gz_sim.launch.py'])),
        launch_arguments=[
            ("gz_args", [default_world, " -r -v ", LaunchConfiguration('ign_debug')])  # -r (run), -v 4 (verbose)
        ]
    )

    bridge_config = PathJoinSubstitution([pkg_share, "config", "bridge_config.yaml"])
    
    ros_ign_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{"config_file": bridge_config}],
        output="screen"
    )

    return LaunchDescription([
        # ign_resource_path,
        # ign_system_plugin_path,
        ign_debug,
        gazebo,
        ros_ign_bridge
    ])
