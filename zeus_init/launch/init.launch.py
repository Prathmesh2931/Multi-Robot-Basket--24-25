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
    
    share_dir = FindPackageShare(package="zeus_init")
    launch_file_dir = os.path.join(get_package_share_directory('zeus_init'), 'launch')
    urdfPath = PathJoinSubstitution([FindPackageShare("zeus_description") , "urdf", "zeus.xacro"])
 

    robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            'robot_description': ParameterValue(Command(['xacro ', urdfPath]), value_type=str)
    }]
    )

    joint_States_config = PathJoinSubstitution([share_dir, "config", "joint_states.yaml"])
    
    joint_state_pub = Node(package='joint_state_publisher',
                           executable='joint_state_publisher',
                           parameters=[joint_States_config]
                        )



    lidar_launch_path = PathJoinSubstitution([FindPackageShare("rplidar_ros") , "launch", "rplidar_a1_launch.py"])
    lidar_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            lidar_launch_path
        ),
        launch_arguments=[("frame_id","base_link")]
    )

    camConfig=PathJoinSubstitution([share_dir,"config","cam_config.yaml"])
    joyConfig = PathJoinSubstitution([share_dir, "config", "joystick.yaml"])

    joy = Node(name="joy_node", package="joy", executable="joy_node",
               parameters=[joyConfig])

    cam_node = Node(name="usb_cam_node", package="usb_cam", executable="usb_cam_node_exe",parameters=[camConfig])

    teleop_joy = Node(name="teleop_node", package="teleop_twist_joy", executable="teleop_node", parameters=[joyConfig])



    ekfConfig = PathJoinSubstitution([share_dir, "config", "ekf.yaml"])
    
    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekfConfig]
    )


    return  LaunchDescription([
        # robot_state_pub,
        # joint_state_pub,
        # joy,
        # teleop_joy,
        # cam_node,
        lidar_node,
        # robot_localization_node,
        # cam_node
    ])
