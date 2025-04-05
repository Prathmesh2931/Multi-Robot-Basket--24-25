
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

        # Timer for processing dynamic transform
        self.timer = self.create_timer(0.1, self.process_dynamic_transform)

    

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
       
        
        # Get dynamic transform
        dynamic_tf_1 = self.get_dynamic_transform(dynamic_target_frame_1, dynamic_source_frame_1)
        dynamic_tf_2 = self.get_dynamic_transform(dynamic_target_frame_2, dynamic_source_frame_2)
        if not dynamic_tf_1:
            return
        if not dynamic_tf_2:
            return

        

        # Combine transforms
        self.combine_transforms(dynamic_tf_1.transform, dynamic_tf_2.transform,basket='basket_1',robot='r1')
        
        
        
    def combine_transforms(self, dynamic_tf, static_tf,basket,robot):
        """Combines dynamic and static transforms into a final transform."""
        # Dynamic translation and rotation
        t1 = np.array([dynamic_tf.translation.x, dynamic_tf.translation.y, dynamic_tf.translation.z])
        q1 = [dynamic_tf.rotation.x, dynamic_tf.rotation.y, dynamic_tf.rotation.z, dynamic_tf.rotation.w]

        # Static translation and rotation
        t2 = np.array([static_tf.translation.x, static_tf.translation.y, static_tf.translation.z])
        q2 = [static_tf.rotation.x, static_tf.rotation.y, static_tf.rotation.z, static_tf.rotation.w]

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
        yaw=math.atan2(2.0*((combined_tf.transform.rotation.w*combined_tf.transform.rotation.z)+(combined_tf.transform.rotation.x*combined_tf.transform.rotation.y)),1.0-2.0*(combined_tf.transform.rotation.y**2+combined_tf.transform.rotation.z**2))
        # self.get_logger().info(f"Combined transform broadcasted: {combined_tf}")
        # yaw=math.atan2(combined_tf.transform.translation.y,combined_tf.transform.translation.x)
        self.get_logger().info(f'Robot {robot} to r2 distance: {dist} yaw :{yaw}')


def main(args=None):
    rclpy.init(args=args)
    node = Publishpose()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
