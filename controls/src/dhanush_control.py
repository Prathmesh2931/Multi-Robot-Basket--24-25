#!/usr/bin/env python3

import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from launch.actions import ExecuteProcess
import subprocess
from service_handler.srv import AlliBs
from rclpy.qos import QoSProfile
from rclpy.executors import MultiThreadedExecutor

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
        self.get_logger().info(f"{namespace_prefix}............................")

        # self.joy_sub = self.create_subscription(Joy, "/joy", self.joy_callback, 10)
        self.joy_sub = self.create_subscription(Joy, f"{namespace_prefix}joy", self.joy_callback, 10)

        self.fly_pub = self.create_publisher(Float64, f"{namespace_prefix}fly_wheel_up", 10)
        self.flydw_pub=self.create_publisher(Float64, f"{namespace_prefix}fly_wheel_dw",10)
        self.ser_angle=self.create_publisher(Float64,f"{namespace_prefix}frame_angle",10)
        self.dock_cli=self.create_client(AlliBs,f"{namespace_prefix}Allign",qos_profile=QoSProfile(depth=10))
        
        self.spawner_triggered=False
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.flyWheelSpeed = 0.0
        # self.curr_angle=0.0
        
        self.frame_angle=45
        self.update_fly_sp=500
        self.scale_angle=10
        
        self.msg = Float64()
        self.msg2=Float64()
        
        self.ser_angle_=Float64()
        
        # set initial state to inwards
        
        # self.ser_angle_.data=0.0

        
        
    def joy_callback(self, msg : Joy):
        namespace = self.get_namespace()
        namespace_prefix = f"{namespace}/" if namespace and namespace != '/' else ""
        if namespace_prefix=="/r1/":
            self.robot_name="r1"
        else:
            self.robot_name="r2"
        self.get_logger().info(f"{self.robot_name}...")
        # print(f"{namespace_prefix}............................")
        thresh_linear=0.02
        thresh_angular=0.001
        # enable button to prevent accidental clicks
        if msg.buttons[BTN_L1] == 1:
              
            self.msg.data = -((( 1.0 - msg.axes[BTN_L2]) / 2.0)*self.update_fly_sp)
            self.msg2.data= (( 1.0 - msg.axes[BTN_L2]) / 2.0)*self.update_fly_sp
            
                
            if (msg.buttons[TRIANGLE]):
                self.call_dock(robot=f"{self.robot_name}",basket="b1")
            if (msg.buttons[CROSS]):
                self.call_dock(robot=f"{self.robot_name}",basket="b2")
            if(msg.buttons[SQUARE]==1):
                self.ser_angle_.data =0.1
                self.frame_angle+= (self.ser_angle_.data)*self.scale_angle
            if(msg.buttons[CIRCLE]==1):
                self.ser_angle_.data=-0.1
                self.frame_angle-=(self.ser_angle_.data)*self.scale_angle
            if(msg.buttons[BTN_R1]==1 and not self.spawner_triggered):
                self.get_logger().info("R1 Pressed: Spawning ball...")
                subprocess.Popen(["ros2", "run", "sim_controller", "ball_spawner"])
                self.spawner_triggered = True  # prevent multiple triggers until released
            

        else:
            self.ser_angle_.data=0.0
            self.msg.data = 0.0
            self.msg2.data=0.0
            self.frame_angle+=0.0
            self.spawner_triggered = False 
            

        
       
        self.fly_pub.publish(self.msg)
        self.flydw_pub.publish(self.msg2)
        
        self.ser_angle.publish(self.ser_angle_)
        # self.get_logger().info(f'flywheel {self.msg.data} finger {self.finger_msg.data} angle {self.ser_angle_}')
    
    
    
    def call_dock(self,robot,basket):
        self.dock_req=AlliBs.Request()  
        self.dock_req.robot=robot
        self.dock_req.basket=basket
        
        fut=self.dock_cli.call_async(self.dock_req)
        fut.add_done_callback(self.dock_response_cb)

        # rclpy.spin_until_future_complete(self,fut)
        # if fut.result() is not None and fut.result().success:
        #     self.get_logger().info(f"Task Success Executed ")
            
    def dock_response_cb(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("Task Success Executed")
            else:
                self.get_logger().warn("Docking failed")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

    def timer_callback(self):
        # self.finger_pub.publish(self.finger_msg)
        # self.fly_pub.publish(self.msg)
        # self.ser_angle.publish(self.ser_angle_)
        
        self.get_logger().info(f'flywheel {self.msg.data,self.msg2.data}  angle {self.frame_angle}')


        
def main():
    rclpy.init()
    thread=MultiThreadedExecutor()
    cont = joyController()
    thread.add_node(cont)
    thread.spin()
    cont.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()