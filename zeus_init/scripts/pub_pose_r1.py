#!/usr/bin/env python3

import rclpy
from rclpy.node import Node 
from tf2_msgs.msg import TFMessage

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
# from zeus_init.msg import Pose
import time
# from tf_transformations import euler_from_quaternion
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Transform
from geometry_msgs.msg import TransformStamped


class Publishpose(Node):
    def __init__(self):
        super().__init__('pose_sub')
        # self.create_subscription(TFMessage,'/tf',self.sub_pose(),10)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pub_pose=self.create_publisher(Pose,'/r1/pose',10)
        self.pub_pose2=self.create_publisher(Pose,'/r2/pose',10)
        self.tim=self.create_timer(0.1,self.sub_pose)
       
    def sub_pose(self):
        time.sleep(0.1)
        msg=Pose()
        msg2=Pose()
        from_frame_rel = 'robot1_odom'
        to_frame_rel = 'robot1_base_link'
        from_frame_rel2 = 'robot2_odom'
        to_frame_rel2 = 'robot2_base_link'
        if self.tf_buffer.can_transform('robot1_odom', 'robot1_base_link', rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=2)):
            transform = self.tf_buffer.lookup_transform(from_frame_rel, to_frame_rel, rclpy.time.Time())
            msg.position.x=transform.transform.translation.x
            msg.position.y=transform.transform.translation.y
            msg.position.z=transform.transform.translation.z
            msg.orientation.x=transform.transform.rotation.x
            msg.orientation.y=transform.transform.rotation.y
            msg.orientation.z=transform.transform.rotation.z
            msg.orientation.w=transform.transform.rotation.w
            self.get_logger().info(f'{transform}')
            self.pub_pose.publish(msg)
            
            if self.tf_buffer.can_transform('robot2_odom', 'robot2_base_link', rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=2)):
                transform2 = self.tf_buffer.lookup_transform(from_frame_rel2, to_frame_rel2, rclpy.time.Time())
                msg2.position.x=transform2.transform.translation.x
                msg2.position.y=transform2.transform.translation.y
                msg2.position.z=transform2.transform.translation.z
                msg2.orientation.x=transform2.transform.rotation.x
                msg2.orientation.y=transform2.transform.rotation.y
                msg2.orientation.z=transform2.transform.rotation.z
                msg2.orientation.w=transform2.transform.rotation.w
                self.get_logger().info(f'{transform2}')
                self.pub_pose2.publish(msg2)
                
            # print(transform)
        else:
            self.get_logger().info('Transform not available')

       
   
def main(args=None):
    rclpy.init(args=args)
    node =Publishpose()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__=='__main__':
    main()