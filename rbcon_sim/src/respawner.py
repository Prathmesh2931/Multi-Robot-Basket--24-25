

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, QoSDurabilityPolicy


import os


class respawner (Node):
    
    def __init__(self):
        super().__init__("respawner")
        
        self.desc_sub = self.create_subscription(String, "robot_description", self.desc_update_callback, QoSProfile(
            depth=1,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL))
        
        
        
        
    def desc_update_callback(self, msg : String):
        
        self.get_logger().info("log urdf \n\n" + msg.data)
        os.system('ign ')
        
        


def main():
    
    rclpy.init()
    respawn = respawner()
    rclpy.spin(respawn)

if __name__ == "__main__":
    main()