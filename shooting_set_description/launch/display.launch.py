from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
import xacro
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('shooting_set_description')

    xacro_file = os.path.join(share_dir, 'urdf', 'shooting_set.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    vyom_xacro=os.path.join(share_dir, 'urdf', 'shooting_set.xacro')
    
    # Robot 1 URDF
    robot1_urdf = xacro.process_file(xacro_file,mappings={'robot_name': 'robot1'}).toxml()

    # Robot 2 URDF
    robot2_urdf = xacro.process_file(xacro_file, mappings={'robot_name': 'robot2'}).toxml()

    vyom_urdf=xacro.process_file(xacro_file, mappings={'robot_name': 'robot2'}).toxml()

    robot_urdf = robot_description_config.toxml()

    rviz_config_file = os.path.join(share_dir, 'config', 'display.rviz')

    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='True'
    )

    show_gui = LaunchConfiguration('gui')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot1_urdf},
            # { 'frame_prefix': 'r1_'}
        ],
        
        
        namespace='r1',
        remappings=[('/robot_description', '/r1_description'),]
                    # ('/joint_states', '/r1_joint_states')]

    )
    
    robot2_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot2_state_publisher',
        parameters=[
            {'robot_description': robot2_urdf},
            # { 'frame_prefix': 'r2_'}
        ],
        
        namespace='r2',
        remappings=[('/robot_description', '/r2_description')]
                    # ('/joint_states', '/r2_joint_states')]
    )
    
    test_robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': vyom_urdf},
            # { 'frame_prefix': 'r1_'}
        ],
        
        
        namespace='r1',
        remappings=[('/robot_description', '/r1_description'),]
                    # ('/joint_states', '/r1_joint_states')]

    )


    joint_state_publisher_node = Node(
        condition=UnlessCondition(show_gui),
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        namespace='r1',
        
        
    )
    
    joint_state_publisher_gui_node2 = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        namespace='r2',
        
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )
    
    frame_joint=Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[os.path.join('shooting_set_description', 'config', 'frame_joint_controller.yaml')],
            output='screen'
        )

    return LaunchDescription([
        gui_arg,
        robot_state_publisher_node,
        robot2_state_publisher_node,
        # joint_state_publisher_node,
        # joint_state_publisher_gui_node,
        # joint_state_publisher_gui_node2,
        # frame_joint,
        rviz_node
    ])