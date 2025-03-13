# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node 
# from tf2_msgs.msg import TFMessage

# from tf2_ros import TransformException
# from tf2_ros.buffer import Buffer
# from tf2_ros.transform_listener import TransformListener
# from tf2_ros.transform_broadcaster import TransformBroadcaster
# # from zeus_init.msg import Pose
# import time
# # from tf_transformations import euler_from_quaternion
# from geometry_msgs.msg import Pose
# from geometry_msgs.msg import Transform
# from geometry_msgs.msg import TransformStamped
# from tf_transformations import quaternion_multiply, quaternion_matrix, translation_matrix, concatenate_matrices, quaternion_from_matrix, translation_from_matrix

 
# class Publishpose(Node):
#     def __init__(self):
#         super().__init__('pose_sub')
#         # self.create_subscription(TFMessage,'/tf',self.sub_pose(),10)
#         self.tf_buffer = Buffer()
#         print('hi')
#         self.tf_listener = TransformListener(self.tf_buffer, self)
#         self.tf_broad=TransformBroadcaster(self)
#         print('bye')
#         self.tim=self.create_timer(0.1,self.sub_pose)
        
#     def get_transform(self,from_frame_rel,to_frame_rel):
#         try:
#             return self.tf_buffer.lookup_transform(to_frame_rel,from_frame_rel,rclpy.time.Time())
#         except:
#             return None
        
        
#     def static_transform(self,header,child):
#         static_trans=TransformStamped()
#         static_trans.header.frame_id=header
#         static_trans.child_frame_id=child
#         static_trans.transform.translation.x=6.455
#         static_trans.transform.translation.y=0.0
#         static_trans.transform.translation.z=2.43
#         static_trans.transform.rotation.x=0.0
#         static_trans.transform.rotation.y=0.0
#         static_trans.transform.rotation.z=0.0
#         static_trans.transform.rotation.w=0.0
        
#         return static_trans

    
#     def sub_pose(self):
#         header='map'
#         child='basket_1'
#         target_frame='robot1_base_link'
#         parent_frame ='robot1_odom'
        
#         dynamic_tf_1=self.get_transform(target_frame,parent_frame)
        
#         get_static=self.static_transform(header,child)
#         self.tf_buffer=TransformBroadcaster()
#         self.tf_buffer.sendTransform(get_static)
        
        
#         self.combined_transform(dynamic_tf_1.transform,get_static.transform)
        
    
#     def combined_transform(self,shooting,basket):
#         t1=[shooting.translation.x+0.05,shooting.translation.y,shooting.translation.z+1.201]
#         q1=[shooting.rotation.x,shooting.rotation.y,shooting.rotation.z,shooting.rotation.w]
        
#         t2=[basket.translation.x,basket.translation.y,basket.translation.z]
#         q2=[basket.rotation.x,basket.rotation.y,basket.rotation.z,basket.rotation.w]
        
        
#         mat1=concatenate_matrices(translation_matrix(t1),quaternion_matrix(q1))
#         mat2=concatenate_matrices(translation_matrix(t2),quaternion_matrix(q2))
        
#         combined_mat=concatenate_matrices(mat1,mat2)
        
#         comb_trans=translation_from_matrix(combined_mat)
#         comb_quat=quaternion_from_matrix(combined_mat)
        
#         estimation=TransformStamped()
#         estimation.transform.translation.x=comb_trans[0]
#         estimation.transform.translation.y=comb_trans[1]
#         estimation.transform.translation.z=comb_trans[2]
        
        
#         estimation.transform.rotation.x=comb_quat[0]
#         estimation.transform.rotation.y=comb_quat[1]
#         estimation.transform.rotation.z=comb_quat[2]
#         estimation.transform.rotation.x=comb_quat[3]

#         self.get_logger().info(f'estimate pose :{estimation}')


        
       
   
# def main(args=None):
#     rclpy.init(args=args)
#     node =Publishpose()
#     rclpy.spin(node)
#     rclpy.shutdown()


# if __name__=='__main__':
#     main()





#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros.transform_broadcaster import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from scipy.spatial.transform import Rotation as R
import numpy as np
import math

class Publishpose(Node):
    def __init__(self):
        super().__init__('pose_sub')

        # TF2 Buffer and Listener for dynamic transforms
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Broadcasters
        self.dynamic_broadcaster = TransformBroadcaster(self)
        self.static_broadcaster = StaticTransformBroadcaster(self)

        # Broadcast static transform once
        self.broadcast_static_transform_1()
        
        self.broadcast_static_transform_2()


        # Timer for processing dynamic transform
        self.timer = self.create_timer(0.1, self.process_dynamic_transform)

    def broadcast_static_transform_1(self):
        """Broadcasts the static transform once."""
        static_transform = TransformStamped()
        static_transform.header.stamp = self.get_clock().now().to_msg()
        static_transform.header.frame_id = "map"
        static_transform.child_frame_id = "basket_1"
        static_transform.transform.translation.x = 6.455
        static_transform.transform.translation.y = 0.0
        static_transform.transform.translation.z = 2.43   
        static_transform.transform.rotation.x = 0.0
        static_transform.transform.rotation.y = 0.0
        static_transform.transform.rotation.z = 0.0
        static_transform.transform.rotation.w = 1.0  # Identity quaternion

        # Use the static transform broadcaster
        self.static_broadcaster.sendTransform(static_transform)
        self.get_logger().info("Static transform broadcasted for basket1 ")
        
    def broadcast_static_transform_2(self):
        """Broadcasts the static transform once."""
        static_transform = TransformStamped()
        static_transform.header.stamp = self.get_clock().now().to_msg()
        static_transform.header.frame_id = "map"
        static_transform.child_frame_id = "basket_2"
        static_transform.transform.translation.x = -6.455
        static_transform.transform.translation.y = 0.0
        static_transform.transform.translation.z = 2.43
        static_transform.transform.rotation.x = 0.0
        static_transform.transform.rotation.y = 0.0
        static_transform.transform.rotation.z = 0.0
        static_transform.transform.rotation.w = 1.0  # Identity quaternion

        # Use the static transform broadcaster
        self.static_broadcaster.sendTransform(static_transform)
        self.get_logger().info("Static transform broadcasted. for basket 2")

    def get_dynamic_transform(self, target_frame, source_frame):
        """Retrieves the dynamic transform between two frames."""
        try:
            return self.tf_buffer.lookup_transform(
                target_frame, source_frame, rclpy.time.Time()
            )
        except Exception as e:
            self.get_logger().error(f"Dynamic transform lookup failed: {e}")
            return None

    def process_dynamic_transform(self):
        """Processes and combines dynamic and static transforms."""
        # Frame IDs
        dynamic_target_frame_1 = "robot1_base_link"
        dynamic_source_frame_1 = "robot1_odom"
        dynamic_target_frame_2 = "robot2_base_link"
        dynamic_source_frame_2 = "robot2_odom"
        static_source_frame_1 = "map"
        static_target_frame_1 = "basket_1"
        static_source_frame_2 = "map"
        static_target_frame_2 = "basket_2"
        
        # Get dynamic transform
        dynamic_tf_1 = self.get_dynamic_transform(dynamic_target_frame_1, dynamic_source_frame_1)
        dynamic_tf_2 = self.get_dynamic_transform(dynamic_target_frame_2, dynamic_source_frame_2)
        if not dynamic_tf_1:
            return
        if not dynamic_tf_2:
            return

        # Get static transform
        try:
            static_tf_1= self.tf_buffer.lookup_transform(
                static_source_frame_1, static_target_frame_1, rclpy.time.Time(),
            )
            static_tf_2= self.tf_buffer.lookup_transform(
                static_source_frame_2, static_target_frame_2, rclpy.time.Time(),
            )
            
        except Exception as e:
            self.get_logger().error(f"Static transform lookup failed: {e}")
            return

        # Combine transforms
        self.combine_transforms(dynamic_tf_1.transform, static_tf_1,basket='basket_1',robot='r1')
        self.combine_transforms(dynamic_tf_1.transform, static_tf_2,basket='basket_2',robot='r1') 
        self.combine_transforms(dynamic_tf_2.transform, static_tf_1,basket='basket_1',robot='r2')
        self.combine_transforms(dynamic_tf_2.transform, static_tf_2,basket='basket_2',robot='r2') 
        
        
    def combine_transforms(self, dynamic_tf, static_tf,basket,robot):
        """Combines dynamic and static transforms into a final transform."""
        # Dynamic translation and rotation
        t1 = np.array([dynamic_tf.translation.x, dynamic_tf.translation.y, dynamic_tf.translation.z])
        q1 = [dynamic_tf.rotation.x, dynamic_tf.rotation.y, dynamic_tf.rotation.z, dynamic_tf.rotation.w]

        # Static translation and rotation
        t2 = np.array([static_tf.transform.translation.x, static_tf.transform.translation.y, static_tf.transform.translation.z])
        q2 = [static_tf.transform.rotation.x, static_tf.transform.rotation.y, static_tf.transform.rotation.z, static_tf.transform.rotation.w]

        # Convert quaternions to rotation matrices
        r1 = R.from_quat(q1).as_matrix()
        r2 = R.from_quat(q2).as_matrix()

        # Create transformation matrices
        mat1 = np.eye(4)
        mat1[:3, :3] = r1
        mat1[:3, 3] = t1

        mat2 = np.eye(4)
        mat2[:3, :3] = r2
        mat2[:3, 3] = t2

        # Combine transformations
        combined_mat = np.dot(mat1, mat2)

        # Extract combined translation and rotation
        combined_translation = combined_mat[:3, 3]
        combined_rotation = R.from_matrix(combined_mat[:3, :3]).as_quat()

        # Broadcast the combined transform
        combined_tf = TransformStamped()
        combined_tf.header.stamp = self.get_clock().now().to_msg()
        combined_tf.header.frame_id = basket
        combined_tf.child_frame_id = robot
        combined_tf.transform.translation.x = combined_translation[0]
        combined_tf.transform.translation.y = combined_translation[1]
        combined_tf.transform.translation.z = combined_translation[2]
        combined_tf.transform.rotation.x = combined_rotation[0]
        combined_tf.transform.rotation.y = combined_rotation[1]
        combined_tf.transform.rotation.z = combined_rotation[2]
        combined_tf.transform.rotation.w = combined_rotation[3]

        self.dynamic_broadcaster.sendTransform(combined_tf)
        
        dist=math.sqrt( (combined_tf.transform.translation.x**2 + combined_tf.transform.translation.y**2))
        # yaw=math.atan2(2.0*((combined_tf.transform.rotation.w*combined_tf.transform.rotation.z)+(combined_tf.transform.rotation.x*combined_tf.transform.rotation.y)),1.0-2.0*(combined_tf.transform.rotation.y**2+combined_tf.transform.rotation.z**2))
        # self.get_logger().info(f"Combined transform broadcasted: {combined_tf}")
        yaw=math.atan2(combined_tf.transform.translation.y,combined_tf.transform.translation.x)
        self.get_logger().info(f'Robot {robot} to {basket} distance: {dist} yaw :{yaw}')


def main(args=None):
    rclpy.init(args=args)
    node = Publishpose()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
