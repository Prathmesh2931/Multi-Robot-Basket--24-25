#!/usr/bin/env python3

import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
import time
import os
BTN_L2 = 2
BTN_L1 = 4
BTN_PS = 5
BTN_R1 = 5
BTN_R2 =5
TRIANGLE = 3
CROSS = 0
SQUARE=2
CIRCLE=1
X_axis=1
Y_axis=0
Z_axis=3
ARM_SPEED = 0.8


class joyController(Node):
   
    def __init__(self):
        namespace = os.getenv('ROS_NAMESPACE', '')
        namespace_prefix = f"{namespace}/" if namespace else ""  # Add prefix only if namespace is set
        super().__init__("joyController")
        # self.joy_sub = self.create_subscription(Joy, "/joy", self.joy_callback, 10)
        self.joy_sub = self.create_subscription(Joy, f"{namespace_prefix}joy", self.joy_callback, 10)

        self.fly_pub = self.create_publisher(Float32, "/flyWheel_speed", 10)
        self.ser_angle=self.create_publisher(Float32,"/flywheel_angle",10)
        self.arm_pub = self.create_publisher(Float32, "/arm_speed", 10)
        self.finger_pub = self.create_publisher(Bool, "/finger", 10)
        
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.flyWheelSpeed = 0.0
        # self.curr_angle=0.0
        self.finger = False
        self.armState = False
        
        
        self.msg = Float32()
        self.arm_msg = Float32()
        self.finger_msg = Bool()
        self.ser_angle_=Float32()
        
        # set initial state to inwards
        self.arm_msg.data = -ARM_SPEED
        # self.ser_angle_.data=0.0

        self.publishArmState()
        
    def joy_callback(self, msg : Joy):
       
        thresh_linear=0.02
        thresh_angular=0.001
        # enable button to prevent accidental clicks
        if msg.buttons[BTN_L1] == 1:
            
            
            self.msg.data = ( 1.0 - msg.axes[BTN_L2]) / 2.0
            self.finger_msg.data = msg.buttons[BTN_R1] == 1
            
            
            

                   
            
            if(msg.buttons[SQUARE]==1):
                self.ser_angle_.data +=0.05
            if(msg.buttons[CIRCLE]==1):
                self.ser_angle_.data-=0.05
                
            if not self.armState and msg.buttons[TRIANGLE] == 1:
                self.armState = not self.armState
                
                self.arm_msg.data = ARM_SPEED if self.armState else -ARM_SPEED
                self.publishArmState()

            if self.armState and msg.buttons[CROSS] == 1:
                self.armState = not self.armState

                self.arm_msg.data = ARM_SPEED if self.armState else -ARM_SPEED
                self.publishArmState2()

        else:
           
            self.msg.data = 0.0
            self.finger_msg.data = False
            self.arm_msg.data=0.0
            self.publishArmState()
            

        
        self.finger_pub.publish(self.finger_msg)
        self.fly_pub.publish(self.msg)
        
        self.ser_angle.publish(self.ser_angle_)
        # self.get_logger().info(f'flywheel {self.msg.data} finger {self.finger_msg.data} angle {self.ser_angle_}')
    
    
    def publishArmState2(self):
        self.get_logger().warning(f"publishing arm command {self.arm_msg.data}")
        self.arm_pub.publish(self.arm_msg)
        # time.sleep(1.0)
        # self.arm_pub.publish(self.arm_msg)
    def publishArmState(self):
        self.get_logger().warning(f"publishing arm command {self.arm_msg.data}")
        self.arm_pub.publish(self.arm_msg)
        time.sleep(1.0)
        self.arm_pub.publish(self.arm_msg)
        

    def timer_callback(self):
        # self.finger_pub.publish(self.finger_msg)
        # self.fly_pub.publish(self.msg)
        # self.ser_angle.publish(self.ser_angle_)
        self.get_logger().info(f'flywheel {self.msg.data} finger {self.finger_msg.data} angle {self.ser_angle_.data}')


        
def main():
    rclpy.init()
    
    cont = joyController()
    rclpy.spin(cont)


if __name__ == "__main__":
    main()