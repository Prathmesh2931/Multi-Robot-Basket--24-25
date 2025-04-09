#!/usr/bin/env python3

import rclpy
from rclpy.node import Node 
from std_srvs.srv import SetBool
from service_handler.srv import AlliBs
from std_msgs.msg import Float32
import os 
from geometry_msgs.msg import Twist
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from service_handler.srv import RpmVel
from rclpy.qos import QoSProfile


class Service_handle(Node):
    def __init__(self):
        # self.create_publisher()
        namespace = os.getenv('ROS_NAMESPACE', '')
        namespace_prefix = f"{namespace}/" if namespace else ""  # Add prefix only if namespace is set
        super().__init__('Node')
        self.callback_group = ReentrantCallbackGroup()

        self.create_service(AlliBs,f'{namespace_prefix}Allign',callback=self.call_serv,callback_group=self.callback_group)
        self.set_rpm=self.create_client(RpmVel,f"{namespace_prefix}RPM",qos_profile=QoSProfile(depth=10))
        self.sub_dis=self.create_subscription(Float32,f"{namespace_prefix}dis_b1",self.sub_dis,10)
        self.sub_ori=self.create_subscription(Float32,f"{namespace_prefix}ori_b1",self.sub_ori,10)
        self.sub_dis2=self.create_subscription(Float32,f"{namespace_prefix}dis_b2",self.sub_dis2,10)
        self.sub_ori2=self.create_subscription(Float32,f"{namespace_prefix}ori_b2",self.sub_ori2,10)
        self.pub_rpm=self.create_publisher(Float32,f"{namespace_prefix}set_rpm",10)
        
        
        self.vel_pub=self.create_publisher(Twist,f"{namespace_prefix}cmd_vel",10)
        print('init')
        self.start=False
        self.task_complete=False
        self.Ori_complete=False
        self.RPM_set=False
        
        self.basket=None
        self.distance=None
        self.distance2=None
        self.ori=None
        self.ori2=None
        self.create_timer(0.1,self.control_loop)
        
    def sub_dis(self,msg:Float32):
        # self.get_logger().info(f"Distance :{msg.data}")  
        self.distance=msg.data
        
        
    def sub_ori(self,msg:Float32):
        # self.get_logger().info(f"orienttation :{msg.data}")
        self.ori=msg.data
    
    def sub_dis2(self,msg:Float32):
        # self.get_logger().info(f"Distance 2:{msg.data}")  
        self.distance2=msg.data
        
        
    def sub_ori2(self,msg:Float32):
        # self.get_logger().info(f"orienttation 2:{msg.data}")
        self.ori2=msg.data
    
    def move_bot(self,val):
        cmd_vel=Twist()
        cmd_vel.angular.z=-val
        
        self.vel_pub.publish(cmd_vel)
        
    def correct_orie(self,kp,target,thresh):
        if self.basket=="b1":
          error=target-self.ori
        else:
          error=target-self.ori2  
          
          
        if abs(error)>=thresh:
            pid=error*kp
            self.move_bot(pid)
        else:
            self.get_logger().info(f"Alligned SuccessFully")
            self.Ori_complete=True
            self.move_bot(0.0)
            
    def call_rpm_set(self,dis,height,radius,angle=45):
        req=RpmVel.Request()
        req.distance=dis
        req.height=height
        req.wheel_radius=radius
        req.angle=angle
        
        fut =self.set_rpm.call_async(req)
        fut.add_done_callback(self.handle_rpm_response)
        # if fut.result().success:
        #     rpm_msg = Float32()
        #     rpm_msg.data = fut.result().rpm
        #     self.pub_rpm.publish(rpm_msg)
        #     self.RPM_set = True
        #     self.get_logger().info(f"RPM Set Successfully: ")
        
    def handle_rpm_response(self, future):
        try:
            response = future.result()
            if response.success:
                rpm_msg = Float32()
                rpm_msg.data = response.rpm
                self.pub_rpm.publish(rpm_msg)
                self.RPM_set = True
                self.get_logger().info(f"RPM Set Successfully: {response.rpm:.2f}")
            else:
                self.get_logger().warn("RPM setting failed (success=False).")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

    def control_loop(self):
        if not self.start:
            return 
        
        self.Kp=4.0
        self.Ki=0.01
        self.Kd=0.005
        self.target_ori=0.00
        self.thresh_ori=0.02
        self.angle_shoot=45.00
        self.wheel_radius=0.10
        
        if self.basket=="b1":
            dist=self.distance
        else:
            dist=self.distance2
            
        if not self.Ori_complete:
            self.correct_orie(self.Kp,target=self.target_ori,thresh=self.thresh_ori)
            
            return
        
        if not self.RPM_set:
            
            self.call_rpm_set(dis=dist,height=1.2,radius=self.wheel_radius,angle=self.angle_shoot)
            
            return
        
        self.task_complete=True
        self.start=False
        
    def call_serv(self,request,response):
        self.robot=request.robot
        self.basket=request.basket
        self.task_complete=False
        self.Ori_complete=False
        self.start=True
        self.RPM_set=False
        
        rate=self.create_rate(100,self.get_clock())
        while not self.task_complete:
            rate.sleep()
        
        self.get_logger().info(f"Task Completetd")
        response.success=True
        response.message="Success Full"
        
        # self.task_complete=False``
        return response


def main(args=None):
    rclpy.init(args=args)
    node=Service_handle()
    thread=MultiThreadedExecutor()
    thread.add_node(node)
    thread.spin()
    node.destroy_node()
    rclpy.shutdown()
if __name__=='__main__':
    main()