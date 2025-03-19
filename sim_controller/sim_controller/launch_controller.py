

# import rclpy
# from rclpy.node import Node
# from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint




# class launch_controller(Node):
    
#     def __init__(self):
#         super().__init__("launch_controller")
        
#         self.get_logger().info("initialized launch controller")
        
#         self.traj_pub = self.create_publisher(JointTrajectory, "/r1/joint_control", 10)

#         self.timer = self.create_timer(0.5, self.timer_callback)
#         self.traj_msg = JointTrajectory()
#         self.traj_msg.joint_names = ['robot1_frame_joint', 'robot1_upper_shaft_joint', 'robot1_bottom_shaft_joint']
#         self.pos = 0.0
#         self.diff = 0.1
        
        
#     def timer_callback(self):
        
#         self.pos = self.pos + self.diff
#         self.get_logger().info(f"position set to {self.pos}")
        
#         if self.pos > 1.57 or self.pos < -1.57:
#             self.diff = - self.diff
        
#         loc = JointTrajectoryPoint()
#         loc.positions = [ self.pos ]
#         # loc.effort = [0.1, 10.1, -10.1]
#         # loc.positions = [self.pos, self.pos, self.pos]
#         loc.time_from_start.nanosec = 100000000
        
#         self.traj_msg.points = [ loc ]
#         self.traj_pub.publish(self.traj_msg)




# def main(args = None):
#     rclpy.init(args=args)
    
#     lc = launch_controller()
#     rclpy.spin(lc)
    
#     rclpy.shutdown()

    



import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class LaunchController(Node):

    def __init__(self):
        super().__init__("launch_controller")

        self.get_logger().info("Initialized launch controller")

        self.traj_pub = self.create_publisher(JointTrajectory, "/r1/joint_control", 10)

        self.timer = self.create_timer(0.5, self.timer_callback)

        self.traj_msg = JointTrajectory()
        self.traj_msg.joint_names = ["robot1_upper_shaft_joint", "robot1_bottom_shaft_joint"]

        self.pos = 0.0
        self.diff = 0.5

    # def timer_callback(self):
    #     self.pos += self.diff
    #     self.get_logger().info(f"Position set to {self.pos}")

    #     if self.pos > 1.57 or self.pos < -1.57:
    #         self.diff = -self.diff

    #     # Define multiple effort points similar to your Ignition example
    #     points = []

    #     # First effort point
    #     point1 = JointTrajectoryPoint()
    #     point1.effort = [-1.0, 0.5]
    #     point1.time_from_start.sec = 1
    #     point1.time_from_start.nanosec = 0
    #     points.append(point1)

    #     # Second effort point
    #     point2 = JointTrajectoryPoint()
        
    #     point2.effort = [-2.5, 1.5]
    #     point2.time_from_start.sec = 1
    #     point2.time_from_start.nanosec = 500000000
    #     points.append(point2)

    #     # Third effort point
    #     point3 = JointTrajectoryPoint()
    #     point3.effort = [-0.4, -0.2]
    #     point3.time_from_start.sec = 1
    #     point3.time_from_start.nanosec = 750000000
    #     points.append(point3)

    #     self.traj_msg.points = points

    #     # Publish the message
    #     self.traj_pub.publish(self.traj_msg)
    def timer_callback(self):
        self.pos += self.diff
        self.get_logger().info(f"Position set to {self.pos}")

        if self.pos > 1.57 or self.pos < -1.57:
            self.diff = -self.diff

        points = []

        point1 = JointTrajectoryPoint()
        point1.positions = [self.pos, self.pos]
        point1.velocities = [0.0, 0.0]
        point1.effort = [-1.0, 0.5]
        point1.time_from_start.sec = 1
        points.append(point1)

        point2 = JointTrajectoryPoint()
        point2.positions = [self.pos + 0.2, self.pos + 0.2]
        point2.velocities = [0.0, 0.0]
        point2.effort = [-2.5, 1.5]
        point2.time_from_start.sec = 2
        points.append(point2)

        point3 = JointTrajectoryPoint()
        point3.positions = [self.pos - 0.1, self.pos - 0.1]
        point3.velocities = [0.0, 0.0]
        point3.effort = [-0.4, -0.2]
        point3.time_from_start.sec = 3
        points.append(point3)

        self.traj_msg.points = points
        self.traj_pub.publish(self.traj_msg)



def main(args=None):
    rclpy.init(args=args)

    lc = LaunchController()
    rclpy.spin(lc)

    rclpy.shutdown()




# import rclpy
# from rclpy.node import Node
# from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

# class LaunchController(Node):

#     def __init__(self):
#         super().__init__("launch_controller")

#         self.get_logger().info("Initialized launch controller")

#         self.traj_pub = self.create_publisher(JointTrajectory, "/r1/joint_control", 10)

#         self.timer = self.create_timer(0.2, self.timer_callback)  # Faster updates

#         self.traj_msg = JointTrajectory()
#         self.traj_msg.joint_names = ["robot1_upper_shaft_joint", "robot1_bottom_shaft_joint"]

#         self.vel = 0.2  # Initial velocity
#         self.vel_increment = 0.1  # Acceleration step

#     def timer_callback(self):
#         self.vel += self.vel_increment
#         self.get_logger().info(f"Velocity set to {self.vel}")

#         if self.vel > 2.5 or self.vel < -2.5:
#             self.vel_increment = -self.vel_increment  # Reverse direction smoothly

#         # Define velocity points for trajectory
#         points = []

#         # First velocity point
#         point1 = JointTrajectoryPoint()
#         point1.velocities = [self.vel, -self.vel]
#         point1.time_from_start.sec = 0
#         point1.time_from_start.nanosec = 50000000  # 50ms
#         points.append(point1)

#         # Second velocity point (increases speed)
#         point2 = JointTrajectoryPoint()
#         point2.velocities = [self.vel * 1.5, -self.vel * 1.2]
#         point2.time_from_start.sec = 1
#         point2.time_from_start.nanosec = 90000000
#         points.append(point2)

#         # Third velocity point (near max speed)
#         point3 = JointTrajectoryPoint()
#         point3.velocities = [self.vel * 2, -self.vel * 1.5]
#         point3.time_from_start.sec = 2
#         point3.time_from_start.nanosec = 500000000
#         points.append(point3)

#         self.traj_msg.points = points

#         # Publish the message
#         self.traj_pub.publish(self.traj_msg)


# def main(args=None):
#     rclpy.init(args=args)

#     lc = LaunchController()
#     rclpy.spin(lc)

#     rclpy.shutdown()


# import rclpy
# from rclpy.node import Node
# from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

# class LaunchController(Node):

#     def __init__(self):
#         super().__init__("launch_controller")

#         self.get_logger().info("Initialized launch controller")

#         self.traj_pub = self.create_publisher(JointTrajectory, "/r1/joint_control", 10)

#         self.timer = self.create_timer(0.5, self.timer_callback)  # Publish every 0.5s

#         self.traj_msg = JointTrajectory()
#         self.traj_msg.joint_names = ["robot1_upper_shaft_joint", "robot1_bottom_shaft_joint"]

#         self.fixed_vel = 0.5  # Set a constant velocity

#     def timer_callback(self):
#         self.get_logger().info(f"Publishing fixed velocity: {self.fixed_vel}")

#         point = JointTrajectoryPoint()
#         point.velocities = [self.fixed_vel, -self.fixed_vel]  # Set velocities instead of positions
#         point.time_from_start.sec = 1  # 1 second time from start
#         point.time_from_start.nanosec = 0

#         self.traj_msg.points = [point]  # Only one velocity point

#         self.traj_pub.publish(self.traj_msg)  # Publish once

# def main(args=None):
#     rclpy.init(args=args)

#     lc = LaunchController()
#     rclpy.spin(lc)

#     rclpy.shutdown()
