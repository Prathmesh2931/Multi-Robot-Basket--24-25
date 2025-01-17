

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint




class launch_controller(Node):
    
    def __init__(self):
        super().__init__("launch_controller")
        
        self.get_logger().info("initialized launch controller")
        
        self.traj_pub = self.create_publisher(JointTrajectory, "/r2/joint_control", 10)

        self.timer = self.create_timer(0.5, self.timer_callback)
        self.traj_msg = JointTrajectory()
        self.traj_msg.joint_names = ['robot2_frame_joint', 'robot2_upper_shaft_joint', 'robot2_bottom_shaft_joint']
        self.pos = 0.0
        self.diff = 0.1
        
        
    def timer_callback(self):
        
        self.pos = self.pos + self.diff
        self.get_logger().info(f"position set to {self.pos}")
        
        if self.pos > 1.57 or self.pos < -1.57:
            self.diff = - self.diff
        
        loc = JointTrajectoryPoint()
        # loc.positions = [ self.pos ]
        loc.effort = [0.1, -10.1, 10.1]
        # loc.positions = [self.pos, self.pos, self.pos]
        loc.time_from_start.nanosec = 100000000
        
        self.traj_msg.points = [ loc ]
        self.traj_pub.publish(self.traj_msg)




def main(args = None):
    rclpy.init(args=args)
    
    lc = launch_controller()
    rclpy.spin(lc)
    
    rclpy.shutdown()

    
    
    