import rclpy
from rclpy.node import Node 
from nav_msgs.msg import Odometry
import rclpy.time
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Pose,Point,Quaternion
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from ros_gz_interfaces.srv import SpawnEntity
from ros2launch.api import launch_a_launch_file
import os

class ball_spawn(Node):
    def __init__(self):
        super().__init__('ball_spawn')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.timer = self.create_timer(2, self.tf_lookup_timer_callback)
        
        self.file_name='~/ws/src/rbcon_sim/sdf/basketball.sdf'
        self.model='basketball'
        self.spawnIndex = 0
     
    def tf_lookup_timer_callback(self):
        try:
            tf=self.tf_buffer.lookup_transform( 'base_link',
                                'map',
                                rclpy.time.Time())

            
            self.get_logger().info(f"got transforms {tf.transform.translation} ")
            self.spawn_ball(self.file_name, self.model + str(self.spawnIndex), 
                            tf.transform.translation.x,
                            tf.transform.translation.y,
                            tf.transform.translation.z + 2)

        except Exception as e:
            self.get_logger().info(f"failed to get transforms {e} ")
            return
        
        

    def spawn_ball(self,file_name,model,pose_x,pose_y,pose_z,orie_x=0,orie_y=0,orie_z=0,orie_w=0):
        
        self.spawnIndex += 1
        self.get_logger().info("spawn service called")
        
        try:
            ret = os.system(f'ros2 run ros_gz_sim create --file {self.file_name} -x {-pose_x} -y {-pose_y} -z {pose_z} -name {model}')
        except:
            self.get_logger().info("systemcall failed")

       

def main(args=None):
    rclpy.init(args=args)
    Node =ball_spawn()
    
    rclpy.spin(node=Node)
    rclpy.shutdown()


if __name__=='__main__':
   main()